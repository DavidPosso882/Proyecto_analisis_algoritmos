"""Heurística voraz: vecino más cercano dirigido (R4-10, DA-13).

Desde la partida, ir siempre al lugar no visitado de menor tiempo e ir;
al final regresar a la partida. Desempate por menor índice. Constructiva
pura: sin mejoras no voraces. Python puro (DA-21).
"""
import math


def vecino_mas_cercano(matriz, partida=0):
    """Devuelve (recorrido, total, info). Recorrido empieza y termina en partida."""
    k = len(matriz)
    if k < 1:
        raise ValueError("matriz vacía")
    if not isinstance(partida, int) or not 0 <= partida < k:
        raise ValueError("partida fuera de rango")
    visitado = [False] * k
    visitado[partida] = True
    tour = [partida]
    total = 0
    actual = partida
    for _ in range(k - 1):
        mejor, mejor_t = -1, math.inf
        for j in range(k):  # orden fijo: el menor índice gana empates
            if not visitado[j] and matriz[actual][j] < mejor_t:
                mejor, mejor_t = j, matriz[actual][j]
        visitado[mejor] = True
        tour.append(mejor)
        total += mejor_t
        actual = mejor
    total += matriz[actual][partida]
    tour.append(partida)
    return tour, total, {"metodo": "vecino_mas_cercano"}
