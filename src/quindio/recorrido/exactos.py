"""TSP asimétrico exacto: fuerza bruta + Held-Karp (R4a-exacto, UT-09 parcial).

Python puro: solo builtins + math en medidos (DA-21, R4-17/19).
Costo con celdas dirigidas matriz[i][j] (R4-01). Ambos devuelven
(recorrido, total, info): recorrido empieza y termina en la partida (R4-04).
Subestructura y recurrencia: specs/R4.md, Spec R4a-exacto (R4-03).
Complejidades con fuente (Bellman 1962, JACM 9(1); Held y Karp 1962,
J. SIAM 10(1)): bruta O(k!) tiempo / O(k) memoria; Held-Karp O(k²·2^k)
tiempo / O(k·2^k) memoria (R4-15).
"""

import math


def _validar(matriz, partida):
    k = len(matriz)
    if k < 1:
        raise ValueError("matriz vacía")
    if not isinstance(partida, int) or not 0 <= partida < k:
        raise ValueError("partida fuera de rango")
    for fila in matriz:
        if len(fila) != k:
            raise ValueError("matriz no cuadrada")
        for c in fila:
            if isinstance(c, bool) or not isinstance(c, (int, float)):
                raise TypeError("costos numéricos")
            if not math.isfinite(c) or c < 0:
                raise ValueError("costos finitos y >= 0")
    return k


def _reordenar(matriz, partida):
    """Pone la partida como índice 0; devuelve (matriz_reord, mapa_inv)."""
    k = len(matriz)
    orden = [partida] + [i for i in range(k) if i != partida]
    reord = [[matriz[i][j] for j in orden] for i in orden]
    return reord, orden


def _permutaciones_propias(elementos):
    """Generador de permutaciones propio (R4-02). Sin poda ni memo."""
    if len(elementos) <= 1:
        yield list(elementos)
        return
    for i in range(len(elementos)):
        resto = elementos[:i] + elementos[i + 1:]
        for perm in _permutaciones_propias(resto):
            yield [elementos[i]] + perm


def fuerza_bruta(matriz, partida=0):
    """Todas las permutaciones desde la partida (R4-02). Sin poda ni memo."""
    k = _validar(matriz, partida)
    if k == 1:
        return [partida, partida], 0, {"permutaciones": 1}
    reord, orden = _reordenar(matriz, partida)
    resto = list(range(1, k))
    mejor_total = math.inf
    mejor_tour = None
    n_enum = 0
    for perm in _permutaciones_propias(resto):
        n_enum += 1
        total = reord[0][perm[0]]
        for a, b in zip(perm, perm[1:]):  # noqa: RUF007 - DA-21: módulo medido sin libs extra
            total += reord[a][b]
        total += reord[perm[-1]][0]
        if total < mejor_total:  # mejora estricta: primer óptimo gana
            mejor_total = total
            mejor_tour = [0] + perm + [0]
    tour = [orden[i] for i in mejor_tour]
    return tour, mejor_total, {"permutaciones": n_enum}


def tamano_tabla(k):
    """(entradas, bytes_est) de la tabla HK para k lugares (R4-05)."""
    m = max(k - 1, 0)
    entradas = m * (1 << m)
    return entradas, entradas * 8


def held_karp(matriz, partida=0):
    """Held-Karp DP sobre subconjuntos (R4-02). Devuelve (tour, total, info)."""
    k = _validar(matriz, partida)
    if k == 1:
        return [partida, partida], 0, {"entradas_tabla": 0}
    reord, orden = _reordenar(matriz, partida)
    m = k - 1
    inf = math.inf
    dp = [[inf] * m for _ in range(1 << m)]
    padre = [[-1] * m for _ in range(1 << m)]
    for j in range(m):
        dp[1 << j][j] = reord[0][j + 1]
    for mask in range(1 << m):
        for j in range(m):
            if not (mask & (1 << j)) or dp[mask][j] == inf:
                continue
            for h in range(m):
                if mask & (1 << h):
                    continue
                nuevo = dp[mask][j] + reord[j + 1][h + 1]
                if nuevo < dp[mask | (1 << h)][h]:
                    dp[mask | (1 << h)][h] = nuevo
                    padre[mask | (1 << h)][h] = j
    completa = (1 << m) - 1
    mejor_total = inf
    mejor_fin = -1
    for j in range(m):
        total = dp[completa][j] + reord[j + 1][0]
        if total < mejor_total:
            mejor_total = total
            mejor_fin = j
    camino = []
    mask, j = completa, mejor_fin
    while True:
        camino.append(j + 1)
        anterior = padre[mask][j]
        mask ^= 1 << j
        if mask == 0:
            break
        j = anterior
    camino.reverse()
    tour = [orden[i] for i in [0] + camino + [0]]
    entradas, _ = tamano_tabla(k)
    return tour, mejor_total, {"entradas_tabla": entradas}
