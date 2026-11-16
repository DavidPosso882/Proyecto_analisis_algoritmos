"""Verificación independiente R1-06/R1-12 (2º método + geodésica + bbox).

- Árbol KD (scipy, solo verificación) reproduce los nodos asociados.
- Distancia geodésica (pyproj.Geod) vs euclidiana UTM: tolerancia abs 2 m
  declarada (distorsión de escala UTM en el Quindío « 1 %).
- Mapa humano de coordenadas: tarea del grupo (GLOB-21).
Uso: .venv/bin/python verificacion/r1_asociacion.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

RAIZ = Path(__file__).resolve().parents[1]
TOL_M = 2.0


def main():
    import numpy as np
    from pyproj import Geod
    from scipy.spatial import KDTree

    from quindio.red.asociacion import (
        asociar,
        cargar_catalogo,
        en_bbox,
        proyectar_nodos,
        proyectar_puntos,
        reportar_lejanos,
    )
    from quindio.red.procesado import cargar_procesado

    proc = cargar_procesado(str(RAIZ / "data" / "procesado"))
    lugares = cargar_catalogo(str(RAIZ / "data" / "catalogo" / "catalogo.csv"))
    G = proc["grafo"]
    nodos_utm = proyectar_nodos(G)
    puntos_utm = proyectar_puntos(lugares)

    # (i) 2º método: KDTree coincide (empates documentados aparte)
    ids = sorted(nodos_utm)
    arbol = KDTree(np.array([nodos_utm[i] for i in ids]))
    asocs = asociar(puntos_utm, nodos_utm)
    for lid, x, y in puntos_utm:
        _, pos = arbol.query([x, y])
        assert asocs[lid][0] == ids[pos], lid

    # (ii) geodésica vs UTM dentro de la tolerancia
    geod = Geod(ellps="WGS84")
    por_id = {l["id"]: l for l in lugares}
    lon_nodo = {n: G.nodes[n]["x"] for n in G.nodes}
    lat_nodo = {n: G.nodes[n]["y"] for n in G.nodes}
    for lid, (nodo, d_utm) in asocs.items():
        l = por_id[lid]
        _, _, d_geo = geod.inv(l["lon"], l["lat"], lon_nodo[nodo], lat_nodo[nodo])
        assert abs(d_geo - d_utm) <= TOL_M, (lid, d_geo, d_utm)

    # (iii) bbox (se reporta, no se exige: DA-11 contempla lugares lejos de la
    # red vial; Acaime está 3.2 km al este del último nodo drive) + ids intactos
    fuera = en_bbox(puntos_utm, nodos_utm)
    print("fuera del bbox de la componente:", fuera)
    assert set(asocs) == {l["id"] for l in lugares}
    guardadas = {r["id"]: (int(r["nodo_id"]), float(r["distancia_m"]))
                 for r in proc["asociaciones"]}
    assert set(guardadas) == set(asocs)
    for lid in asocs:
        assert guardadas[lid][0] == asocs[lid][0]
        assert abs(guardadas[lid][1] - asocs[lid][1]) < 0.001
    n_lejanos = len(reportar_lejanos(asocs))
    print(f"R1-06/R1-12 OK: KDTree coincide, geodésica ±{TOL_M:.1f} m, "
          f"{len(asocs)} lugares, {n_lejanos} a >500 m")
    for lid in reportar_lejanos(asocs):
        print("  >500 m:", lid, f"{asocs[lid][1]:.1f} m")


if __name__ == "__main__":
    main()
