"""Segunda implementación propia para verificar Dijkstra (R2-06, EXP-07).

Bellman-Ford O(V·E): algoritmo distinto, mismo resultado en grafos sin pesos
negativos. Solo verificación; nunca en módulos medidos (GLOB-03).
"""
import math


def bellman_ford(n, ady, origen, destino):
    """Devuelve (tiempo, ruta). Inalcanzable: (inf, [])."""
    inf = math.inf
    dist = [inf] * n
    pred = [None] * n
    dist[origen] = 0
    for _ in range(n - 1):
        cambio = False
        for u in range(n):
            if dist[u] == inf:
                continue
            for v, peso in ady[u]:
                if v == u:
                    continue
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    pred[v] = u
                    cambio = True
        if not cambio:
            break
    if dist[destino] == inf:
        return inf, []
    ruta = [destino]
    while ruta[-1] != origen:
        ruta.append(pred[ruta[-1]])
    ruta.reverse()
    return dist[destino], ruta


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src"))
    from quindio.caminos.dijkstra import dijkstra_cola, dijkstra_lineal

    # Grafo dirigido a mano: 0->1 (4), 0->2 (1), 2->1 (2), 1->3 (1), 2->3 (6).
    # Óptimo 0->3 = 1+2+1 = 4 por [0, 2, 1, 3].
    ady = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 6)], []]
    for o, d in [(0, 3), (0, 1), (2, 3), (0, 0)]:
        t1, r1, _ = dijkstra_lineal(4, ady, o, d)
        t2, r2, _ = dijkstra_cola(4, ady, o, d)
        tb, rb = bellman_ford(4, ady, o, d)
        assert t1 == t2 == tb, (o, d, t1, t2, tb)
        print("par", o, d, "tiempo", t1, "rutas", r1, r2, rb)
    print("R2-06 OK: tres implementaciones coinciden")
