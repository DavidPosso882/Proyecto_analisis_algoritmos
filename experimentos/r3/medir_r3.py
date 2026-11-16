"""T2 R3b — mide la envolvente propia y SciPy sobre la MISMA entrada entera.

Spec: `specs/R3.md` (UT-08: R3-07; R3-10). Reglas: EXP-02/03/04/08/11/13/14/16,
DA-17 (semilla derivada) y DA-18 (redondeo half-up, lado del cuadrado, n tras
dedup + generados, Cociente = propio/SciPy).

Preparación FUERA de la región medida (EXP-02, R3-07):
- Red real: nodos de la componente UT-04 (lectura) → UTM 18N (DA-10) → entero
  half-up (DA-18) → dedup. `n` informado = tras dedup; `generados` = antes.
- Cuadrados: 1 000 / 10 000 / 50 000 puntos enteros uniformes, semilla
  derivada ``42 + (500 + i)`` (DA-17) y lado = mayor dimensión del bbox UTM
  (DA-18), anclado en la esquina (xmin, ymin) del bbox.

Cada conjunto se entrega en el formato natural de cada versión: tupla de
tuplas de enteros (propio) y ``ndarray`` ``int64`` (SciPy). La región medida
solo llama a ``envolvente(...)`` y a ``ConvexHull(...)``; el símbolo de SciPy
se toma de `quindio.envolvente.referencia`, único módulo que importa
``scipy.spatial`` (excepción GLOB-03, tabla R3-12).

Salidas: `resultados/r3/mediciones.csv` (arnés UT-01, reanudable),
`resultados/r3/entradas_r3.json` (testigo de cada conjunto) y
`resultados/r3/vertices_red.csv` (R3-11, lo lee R5 sin recalcular).

Uso: .venv/bin/python experimentos/r3/medir_r3.py
"""
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np

from quindio.envolvente.quickhull import envolvente, redondear_half_up
from quindio.envolvente.referencia import ConvexHull, referencia
from quindio.medicion.arnes import (
    SEMILLA_MAESTRA,
    derivar_semilla,
    guardar_incremental,
    huella_entrada,
    ids_completados,
    medir,
)

RAIZ = Path(__file__).resolve().parents[2]
R3 = RAIZ / "resultados" / "r3"
SALIDA = R3 / "mediciones.csv"
ENTRADAS = R3 / "entradas_r3.json"
VERTICES = R3 / "vertices_red.csv"

INDICE_BASE = 500  # DA-17: semilla del cuadrado i = 42 + (500 + i)
TAMANOS_CUADRADO = (1_000, 10_000, 50_000)
CONJUNTOS = (("red", "Nodos de la red"),
             ("cuadrado_1000", "Cuadrado, 1 000 puntos"),
             ("cuadrado_10000", "Cuadrado, 10 000 puntos"),
             ("cuadrado_50000", "Cuadrado, 50 000 puntos"))
METODO_VERIFICACION = ("R3-05/R3-13: propio == SciPy (conjuntos) en los cuatro "
                       "conjuntos + degenerados a mano (R3-06)")


def fn_propio(pts, arr):
    """Región medida: solo ``envolvente`` sobre las tuplas ya preparadas."""
    casco = envolvente(pts)
    return casco, {"n": len(pts), "vertices": len(casco)}


def fn_scipy(pts, arr):
    """Región medida: solo ``ConvexHull`` sobre el ``ndarray`` ya preparado.

    El símbolo viene del módulo de referencia: la única importación de
    ``scipy.spatial`` del repositorio sigue viviendo allí (GLOB-03, R3-12).
    """
    casco = ConvexHull(arr)
    return None, {"n": len(arr), "vertices": len(casco.vertices)}


def _bbox(enteros):
    xs = [x for x, _ in enteros]
    ys = [y for _, y in enteros]
    return min(xs), max(xs), min(ys), max(ys)


def _nodos_red():
    """Nodos de UT-04 → enteros UTM (DA-10/DA-18), con su ``nodo_id``."""
    from quindio.red.asociacion import proyectar_nodos
    from quindio.red.procesado import cargar_procesado

    proc = cargar_procesado(str(RAIZ / "data" / "procesado"))
    enteros = []
    nodo_de = {}
    for nodo, (x, y) in proyectar_nodos(proc["grafo"]).items():
        punto = (redondear_half_up(x), redondear_half_up(y))
        enteros.append(punto)
        nodo_de.setdefault(punto, nodo)
    esperados = int(proc["metadato"]["componente"]["nodos"])
    if len(enteros) != esperados:  # GLOB-06: no medir con datos inconsistentes
        raise ValueError(f"red: {len(enteros)} nodos != metadato {esperados}")
    if len(nodo_de) != len(enteros):
        raise ValueError("red: dos nodos colapsan al mismo entero (revisar DA-18)")
    return enteros, nodo_de


def _cuadrado(n, semilla, lado, x0, y0):
    """n puntos enteros uniformes en [x0, x0+lado] × [y0, y0+lado] (DA-18)."""
    rnd = random.Random(semilla)
    return [(x0 + rnd.randrange(lado + 1), y0 + rnd.randrange(lado + 1))
            for _ in range(n)]


def preparar():
    """Construye los cuatro conjuntos enteros (fuera de la región medida)."""
    generados_red, nodo_de = _nodos_red()
    enteros_red = sorted(set(generados_red))
    xmin, xmax, ymin, ymax = _bbox(enteros_red)
    lado = max(xmax - xmin, ymax - ymin)
    nombres = dict(CONJUNTOS)
    conjuntos = {
        "red": {"nombre": nombres["red"], "enteros": enteros_red,
                "generados": len(generados_red), "semilla": SEMILLA_MAESTRA,
                "semilla_generacion": None, "nodo_de": nodo_de},
    }
    for i, n in enumerate(TAMANOS_CUADRADO):
        clave = f"cuadrado_{n}"
        semilla = derivar_semilla(INDICE_BASE + i)
        generados = _cuadrado(n, semilla, lado, xmin, ymin)
        conjuntos[clave] = {"nombre": nombres[clave],
                            "enteros": sorted(set(generados)),
                            "generados": len(generados), "semilla": semilla,
                            "semilla_generacion": semilla, "lado": lado,
                            "x0": xmin, "y0": ymin}
    bbox = {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}
    return conjuntos, bbox, lado


def verificar(conjuntos):
    """EXP-07/GLOB-06: casos degenerados a mano y propio == SciPy antes de medir."""
    assert envolvente([(0, 0), (1, 1), (2, 2), (3, 3)]) == [(0, 0), (3, 3)]
    assert sorted(envolvente([(0, 0), (4, 0), (4, 4), (0, 4), (2, 0), (4, 2),
                              (2, 4), (0, 2), (1, 1)])) == [
        (0, 0), (0, 4), (4, 0), (4, 4)]
    for datos in conjuntos.values():
        if set(envolvente(datos["enteros"])) != referencia(datos["enteros"]):
            raise ValueError(f"{datos['nombre']}: propio != SciPy (GLOB-06)")
    return True


def _escribir_vertices(vertices_utm, nodo_de):
    """R3-11: vértices de la red (enteros UTM + lon/lat) para R5."""
    from pyproj import Transformer

    trans = Transformer.from_crs("epsg:32618", "epsg:4326", always_xy=True)
    with open(VERTICES, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["orden", "x_utm", "y_utm", "lon", "lat", "nodo_id"])
        for orden, (x, y) in enumerate(vertices_utm):
            lon, lat = trans.transform(x, y)
            writer.writerow([orden, x, y, f"{lon:.7f}", f"{lat:.7f}",
                             nodo_de[(x, y)]])
    return len(vertices_utm)


def main():
    R3.mkdir(parents=True, exist_ok=True)
    conjuntos, bbox, lado = preparar()
    verificado = verificar(conjuntos)
    hechos = ids_completados(str(SALIDA))
    entradas = {
        "requerimiento": "R3",
        "spec": "specs/R3.md UT-08 (R3-07, R3-10, R3-11)",
        "epsg": "EPSG:32618",
        "redondeo": "half-up de quindio.envolvente.quickhull.redondear_half_up (DA-18)",
        "dedup": "sí; n = puntos tras deduplicar, generados = antes (DA-18)",
        "region_medida": ("solo la envolvente: envolvente(pts) y ConvexHull(arr) "
                          "sobre la entrada ya preparada (EXP-02, R3-07)"),
        "formato_propio": "tupla de tuplas de int (Python)",
        "formato_scipy": "ndarray int64 (n, 2)",
        "semilla_maestra": SEMILLA_MAESTRA,
        "indice_base": INDICE_BASE,
        "bbox_utm": bbox,
        "lado_cuadrado": lado,
        "conjuntos": {},
    }
    for clave, nombre in CONJUNTOS:
        datos = conjuntos[clave]
        pts = tuple(datos["enteros"])
        arr = np.array(pts, dtype=np.int64)  # formato SciPy, fuera de la región
        if set(map(tuple, arr.tolist())) != set(pts):
            raise ValueError(f"{clave}: el ndarray no representa el mismo conjunto")
        casco_propio = envolvente(datos["enteros"])
        frente_scipy = referencia(datos["enteros"])
        if set(casco_propio) != frente_scipy:
            raise ValueError(f"{nombre}: propio != SciPy antes de medir (GLOB-06)")
        huella = huella_entrada((pts, arr))
        entradas["conjuntos"][clave] = {
            "nombre": nombre, "n": len(pts),
            "generados": datos["generados"],
            "semilla_efectiva": datos["semilla"],
            "semilla_generacion": datos["semilla_generacion"],
            "lado_cuadrado": datos.get("lado"),
            "x0": datos.get("x0"), "y0": datos.get("y0"),
            "vertices": len(casco_propio),
            "huella_entrada": huella,
        }
        if clave == "red":
            entradas["conjuntos"][clave]["vertices_archivo"] = _escribir_vertices(
                casco_propio, datos["nodo_de"])
        for version, fn in (("propio", fn_propio), ("scipy", fn_scipy)):
            mid = f"{clave}:{version}"
            if mid in hechos:
                print(mid, "ya medida, se omite")
                continue
            fila = medir(fn, (pts, arr), id_medicion=mid,
                         semilla=datos["semilla"],
                         metodo_verificacion=METODO_VERIFICACION,
                         verificacion=lambda: verificado)
            info = dict(fila["info"] or {})
            info.update({
                "conjunto": nombre,
                "generados": datos["generados"],
                "vertices_scipy": len(frente_scipy),
                "vertices_iguales_scipy": True,
                "semilla_generacion": datos["semilla_generacion"],
                "formato_entrada": (entradas["formato_propio"] if version == "propio"
                                    else entradas["formato_scipy"]),
                "huella_conjunto": huella,
            })
            fila["info"] = info
            guardar_incremental(str(SALIDA), fila)
            med = fila["mediana_ms"]
            print(mid, fila["estado"],
                  f"mediana_ms={med:.3f}" if med else "sin tiempo",
                  f"crudos={len(fila['tiempos_ms_crudos'])}",
                  f"n={info.get('n')} vertices={info.get('vertices')}")
    with open(ENTRADAS, "w", encoding="utf-8") as fh:
        json.dump(entradas, fh, indent=2, sort_keys=True)
    print("CSV:", SALIDA)
    print("entradas:", ENTRADAS)
    print("vértices red:", VERTICES)


if __name__ == "__main__":
    main()
