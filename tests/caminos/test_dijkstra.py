"""Pruebas de Dijkstra ×2 en grafos sintéticos (R2a, UT-05).

Nombres con ID de regla (REPO-03). Sin datos reales.
"""
import math

import pytest

from quindio.caminos.dijkstra import (
    dijkstra_cola,
    dijkstra_cola_completa,
    dijkstra_lineal,
)

VERSIONES = [dijkstra_lineal, dijkstra_cola]

# 0->1 (4), 0->2 (1), 2->1 (2), 1->3 (1), 2->3 (6). Óptimo 0->3 = 4.
ADY = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 6)], []]


@pytest.mark.parametrize("fn", VERSIONES)
def test_R2_01_parada_y_ruta(fn):
    t, ruta, _ = fn(4, ADY, 0, 3)
    assert t == 4
    assert ruta == [0, 2, 1, 3]


@pytest.mark.parametrize("fn", VERSIONES)
def test_R2_01_origen_destino(fn):
    t, ruta, _ = fn(4, ADY, 2, 2)
    assert t == 0
    assert ruta == [2]


@pytest.mark.parametrize("fn", VERSIONES)
def test_R2_03_conteo_explorados(fn):
    _, _, exp = fn(4, ADY, 0, 3)
    assert 1 <= exp <= 4


def test_R2_04_desempate_menor_indice():
    # 0->1 y 0->2 con peso 1; ambos llevan a 3 con peso 1: gana el índice 1.
    ady = [[(1, 1), (2, 1)], [(3, 1)], [(3, 1)], []]
    for fn in VERSIONES:
        t, ruta, _ = fn(4, ady, 0, 3)
        assert t == 2
        assert ruta == [0, 1, 3]


def test_R2_04_paralelas_y_lazos():
    ady = [[(0, 5), (1, 9), (1, 2)], [(2, 3)], []]
    for fn in VERSIONES:
        t, ruta, _ = fn(3, ady, 0, 2)
        assert t == 5  # 0->1 por la paralela mínima (2) + 1->2 (3)
        assert ruta == [0, 1, 2]


@pytest.mark.parametrize("fn", VERSIONES)
def test_R2_05_rechaza_pesos(fn):
    with pytest.raises(ValueError):
        fn(2, [[(1, -1)], []], 0, 1)
    with pytest.raises(ValueError):
        fn(2, [[(1, math.inf)], []], 0, 1)
    with pytest.raises(ValueError):
        fn(2, [[(1, math.nan)], []], 0, 1)
    with pytest.raises(TypeError):
        fn(2, [[(1, "x")], []], 0, 1)


def test_R2_06_mismos_tiempos_en_todos_los_pares():
    pares = [(o, d) for o in range(4) for d in range(4)]
    for o, d in pares:
        t1, _, _ = dijkstra_lineal(4, ADY, o, d)
        t2, _, _ = dijkstra_cola(4, ADY, o, d)
        assert t1 == t2 == t1  # igualdad exacta entre propios (DA-15)


def test_R2_06_caso_a_mano():
    # Diamante dirigido: 0->1 (2), 0->2 (5), 1->3 (5), 2->3 (1). Óptimo = 6.
    ady = [[(1, 2), (2, 5)], [(3, 5)], [(3, 1)], []]
    for fn in VERSIONES:
        t, ruta, _ = fn(4, ady, 0, 3)
        assert (t, ruta) == (6, [0, 2, 3])


def test_R2_11_completa_da_distancias_a_todos():
    dist, exp = dijkstra_cola_completa(4, ADY, 0)
    assert dist == [0, 3, 1, 4]
    assert exp == 4
    t, _, _ = dijkstra_cola(4, ADY, 0, 3)
    assert dist[3] == t


def test_R2_06_inalcanzable_sin_infinitos_falsos():
    ady = [[(1, 1)], [], []]
    for fn in VERSIONES:
        t, ruta, _ = fn(3, ady, 0, 2)
        assert t == math.inf
        assert ruta == []
