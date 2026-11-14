"""Referencia con scipy.spatial.ConvexHull (R3-05).

Módulo separado: única excepción que permite SciPy fuera de verificación
(ENUNCIADO §5 R3.1/R3.2; GLOB-03). Compara CONJUNTOS de vértices, no índices.
"""
import numpy as np
from scipy.spatial import ConvexHull


def referencia(puntos_enteros):
    """Devuelve el conjunto de vértices (x, y) según SciPy."""
    arr = np.array(sorted(set(puntos_enteros)), dtype=np.int64)
    if len(arr) <= 1:
        return set(map(tuple, arr.tolist()))
    casco = ConvexHull(arr)
    return set(map(tuple, arr[casco.vertices].tolist()))


def version_scipy():
    """Algoritmo+lenguaje+versión para el informe (R3-10)."""
    import scipy

    return {"biblioteca": "scipy.spatial.ConvexHull", "version": scipy.__version__,
            "algoritmo": "Qhull (Barber et al.): https://qhull.org",
            "lenguaje": "C (vía Qhull), interfaz Python"}
