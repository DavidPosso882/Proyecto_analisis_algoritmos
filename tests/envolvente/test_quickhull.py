"""Pruebas de QuickHull entero + referencia (R3a, UT-07)."""
import random

from quindio.envolvente.quickhull import envolvente, preparar_enteros, redondear_half_up
from quindio.envolvente.referencia import referencia


def test_R3_01_enteros_dedup():
    pts, n = preparar_enteros([(0.2, 0.2), (0.2, 0.2), (1.6, 0.4)])
    assert (pts, n) == ([(0, 0), (2, 0)], 2)
    assert redondear_half_up(2.5) == 3  # .5 hacia arriba (DA-18)


def test_R3_03_bordes_no_son_vertices():
    cuadrado = [(0, 0), (4, 0), (4, 4), (0, 4),
                (2, 0), (4, 2), (2, 4), (0, 2), (1, 1)]
    assert sorted(envolvente(cuadrado)) == [(0, 0), (0, 4), (4, 0), (4, 4)]


def test_R3_06_degenerados_a_mano():
    assert envolvente([(0, 0), (1, 1), (2, 2), (3, 3)]) == [(0, 0), (3, 3)]
    assert envolvente([(5, 5)]) == [(5, 5)]
    assert envolvente([(1, 2), (1, 2)]) == [(1, 2)]


def test_R3_05_igual_scipy_azar():
    rng = random.Random(42)
    for talla in (20, 100, 500):
        pts = [(rng.randint(0, 1000), rng.randint(0, 1000)) for _ in range(talla)]
        assert set(envolvente(pts)) == referencia(pts)


def test_R3_05_igual_scipy_red():
    from quindio.red.asociacion import proyectar_nodos
    from quindio.red.procesado import cargar_procesado

    proc = cargar_procesado("data/procesado")
    nodos = proyectar_nodos(proc["grafo"])
    pts, n = preparar_enteros(nodos.values())
    assert n == 8803
    assert set(envolvente(pts)) == referencia(pts)
