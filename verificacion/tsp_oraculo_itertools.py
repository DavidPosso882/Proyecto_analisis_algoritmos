"""Oráculo con itertools para verificar los exactos (R4-06).

Solo verificación; itertools prohibido en módulos medidos (DA-21).
"""
import itertools
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from quindio.recorrido.exactos import fuerza_bruta, held_karp


def costo(matriz, tour):
    return sum(matriz[a][b] for a, b in itertools.pairwise(tour))


def oraculo(matriz, partida=0):
    resto = [i for i in range(len(matriz)) if i != partida]
    mejor = (math.inf, None)
    for perm in itertools.permutations(resto):
        tour = [partida] + list(perm) + [partida]
        total = costo(matriz, tour)
        if total < mejor[0]:
            mejor = (total, tour)
    return mejor


def matriz_azar(k, semilla):
    rng = random.Random(semilla)
    return [[0 if i == j else rng.randint(1, 50) for j in range(k)]
            for i in range(k)]


if __name__ == "__main__":
    for k in (4, 5, 6, 7):
        for s in (42, 43):
            m = matriz_azar(k, s)
            total_or, _ = oraculo(m)
            tour_b, total_b, _ = fuerza_bruta(m)
            tour_h, total_h, _ = held_karp(m)
            assert total_b == total_or, (k, s)
            assert total_h == total_or, (k, s)
            assert costo(m, tour_b) == total_b
            assert costo(m, tour_h) == total_h
            print("k", k, "semilla", s, "óptimo", total_or, "OK")
    print("R4-06 OK: bruta y HK coinciden con el oráculo")
