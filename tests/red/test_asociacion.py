"""Pruebas sintéticas de asociación y procesado (R1b, UT-04).

Nombres con ID de regla (REPO-03). Sin red real ni catálogo.
"""
import math

from quindio.red.asociacion import asociar, en_bbox, reportar_lejanos


def test_R1_06_vecino_mas_cercano_utm():
    puntos = [("P", 0.0, 0.0)]
    nodos = {10: (3.0, 4.0), 20: (6.0, 0.0)}
    assert asociar(puntos, nodos) == {"P": (10, 5.0)}


def test_R1_06_utm_difiere_de_grados():
    # P=(4.5,-75.6); A 0.001995° al este; B 0.002° al norte.
    # En grados: A más cerca. En metros UTM: B más cerca (flip por escala).
    from pyproj import Transformer

    trans = Transformer.from_crs("epsg:4326", "epsg:32618", always_xy=True)
    plat, plon = 4.5, -75.6
    alat, alon = 4.5, -75.6 + 0.001995
    blat, blon = 4.5 + 0.002, -75.6
    d_grados = lambda la, lo: math.hypot(la - plat, lo - plon)
    assert d_grados(alat, alon) < d_grados(blat, blon)
    ax, ay = trans.transform(alon, alat)
    bx, by = trans.transform(blon, blat)
    nodos = {1: (ax, ay), 2: (bx, by)}
    px, py = trans.transform(plon, plat)
    ganador, _ = asociar([("P", px, py)], nodos)["P"]
    assert ganador == 2


def test_R1_06_desempate_menor_id():
    puntos = [("P", 1.0, 0.0)]
    nodos = {50: (0.0, 0.0), 7: (2.0, 0.0)}
    nodo, d = asociar(puntos, nodos)["P"]
    assert (nodo, d) == (7, 1.0)


def test_R1_07_borde_500_estricto():
    asocs = {"a": (1, 500.0), "b": (2, 500.0001), "c": (3, 10.0)}
    assert reportar_lejanos(asocs) == ["b"]


def test_R1_07_ids_intactos():
    puntos = [("x", 0.0, 0.0), ("y", 1200.0, 0.0)]
    nodos = {3: (1.0, 0.0), 4: (600.0, 0.0)}
    asocs = asociar(puntos, nodos)
    assert set(asocs) == {"x", "y"}
    assert reportar_lejanos(asocs) == ["y"]


def test_R1_12_todos_en_bbox():
    puntos = [("P", 5.0, 5.0)]
    nodos = {1: (0.0, 0.0), 2: (10.0, 10.0)}
    assert en_bbox(puntos, nodos) == []
    assert en_bbox([("Q", 50.0, 5.0)], nodos) == ["Q"]
