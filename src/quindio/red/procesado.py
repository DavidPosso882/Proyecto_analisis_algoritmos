"""Grafo procesado: guarda y carga sin descargar (R1-08, R1-09).

Guarda: componente.graphml, metadato.json (V/E antes/después, fecha,
versiones, parámetros, origen), asociaciones.csv, indices.json (nodo→idx
contiguo biyectivo) y grafo_idx.json (estructuras planas para R2-R4).
La carga no invoca descarga (solo lectura de disco).
"""
import csv
import datetime
import json
import os
import platform

ARCHIVOS = ("componente.graphml", "metadato.json", "asociaciones.csv",
            "indices.json", "grafo_idx.json")


def guardar_procesado(dir_proc, G_antes, G_comp, asociaciones, origen="descarga"):
    """Guarda todo; falla si algún destino existe (GLOB-17)."""
    import osmnx
    from osmnx.io import save_graphml

    os.makedirs(dir_proc, exist_ok=True)
    for nombre in ARCHIVOS:
        path = os.path.join(dir_proc, nombre)
        if os.path.exists(path):
            raise FileExistsError(f"GLOB-17: {path} ya existe")
    save_graphml(G_comp, filepath=os.path.join(dir_proc, "componente.graphml"))
    nodos_ordenados = sorted(G_comp.nodes)
    idx_de = {n: i for i, n in enumerate(nodos_ordenados)}
    ady = []
    for n in nodos_ordenados:
        vecinos = []
        for _, v, datos in G_comp.out_edges(n, data=True):
            vecinos.append([idx_de[v], float(datos["tiempo_viaje_s"])])
        ady.append(vecinos)
    with open(os.path.join(dir_proc, "indices.json"), "w", encoding="utf-8") as fh:
        json.dump({"nodo_a_idx": idx_de,
                   "idx_a_nodo": nodos_ordenados}, fh)
    with open(os.path.join(dir_proc, "grafo_idx.json"), "w", encoding="utf-8") as fh:
        json.dump({"n": len(nodos_ordenados), "ady": ady}, fh)
    with open(os.path.join(dir_proc, "asociaciones.csv"), "w", newline="",
              encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "nodo_id", "distancia_m", "idx"])
        for lid in sorted(asociaciones):
            nodo, dist = asociaciones[lid]
            writer.writerow([lid, nodo, f"{dist:.3f}", idx_de[nodo]])
    meta = {
        "fecha": datetime.datetime.now(datetime.UTC).isoformat(),
        "python": platform.python_version(),
        "origen": origen,
        "red_antes": {"nodos": len(G_antes.nodes), "aristas": len(G_antes.edges)},
        "componente": {"nodos": len(G_comp.nodes), "aristas": len(G_comp.edges)},
    }
    try:
        meta["osmnx"] = osmnx.__version__
    except AttributeError:
        pass
    with open(os.path.join(dir_proc, "metadato.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, sort_keys=True)
    return meta


def cargar_procesado(dir_proc):
    """Carga desde disco sin descargar (R1-08)."""
    from osmnx.io import load_graphml

    with open(os.path.join(dir_proc, "indices.json"), encoding="utf-8") as fh:
        indices = json.load(fh)
    # JSON serializa las claves int como str: se restauran los ids de nodo.
    indices = {"nodo_a_idx": {int(k): v for k, v in indices["nodo_a_idx"].items()},
               "idx_a_nodo": indices["idx_a_nodo"]}
    with open(os.path.join(dir_proc, "grafo_idx.json"), encoding="utf-8") as fh:
        grafo = json.load(fh)
    with open(os.path.join(dir_proc, "asociaciones.csv"), encoding="utf-8") as fh:
        asocs = list(csv.DictReader(fh))
    with open(os.path.join(dir_proc, "metadato.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    G = load_graphml(os.path.join(dir_proc, "componente.graphml"))
    # GraphML devuelve attrs como str: se normalizan los pesos a float.
    for _, _, _, datos in G.edges(keys=True, data=True):
        datos["distancia_m"] = float(datos["distancia_m"])
        datos["tiempo_viaje_s"] = float(datos["tiempo_viaje_s"])
    return {"grafo": G, "indices": indices, "ady": grafo,
            "asociaciones": asocs, "metadato": meta}
