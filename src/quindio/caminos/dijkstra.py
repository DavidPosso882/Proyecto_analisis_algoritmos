"""Dijkstra en dos versiones, implementación propia (R2a, UT-05).

Python puro, sin NumPy/NetworkX/SciPy/OSMnx/igraph (R2-13, GLOB-03).
`ady[i]` = lista de `(vecino, peso)` en orden de inserción; los índices son
contiguos 0..n-1 (anticipa R1-09). Ambas versiones comparten orden de
adyacencia, desempate por menor índice y mejora estricta (R2-04, DA-15).

Invariante (R2-14): al extraer un nodo, su distancia ya es óptima, porque todo
camino alternativo hacia él pasa por un nodo no extraído de distancia mayor o
igual. Por eso es correcto detenerse al extraer el destino. Condición: pesos
finitos y >= 0 (R2-05).
Complejidades con fuente (Cormen et al., *Introduction to Algorithms*, 3ra
ed., §24.3): versión lineal O(V²); versión con cola binaria O((V+E) log V)
(costo de `heapq` incluido según GLOB-04).
"""

import heapq
import math


def _validar(n, ady, origen, destino):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n debe ser entero positivo")
    if len(ady) != n:
        raise ValueError("ady debe tener n listas")
    for extremo in (origen, destino):
        if not isinstance(extremo, int) or not 0 <= extremo < n:
            raise ValueError("origen/destino fuera de rango")
    for u, vecinos in enumerate(ady):
        for v, peso in vecinos:
            if not isinstance(v, int) or not 0 <= v < n:
                raise ValueError("vecino fuera de rango")
            if isinstance(peso, bool) or not isinstance(peso, (int, float)):
                raise TypeError("peso debe ser numérico")
            if not math.isfinite(peso) or peso < 0:
                raise ValueError("pesos finitos y >= 0 (R2-05)")


def _reconstruir(pred, origen, destino):
    ruta = [destino]
    while ruta[-1] != origen:
        anterior = pred[ruta[-1]]
        if anterior is None:
            return []
        ruta.append(anterior)
    ruta.reverse()
    return ruta


def _relajar(u, ady, dist, pred):
    for v, peso in ady[u]:  # mismo orden en ambas versiones (R2-04)
        if v == u:  # sin lazos
            continue
        nuevo = dist[u] + peso
        if nuevo < dist[v]:  # mejora estricta; paralelas: vale la mínima
            dist[v] = nuevo
            pred[v] = u


def dijkstra_lineal(n, ady, origen, destino):
    """Dijkstra O(V²) con mínimo por recorrido lineal. Devuelve
    (tiempo, ruta, explorados). Inalcanzable: (inf, [], explorados)."""
    _validar(n, ady, origen, destino)
    inf = math.inf
    dist = [inf] * n
    pred = [None] * n
    visitado = [False] * n
    dist[origen] = 0
    explorados = 0
    for _ in range(n):
        u = -1
        mejor = inf
        for i in range(n):  # barrido lineal; empate: menor índice
            if not visitado[i] and dist[i] < mejor:
                mejor = dist[i]
                u = i
        if u == -1 or mejor == inf:
            break
        visitado[u] = True
        explorados += 1  # se cuenta al salir, una sola vez (R2-01)
        if u == destino:
            break
        _relajar(u, ady, dist, pred)
    if dist[destino] == inf:
        return inf, [], explorados
    return dist[destino], _reconstruir(pred, origen, destino), explorados


def dijkstra_cola(n, ady, origen, destino):
    """Dijkstra O((V+E) log V) con `heapq`. Misma interfaz que la lineal."""
    _validar(n, ady, origen, destino)
    inf = math.inf
    dist = [inf] * n
    pred = [None] * n
    sacado = [False] * n
    dist[origen] = 0
    explorados = 0
    cola = [(0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if d != dist[u] or sacado[u]:
            continue  # entrada obsoleta: no se cuenta (R2-01)
        sacado[u] = True
        explorados += 1
        if u == destino:
            break
        _relajar(u, ady, dist, pred)
        for v, peso in ady[u]:
            if v == u:
                continue
            if dist[u] + peso == dist[v] and pred[v] == u:
                heapq.heappush(cola, (dist[v], v))
    if dist[destino] == inf:
        return inf, [], explorados
    return dist[destino], _reconstruir(pred, origen, destino), explorados


def dijkstra_cola_completa(n, ady, origen):
    """Dijkstra con cola sin detenerse: devuelve (distancias, explorados).

    Para la matriz R2-11: una ejecución por origen. Sin predecesores.
    Inalcanzables quedan en inf (con la componente no ocurre: R1-10)."""
    _validar(n, ady, origen, origen)
    inf = math.inf
    dist = [inf] * n
    sacado = [False] * n
    dist[origen] = 0
    explorados = 0
    cola = [(0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if d != dist[u] or sacado[u]:
            continue
        sacado[u] = True
        explorados += 1
        for v, peso in ady[u]:
            if v == u:
                continue
            nuevo = dist[u] + peso
            if nuevo < dist[v]:
                dist[v] = nuevo
                heapq.heappush(cola, (nuevo, v))
    return dist, explorados
