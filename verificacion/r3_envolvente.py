"""Verificación independiente R3-13 (2º ángulo + Shapely + propiedades).

- Casos a mano: extremos, alineados, duplicados.
- Red real: propio vs SciPy (conjuntos) + Shapely.contains (contención).
- Propiedades enteras: giros estrictos a la izquierda y contención por
  semiplanos (sin float).
Uso: .venv/bin/python verificacion/r3_envolvente.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

RAIZ = Path(__file__).resolve().parents[1]


def giros_izq(hull):
    from quindio.envolvente.quickhull import cross

    n = len(hull)
    return [cross(hull[i], hull[(i + 1) % n], hull[(i + 2) % n]) for i in range(n)]


def contiene(hull, p):
    from quindio.envolvente.quickhull import cross

    n = len(hull)
    return all(cross(hull[i], hull[(i + 1) % n], p) >= 0 for i in range(n))


def main():
    from shapely.geometry import MultiPoint

    from quindio.envolvente.quickhull import envolvente, preparar_enteros
    from quindio.envolvente.referencia import referencia
    from quindio.red.asociacion import proyectar_nodos
    from quindio.red.procesado import cargar_procesado

    assert all(g > 0 for g in giros_izq(envolvente([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)])))
    assert envolvente([(0, 0), (1, 1), (2, 2)]) == [(0, 0), (2, 2)]
    proc = cargar_procesado(str(RAIZ / "data" / "procesado"))
    pts, n = preparar_enteros(proyectar_nodos(proc["grafo"]).values())
    hull = envolvente(pts)
    assert set(hull) == referencia(pts)
    giros = giros_izq(hull)
    assert len(hull) == 14 and all(g > 0 for g in giros)
    assert all(contiene(hull, p) for p in pts)
    from shapely.geometry import Point

    shape = MultiPoint(pts).convex_hull
    assert all(shape.covers(Point(p)) for p in pts)
    assert len(shape.exterior.coords) - 1 == len(hull)
    assert all(shape.covers(Point(v)) for v in hull)
    print(f"R3-13 OK: red n={n} vértices={len(hull)}, giros izq estrictos, "
          "contención entera + Shapely OK")


if __name__ == "__main__":
    main()
