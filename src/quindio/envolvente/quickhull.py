"""QuickHull con aritmética entera exacta (R3a, UT-07; DA-12 confirmado).

Solo enteros Python (exactos, sin cota): cross para giros y distancias;
sin float/div/sqrt/trig en predicados (R3-02). Colineales sobre los lados no
son vértices (R3-03, comparación estricta). Degenerados: si todos colineales,
los dos extremos distintos (DA-18). Recurrencia y fuente
(Barber-Dobkin-Huhdanpaa 1996): specs/R3.md, Spec R3a (R3-04).
"""
import math


def cross(o, a, b):
    """Producto cruzado (a-o) x (b-o): >0 giro izq, <0 der, ==0 colineal."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def redondear_half_up(x):
    """Al entero más cercano; .5 hacia arriba (DA-18, documentado)."""
    return math.floor(x + 0.5)


def preparar_enteros(puntos_xy):
    """UTM float → enteros half-up + dedup. Devuelve (lista, n_tras_dedup).

    `n` reportado = tras deduplicar (DA-18); se informa además `generados`.
    """
    enteros = sorted({(redondear_half_up(x), redondear_half_up(y))
                      for x, y in puntos_xy})
    return enteros, len(enteros)


def _lado(pts, a, b):
    """Puntos estrictamente a la izquierda del segmento dirigido a→b."""
    return [p for p in pts if cross(a, b, p) > 0]


def _buscar(pts, a, b):
    """QuickHull sobre el semicaso: puntos a la izq de a→b (sin a ni b).

    Devuelve los vértices entre a y b (excluidos), en orden.
    """
    if not pts:
        return []
    c = max(pts, key=lambda p: abs(cross(a, b, p)))
    izq_ac = _lado([p for p in pts if p != c], a, c)
    izq_cb = _lado([p for p in pts if p != c], c, b)
    return _buscar(izq_ac, a, c) + [c] + _buscar(izq_cb, c, b)


def envolvente(puntos):
    """Envolvente convexa: lista de vértices CCW sin repetir el primero.

    `puntos`: iterable de (x, y) enteros (idealmente ya deduplicados).
    Colineales en bordes excluidos (R3-03); conjunto degenerado → extremos.
    """
    pts = sorted(set(puntos))
    if len(pts) <= 1:
        return list(pts)
    # Todos colineales: extremos distintos (DA-18).
    a0, b0 = pts[0], pts[-1]
    if all(cross(a0, b0, p) == 0 for p in pts):
        return [a0] if a0 == b0 else [a0, b0]
    izq = min(pts)
    der = max(pts)
    arriba = _lado(pts, izq, der)
    abajo = _lado(pts, der, izq)
    # CCW desde izq: baja por abajo hasta der y vuelve por arriba; así todo
    # giro consecutivo es estricto a la izquierda (verificación R3-13).
    baja = list(reversed(_buscar(abajo, der, izq)))
    sube = list(reversed(_buscar(arriba, izq, der)))
    return [izq] + baja + [der] + sube
