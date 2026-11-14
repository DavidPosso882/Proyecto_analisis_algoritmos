"""Pruebas offline de red: memoria, pesos puros, metadato, componente (R1a).

Nombres con ID de regla (REPO-03). La descarga real va en experimentos/.
"""
import math

import networkx as nx
import pytest

from quindio.red.componente import componente_mas_grande
from quindio.red.descarga import construir_metadato, guardar_crudo, validar_metadato
from quindio.red.memoria import estimar_mb
from quindio.red.pesos import tiempo_viaje_s


def test_R1_02_mb_con_V_E_a_mano():
    # V=1000, E=2000: matriz = 1e6*8 B = 7.629 MB; listas = (8000+48000)/MB.
    r = estimar_mb(1000, 2000)
    assert r["matriz_mb"] == pytest.approx(1_000_000 * 8 / (1024 * 1024))
    assert r["listas_mb"] == pytest.approx(56_000 / (1024 * 1024))
    assert r["listas_mb"] < r["matriz_mb"]


def test_R1_03_tiempo_es_distancia_sobre_velocidad():
    assert tiempo_viaje_s(100.0, 36.0) == pytest.approx(10.0)  # 36 km/h = 10 m/s
    with pytest.raises(ValueError):
        tiempo_viaje_s(100.0, 0.0)


def test_R1_01_metadato_con_campos_no_vacios():
    meta = construir_metadato(10, 20)
    validar_metadato(meta)
    assert meta["parametros"]["network_type"] == "drive"
    assert meta["origen"] == "descarga"


def test_R1_01_no_sobrescribe_crudo(tmp_path):
    G = nx.MultiDiGraph()
    G.add_edge(0, 1, length=5.0)
    gml = str(tmp_path / "x.graphml")
    meta = str(tmp_path / "x.meta.json")
    with open(gml, "w") as fh:
        fh.write("existe")
    with pytest.raises(FileExistsError):
        guardar_crudo(G, gml, meta)


def test_R1_04_conexa_devuelve_mismo_objeto():
    G = nx.MultiDiGraph([(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)])
    assert componente_mas_grande(G) is G  # R1-17: sin trabajo ni copia


def test_R1_04_filtra_a_la_mayor():
    G = nx.MultiDiGraph([(0, 1), (1, 0), (1, 2), (2, 1), (3, 4)])
    C = componente_mas_grande(G)
    assert set(C.nodes) == {0, 1, 2}
    assert nx.is_strongly_connected(C)


def test_R1_03_pesos_finitos_en_muestra():
    G = nx.MultiDiGraph()
    G.add_edge(0, 1, length=100.0, speed_kph=36.0)
    from quindio.red.pesos import verificar_pesos

    G[0][1][0]["distancia_m"] = 100.0
    G[0][1][0]["tiempo_viaje_s"] = tiempo_viaje_s(100.0, 36.0)
    assert verificar_pesos(G) == 1
    assert math.isclose(100.0 / G[0][1][0]["tiempo_viaje_s"], 10.0, rel_tol=1e-9)
