"""Pruebas de fuerza bruta + Held-Karp en sintéticos asimétricos (R4a-exacto).

Nombres con ID de regla (REPO-03). Sin matriz real.
"""
import math
import random

import pytest

from quindio.recorrido.exactos import fuerza_bruta, held_karp, tamano_tabla

METODOS = [fuerza_bruta, held_karp]

# Asimétrica a mano: ir 0->1 cuesta 1 pero volver 1->0 cuesta 10 (R4-01).
# Óptimo desde 0: [0, 1, 2, 0] = 1 + 2 + 3 = 6; inverso [0, 2, 1, 0] = 4+5+10 = 19.
ASIM = [
    [0, 1, 4],
    [10, 0, 2],
    [3, 5, 0],
]


def costo(matriz, tour):
    return sum(matriz[a][b] for a, b in zip(tour, tour[1:]))  # noqa: RUF007 - mismo estilo que el medido


def test_R4_01_asimetrico_inverso_distinto():
    assert ASIM[0][1] != ASIM[1][0]
    tour_b, total_b, _ = fuerza_bruta(ASIM)
    assert (tour_b, total_b) == ([0, 1, 2, 0], 6)


@pytest.mark.parametrize("fn", METODOS)
def test_R4_04_recorrido_y_total(fn):
    tour, total, _ = fn(ASIM)
    assert tour[0] == tour[-1] == 0
    assert sorted(tour[:-1]) == [0, 1, 2]
    assert total == costo(ASIM, tour) == 6


def test_R4_02_bruta_enumera_todo():
    _, _, info = fuerza_bruta(ASIM)
    assert info["permutaciones"] == math.factorial(2)


def test_R4_19_cuenta_permutaciones_en_k_pequeno():
    rng = random.Random(42)
    for k in (4, 5, 6):
        m = [[0 if i == j else rng.randint(1, 20) for j in range(k)]
             for i in range(k)]
        _, _, info = fuerza_bruta(m)
        assert info["permutaciones"] == math.factorial(k - 1)


def test_R4_06_bruta_igual_hk_azar():
    rng = random.Random(42)
    for k in (3, 4, 5, 6):
        m = [[0 if i == j else rng.randint(1, 30) for j in range(k)]
             for i in range(k)]
        tour_b, total_b, _ = fuerza_bruta(m)
        tour_h, total_h, _ = held_karp(m)
        assert total_b == total_h
        assert costo(m, tour_b) == total_b
        assert costo(m, tour_h) == total_h


def test_R4_05_tabla():
    entradas, bytes_est = tamano_tabla(5)
    assert entradas == 4 * 16
    assert bytes_est == entradas * 8
    _, _, info = held_karp(ASIM)
    assert info["entradas_tabla"] == 2 * 4
