"""Pruebas del arnés UT-01 con funciones de duración conocida (FASE-01, T3).

Nombres con ID de regla (REPO-03). Límites reducidos por parámetro;
las constantes reales (60 s / 300 s) no se alteran.
"""
import time

import pytest

from quindio.medicion.arnes import (
    ESTADO_NO_COMPLETADA,
    ESTADO_OK,
    TOPE_PARED_S,
    UMBRAL_UNA_SOLA_S,
    EntradaMutada,
    VerificacionFallida,
    cargar_filas,
    debe_medir_una_sola,
    derivar_semilla,
    fusionar,
    guardar_incremental,
    huella_entrada,
    ids_completados,
    mediana_de,
    medir,
    ns_a_ms,
)

# --- Funciones de duración conocida (nivel módulo: picklables para spawn) ---

def fn_rapida(x):
    return x * 2, {"doble": x * 2}


def fn_otro_algoritmo(x):
    return x + 100, {"mas100": x + 100}


def fn_lenta(seg):
    time.sleep(seg)
    return seg, {"dormido_s": seg}


def fn_mutante(items):
    items.append("x")
    return len(items), {}


def preparar_lenta():
    time.sleep(0.4)


# --- EXP-03 ---

def test_EXP_03_mediana_es_tercer_ordenado():
    assert mediana_de([5, 1, 4, 2, 3]) == 3


def test_EXP_03_guarda_cinco_crudos_y_mediana():
    fila = medir(fn_rapida, (21,), id_medicion="exp03",
                 semilla=derivar_semilla(0), verificacion=lambda: True,
                 metodo_verificacion="caso a mano")
    assert fila["estado"] == ESTADO_OK
    assert len(fila["tiempos_ms_crudos"]) == 5
    assert fila["mediana_ms"] == pytest.approx(
        sorted(fila["tiempos_ms_crudos"])[2])
    assert fila["info"] == {"doble": 42}


# --- EXP-04 ---

def test_EXP_04_decide_tras_primera_repeticion():
    assert debe_medir_una_sola(61.0) is True
    assert debe_medir_una_sola(60.0) is False


def test_EXP_04_una_sola_si_supera_umbral():
    fila = medir(fn_lenta, (0.3,), id_medicion="exp04-larga",
                 semilla=derivar_semilla(1), umbral_una_sola_s=0.1,
                 verificacion=lambda: True)
    assert fila["estado"] == ESTADO_OK
    assert len(fila["tiempos_ms_crudos"]) == 1


def test_EXP_04_cinco_si_primera_bajo_umbral():
    fila = medir(fn_rapida, (7,), id_medicion="exp04-corta",
                 semilla=derivar_semilla(2), umbral_una_sola_s=60,
                 verificacion=lambda: True)
    assert len(fila["tiempos_ms_crudos"]) == 5


# --- EXP-08 ---

def test_EXP_08_tope_da_no_completada_sin_tiempo():
    fila = medir(fn_lenta, (30.0,), id_medicion="exp08",
                 semilla=derivar_semilla(3), tope_pared_s=0.5,
                 verificacion=lambda: True)
    assert fila["estado"] == ESTADO_NO_COMPLETADA
    assert fila["mediana_ms"] is None
    assert fila["tiempos_ms_crudos"] == []


def test_EXP_08_constante_real_es_cinco_minutos():
    assert TOPE_PARED_S == 300
    assert UMBRAL_UNA_SOLA_S == 60


# --- EXP-02 ---

def test_EXP_02_preparacion_fuera_de_region():
    fila = medir(fn_rapida, (3,), id_medicion="exp02",
                 semilla=derivar_semilla(4), preparar=preparar_lenta,
                 verificacion=lambda: True)
    assert fila["estado"] == ESTADO_OK
    assert fila["mediana_ms"] < 400  # los 400 ms de preparar no se miden


# --- EXP-11 / EXP-13 ---

def test_EXP_11_misma_entrada_misma_huella():
    f1 = medir(fn_rapida, (11,), id_medicion="exp11-a",
               semilla=derivar_semilla(5), verificacion=lambda: True)
    f2 = medir(fn_otro_algoritmo, (11,), id_medicion="exp11-b",
               semilla=derivar_semilla(5), verificacion=lambda: True)
    assert f1["huella_entrada"] == f2["huella_entrada"]


def test_EXP_13_detecta_entrada_mutada():
    with pytest.raises(EntradaMutada):
        medir(fn_mutante, ([1, 2],), id_medicion="exp13",
              semilla=derivar_semilla(6), verificacion=lambda: True)


def test_EXP_13_huella_intacta_tras_medir():
    args = (9,)
    fila = medir(fn_rapida, args, id_medicion="exp13b",
                 semilla=derivar_semilla(7), verificacion=lambda: True)
    assert fila["huella_entrada"] == huella_entrada(args)


# --- EXP-05 / EXP-06 / EXP-14 ---

def test_EXP_05_conversion_unica_a_ms():
    assert ns_a_ms(1_500_000) == pytest.approx(1.5)


def test_EXP_06_DA17_semilla_maestra_42_y_derivacion():
    assert derivar_semilla(0) == 42
    assert derivar_semilla(3) == 45
    assert derivar_semilla(3) == derivar_semilla(3)


def test_EXP_14_fila_trae_metadatos_y_crudos():
    fila = medir(fn_rapida, (5,), id_medicion="exp14",
                 semilla=derivar_semilla(8), verificacion=lambda: True,
                 metodo_verificacion="biblioteca")
    for clave in ("id_medicion", "estado", "mediana_ms", "tiempos_ms_crudos",
                  "semilla_efectiva", "maquina", "maquina_id", "python_version",
                  "versiones", "fecha", "huella_entrada", "metodo_verificacion",
                  "gc_desactivada_en_region", "unidad", "info"):
        assert clave in fila
    assert fila["unidad"] == "ms"
    assert fila["semilla_efectiva"] == 42 + 8
    assert fila["metodo_verificacion"] == "biblioteca"
    assert fila["gc_desactivada_en_region"] is True
    assert set(fila["maquina"]) >= {"sistema", "ram_mb", "python"}


# --- GLOB-06 / GLOB-07+EXP-15 / EXP-01 / EXP-16 ---

def test_GLOB06_verificacion_previa_aborta_si_falla():
    with pytest.raises(VerificacionFallida):
        medir(fn_rapida, (1,), id_medicion="g06",
              semilla=derivar_semilla(9), verificacion=lambda: False)


def test_GLOB07_EXP15_misma_semilla_mismo_determinista():
    f1 = medir(fn_rapida, (13,), id_medicion="rep-a",
               semilla=derivar_semilla(10), verificacion=lambda: True)
    f2 = medir(fn_rapida, (13,), id_medicion="rep-b",
               semilla=derivar_semilla(10), verificacion=lambda: True)
    assert f1["info"] == f2["info"]
    assert f1["huella_entrada"] == f2["huella_entrada"]


def fn_carga_grande(n):
    return None, {"muchos": list(range(n))}


def test_EXP08_carga_grande_no_se_traba():
    # Regresión: un resultado mayor que el buffer del pipe (64 KB) debe
    # llegar igual; antes se marcaba no_completada por leer tras el join.
    fila = medir(fn_carga_grande, (20000,), id_medicion="big",
                 semilla=derivar_semilla(20), tope_pared_s=60,
                 verificacion=lambda: True)
    assert fila["estado"] == ESTADO_OK
    assert fila["info"] == {"muchos": list(range(20000))}


def test_EXP01_fusionar_rechaza_otra_maquina():
    f1 = medir(fn_rapida, (2,), id_medicion="m1",
               semilla=derivar_semilla(11), verificacion=lambda: True)
    f2 = dict(f1, id_medicion="m2", maquina_id="otra-maquina")
    with pytest.raises(ValueError):
        fusionar([f2], [f1])
    assert len(fusionar([dict(f1, id_medicion="m2")], [f1])) == 2


def test_EXP16_reanudar_no_repite_completadas(tmp_path):
    csv_path = str(tmp_path / "serie.csv")
    f1 = medir(fn_rapida, (4,), id_medicion="s1",
               semilla=derivar_semilla(12), verificacion=lambda: True)
    guardar_incremental(csv_path, f1)
    assert ids_completados(csv_path) == {"s1"}
    # Reanudación: s1 se salta, solo se mide s2
    pendientes = [m for m in ("s1", "s2") if m not in ids_completados(csv_path)]
    assert pendientes == ["s2"]
    f2 = medir(fn_otro_algoritmo, (4,), id_medicion="s2",
               semilla=derivar_semilla(12), verificacion=lambda: True)
    guardar_incremental(csv_path, f2)
    filas = cargar_filas(csv_path)
    assert [f["id_medicion"] for f in filas] == ["s1", "s2"]
    assert all(f["estado"] == ESTADO_OK for f in filas)
