"""Verificación R2b con NetworkX por fila (permitido aquí, GLOB-03).

Compara las distancias de precisión completa (filas mat:* de mediciones.csv)
contra single_source_dijkstra_path_length (tol relativa DA-15 = 1e-9) y
comprueba que matriz_tiempos.csv == redondeo a ms + esquema (header==ids,
diagonal 0, sin infinitos).
Uso: .venv/bin/python verificacion/r2_matriz.py
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

RAIZ = Path(__file__).resolve().parents[1]
TOL_REL = 1e-9


def main():
    import sys

    import networkx as nx
    import osmnx

    csv.field_size_limit(sys.maxsize)
    with open(RAIZ / "data" / "catalogo" / "catalogo.csv", encoding="utf-8") as fh:
        ids = [r["id"] for r in csv.DictReader(fh)]
    with open(RAIZ / "data" / "procesado" / "asociaciones.csv", encoding="utf-8") as fh:
        asocs = list(csv.DictReader(fh))
    nodo_de = {r["id"]: int(r["nodo_id"]) for r in asocs}
    idx_de = {r["id"]: int(r["idx"]) for r in asocs}
    with open(RAIZ / "resultados" / "r2" / "mediciones.csv", encoding="utf-8") as fh:
        dist_de = {}
        for r in csv.DictReader(fh):
            if r["id_medicion"].startswith("mat:"):
                info = json.loads(r["info"])
                assert r["estado"] == "ok"
                dist_de[r["id_medicion"].split(":")[1]] = info["distancias"]
    assert set(dist_de) == set(ids)
    G = osmnx.io.load_graphml(str(RAIZ / "data" / "procesado" / "componente.graphml"))
    for _, _, _, d in G.edges(keys=True, data=True):  # GraphML trae str
        d["tiempo_viaje_s"] = float(d["tiempo_viaje_s"])
    for lid in ids:
        largos = nx.single_source_dijkstra_path_length(
            G, nodo_de[lid], weight="tiempo_viaje_s")
        for otro in ids:
            esperado = largos[nodo_de[otro]]
            obtenido = dist_de[lid][idx_de[otro]]
            assert abs(obtenido - esperado) <= TOL_REL * max(1.0, abs(esperado)), (lid, otro)
    with open(RAIZ / "resultados" / "r2" / "matriz_tiempos.csv", encoding="utf-8") as fh:
        rdr = csv.reader(fh)
        assert next(rdr) == ["id"] + ids
        n = 0
        for fila, lid in zip(rdr, ids):
            assert fila[0] == lid
            for j, otro in enumerate(ids):
                assert fila[1 + j] == f"{dist_de[lid][idx_de[otro]]:.3f}", (lid, otro)
                assert float(fila[1 + j]) != float("inf")
            assert fila[1 + ids.index(lid)] == "0.000"
            n += 1
        assert n == 40
    print("R2-11 OK: 40 filas coinciden con NetworkX (tol 1e-9); CSV == redondeo a ms")


if __name__ == "__main__":
    main()
