"""Arnés de medición UT-01 (FASE-01).

Cubre EXP-01..EXP-16 en lo aplicable al arnés, DA-16 (mecánica firmada
2026-10-27) y DA-17 (semilla maestra 42). Se prueba con funciones de
duración conocida, sin algoritmos reales.

Reglas implementadas (ver odd/tasks/fase-01-arnes.md, S1-S6):
- EXP-03: 5 repeticiones, mediana (3er ordenado), sin descartar la 1ra.
- EXP-04/DA-16: tras la 1ra repetición, si supera el umbral (real: 60 s)
  no se repite y se reporta ese valor.
- EXP-08/DA-04: tope de pared (real: 300 s) en proceso hijo; al pasarlo se
  termina el hijo y se registra estado ``no_completada`` sin tiempo.
- EXP-02: solo el algoritmo en la región medida (``preparar`` queda fuera).
- EXP-05/DA-16: temporizador ``time.perf_counter_ns``; UNICO punto de
  conversión a ms: :func:`ns_a_ms`.
- EXP-06/DA-17: semilla maestra 42, derivadas ``42 + índice``.
- EXP-11: huella de la entrada entregada a cada algoritmo comparado.
- EXP-13: sin cachés entre repeticiones; la entrada no se muta (se verifica
  por huella antes/después y se entrega una copia por repetición).
- EXP-14: metadatos + 5 crudos en cada fila.
- EXP-01: la fusión rechaza máquinas distintas.
- EXP-16: escritura incremental y reanudación sin repetir completadas.
- GLOB-06: la verificación previa aborta la medición si falla.
"""

import copy
import csv
import gc
import hashlib
import json
import multiprocessing as mp
import os
import pickle
import platform
import time
from datetime import UTC, datetime

# Constantes reales (EXP-04, EXP-08). Las pruebas usan valores reducidos
# pasados por parámetro; estas constantes no se alteran en pruebas.
UMBRAL_UNA_SOLA_S = 60
TOPE_PARED_S = 5 * 60

SEMILLA_MAESTRA = 42  # DA-17

ESTADO_OK = "ok"
ESTADO_NO_COMPLETADA = "no_completada"


class VerificacionFallida(Exception):
    """La verificación previa (GLOB-06, EXP-07) falló: no se mide."""


class EntradaMutada(Exception):
    """La entrada cambió durante la región medida (EXP-13)."""


class ErrorMedicion(Exception):
    """El algoritmo lanzó una excepción dentro del hijo."""


def ns_a_ms(ns):
    """UNICO punto de conversión a ms (EXP-05). Toda salida en ms pasa aquí."""
    return ns / 1e6


def mediana_de(valores):
    """Mediana de 5: tercer valor ordenado (EXP-03). Pura, sin E/S."""
    ordenados = sorted(valores)
    return ordenados[len(ordenados) // 2]


def debe_medir_una_sola(primera_s, umbral_s=UMBRAL_UNA_SOLA_S):
    """Decisión EXP-04/DA-16 tras la 1ra repetición. Pura."""
    return primera_s > umbral_s


def derivar_semilla(indice):
    """Semilla derivada determinista: maestra + índice estable (DA-17)."""
    return SEMILLA_MAESTRA + indice


def huella_entrada(entrada):
    """Huella sha256 de la entrada (EXP-11, EXP-13)."""
    try:
        blob = pickle.dumps(entrada, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception:  # noqa: BLE001 - cualquier fallo: repr como respaldo
        blob = repr(entrada).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _ram_mb():
    """RAM física en MB, en Linux/Mac (sysconf) y en Windows (API de Win32)."""
    if hasattr(os, "sysconf"):
        try:
            return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") // (1024 * 1024)
        except (ValueError, OSError):
            return "desconocida"
    if platform.system() == "Windows":
        import ctypes

        class _Estado(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        estado = _Estado()
        estado.dwLength = ctypes.sizeof(_Estado)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado)):
            return estado.ullTotalPhys // (1024 * 1024)
    return "desconocida"


def huella_maquina():
    """Huella de la máquina actual (EXP-01, EXP-14)."""
    return {
        "sistema": platform.system(),
        "version_so": platform.release(),
        "cpu": platform.machine(),
        "procesador": platform.processor(),
        "ram_mb": _ram_mb(),
        "python": platform.python_version(),
    }


def versiones_libs():
    """Versiones de las bibliotecas del proyecto si están importables (EXP-14)."""
    versiones = {}
    for nombre in ("networkx", "numpy", "scipy", "shapely", "matplotlib"):
        try:
            mod = __import__(nombre)
            versiones[nombre] = getattr(mod, "__version__", "instalada")
        except ImportError:
            continue
    return versiones


def _hijo_medir(conn, fn, args, kwargs, preparar, args_prep):
    """Corre en el proceso hijo: prepara fuera de región, mide dentro (EXP-02).

    El hijo mide su propio tiempo tras cargar las entradas (DA-16) con GC
    desactivada solo en la región (DA-16, registrada en el padre).
    """
    try:
        if preparar is not None:
            preparar(*args_prep)
        antes = huella_entrada(args)
        gc.disable()
        try:
            t0 = time.perf_counter_ns()
            valor, info = fn(*args, **kwargs)
            t1 = time.perf_counter_ns()
        finally:
            gc.enable()
        despues = huella_entrada(args)
        conn.send((True, (t1 - t0, valor, info, antes, despues, "")))
    except Exception as exc:  # noqa: BLE001 - se propaga como dato
        conn.send((True, (None, None, {}, "", "", f"{type(exc).__name__}: {exc}")))
    finally:
        conn.close()


_CTX = mp.get_context("spawn")


def _una_repeticion(fn, args, kwargs, preparar, args_prep, tope_s):
    """Una repetición aislada en proceso hijo con tope de pared (EXP-08/DA-16).

    Devuelve (elapsed_ns, info, huella_antes, huella_despues) o
    (None, None, {}, "", "") si el hijo superó el tope y fue terminado.
    Lee el pipe antes de join para no trabarse con resultados grandes.
    """
    padre, hijo = mp.Pipe(duplex=False)
    proc = _CTX.Process(
        target=_hijo_medir, args=(hijo, fn, args, kwargs, preparar, args_prep)
    )
    proc.start()
    hijo.close()  # el padre cierra su copia del extremo del hijo tras el start
    # Leer ANTES de join: si el hijo envía más que el buffer del pipe (64 KB,
    # p. ej. distancias de la matriz), esperar en join lo traba para siempre.
    limite = time.monotonic() + tope_s
    while True:
        restante = limite - time.monotonic()
        if restante <= 0:
            proc.terminate()
            proc.join()
            padre.close()
            return None, None, "", ""
        if padre.poll(min(restante, 0.05)):
            break
    try:
        ok, payload = padre.recv()
    except EOFError:
        proc.join()
        padre.close()
        raise ErrorMedicion("el hijo murió sin enviar resultado")
    padre.close()
    proc.join()
    assert ok
    elapsed_ns, _valor, info, antes, despues, error = payload
    if error:
        raise ErrorMedicion(error)
    return elapsed_ns, info, antes, despues


def medir(fn, entrada, *, id_medicion, semilla, n_rep=5,
          umbral_una_sola_s=UMBRAL_UNA_SOLA_S, tope_pared_s=TOPE_PARED_S,
          preparar=None, metodo_verificacion="", verificacion=None,
          info_extra=None):
    """Mide ``fn(*entrada)`` según EXP-01..EXP-08 y devuelve la fila (EXP-14).

    ``fn`` debe devolver ``(valor, info)`` donde ``info`` es un dict con las
    columnas deterministas (p. ej. nodos_explorados). ``entrada`` es la tupla
    de argumentos. ``verificacion`` es un callable sin args que devuelve True
    si el algoritmo está verificado (GLOB-06): si falla, se aborta.
    """
    if verificacion is not None and not verificacion():
        raise VerificacionFallida(id_medicion)
    args_base = tuple(entrada)
    huella = huella_entrada(args_base)
    crudos_ns = []
    infos = []
    for i in range(n_rep):
        args = copy.deepcopy(args_base)  # copia idéntica por repetición (EXP-11)
        elapsed_ns, info, antes, despues = _una_repeticion(
            fn, args, {}, preparar, (),
            tope_pared_s,
        )
        if elapsed_ns is None:  # superó el tope: no_completada sin tiempo
            return _fila(id_medicion, ESTADO_NO_COMPLETADA, [], None,
                         semilla, huella, metodo_verificacion, info_extra)
        if antes != despues or antes != huella:
            raise EntradaMutada(id_medicion)
        crudos_ns.append(elapsed_ns)
        infos.append(info)
        if i == 0 and debe_medir_una_sola(elapsed_ns / 1e9, umbral_una_sola_s):
            break  # EXP-04: más de un minuto -> una sola medición
    crudos_ms = [ns_a_ms(ns) for ns in crudos_ns]
    if len(crudos_ms) == n_rep:
        mediana_ms = mediana_de(crudos_ms)
    else:
        mediana_ms = crudos_ms[0]  # una sola medición (EXP-04)
    return _fila(id_medicion, ESTADO_OK, crudos_ms, mediana_ms,
                 semilla, huella, metodo_verificacion, info_extra, infos)


def _fila(id_medicion, estado, crudos_ms, mediana_ms, semilla, huella,
          metodo_verificacion, info_extra=None, infos=None):
    maquina = huella_maquina()
    return {
        "id_medicion": id_medicion,
        "estado": estado,
        "mediana_ms": mediana_ms,
        "tiempos_ms_crudos": crudos_ms,
        "semilla_efectiva": semilla,
        "maquina": maquina,
        "maquina_id": hashlib.sha256(
            json.dumps(maquina, sort_keys=True).encode()).hexdigest(),
        "python_version": platform.python_version(),
        "versiones": versiones_libs(),
        "fecha": datetime.now(UTC).isoformat(),
        "huella_entrada": huella,
        "metodo_verificacion": metodo_verificacion,
        "gc_desactivada_en_region": True,
        "unidad": "ms",
        "info": (infos[-1] if infos else (info_extra or {})),
    }


COLUMNAS = ["id_medicion", "estado", "mediana_ms", "tiempos_ms_crudos",
            "semilla_efectiva", "maquina", "maquina_id", "python_version",
            "versiones", "fecha", "huella_entrada", "metodo_verificacion",
            "gc_desactivada_en_region", "unidad", "info"]


def _serializar(fila):
    fila = dict(fila)
    for clave in ("tiempos_ms_crudos", "maquina", "versiones", "info"):
        fila[clave] = json.dumps(fila[clave], sort_keys=True)
    return fila


def _deserializar(fila):
    fila = dict(fila)
    for clave in ("tiempos_ms_crudos", "maquina", "versiones", "info"):
        fila[clave] = json.loads(fila[clave])
    fila["mediana_ms"] = float(fila["mediana_ms"]) if fila["mediana_ms"] else None
    fila["semilla_efectiva"] = int(fila["semilla_efectiva"])
    fila["gc_desactivada_en_region"] = fila["gc_desactivada_en_region"] == "True"
    return fila


def guardar_incremental(path, fila):
    """Agrega la fila al CSV, creando el archivo si no existe (EXP-16)."""
    existe = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNAS)
        if not existe:
            writer.writeheader()
        writer.writerow(_serializar(fila))


def cargar_filas(path):
    """Lee todas las filas del CSV (vacío si no existe)."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [_deserializar(r) for r in csv.DictReader(fh)]


def ids_completados(path):
    """IDs con estado ok ya medidos: reanudar los salta (EXP-16)."""
    return {f["id_medicion"] for f in cargar_filas(path) if f["estado"] == "ok"}


def fusionar(filas_nuevas, filas_existentes):
    """Agrega filas nuevas rechazando mezcla de máquinas (EXP-01)."""
    maquinas = {f["maquina_id"] for f in filas_existentes} | {
        f["maquina_id"] for f in filas_nuevas}
    if len(maquinas) > 1:
        raise ValueError("EXP-01: máquinas distintas en la misma serie")
    return list(filas_existentes) + list(filas_nuevas)
