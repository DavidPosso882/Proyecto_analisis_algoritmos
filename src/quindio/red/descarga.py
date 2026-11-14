"""Descarga única OSMnx + crudo + metadato (R1-01, DA-07, DA-08).

Parámetros firmados (DA-08): `network_type="drive"` en las 5 redes, resto
defaults de osmnx 2.1.1 (simplify=True, retain_all=False,
dist_type="bbox"), todos en el metadato. «Radio» = bbox de `dist` metros por
lado desde el centro (R1-19, verificado en el código instalado).
Escribe en `data/crudo/` una sola vez: si el destino existe, falla (GLOB-17).
"""
import datetime
import json
import os
import platform
from datetime import UTC

LUGAR_DEPTO = "Quindío, Colombia"
CENTRO_ARMENIA = (4.53247, -75.67298)  # plaza de Bolívar, catálogo C01
RADIOS_M = [2000, 5000, 10000, 20000]
ETIQUETAS_RADIO = {
    2000: "Radio de 2 km",
    5000: "Radio de 5 km",
    10000: "Radio de 10 km",
    20000: "Radio de 20 km",
}
ETIQUETA_DEPTO = "Departamento completo"


def parametros_descarga():
    """Parámetros exactos registrados en el metadato (DA-08, R1-14)."""
    import osmnx

    return {
        "lugar_departamento": LUGAR_DEPTO,
        "network_type": "drive",
        "dist_type": "bbox",
        "simplify": True,
        "retain_all": False,
        "truncate_by_edge": False,
        "centro_armenia_latlon": list(CENTRO_ARMENIA),
        "radios_m": RADIOS_M,
        "osmnx": osmnx.__version__,
    }


def construir_metadato(nodos, aristas, origen="descarga"):
    """Metadato R1-01 (puro, testeable sin red)."""
    import networkx
    import osmnx

    return {
        "fecha_descarga": datetime.datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "osmnx": osmnx.__version__,
        "networkx": networkx.__version__,
        "parametros": parametros_descarga(),
        "origen": origen,
        "nodos": nodos,
        "aristas": aristas,
    }


def validar_metadato(meta):
    """Prueba de esquema R1-01: campos presentes y no vacíos."""
    for clave in ("fecha_descarga", "python", "osmnx", "networkx",
                  "parametros", "origen", "nodos", "aristas"):
        assert clave in meta and meta[clave] not in (None, "", {}), clave
    assert meta["nodos"] > 0 and meta["aristas"] > 0


def guardar_crudo(G, path_graphml, path_meta, origen="descarga"):
    """Guarda el grafo crudo sin modificar + metadato. Falla si existe."""
    import osmnx

    for path in (path_graphml, path_meta):
        if os.path.exists(path):
            raise FileExistsError(f"GLOB-17: {path} ya existe, no se sobrescribe")
    osmnx.io.save_graphml(G, filepath=path_graphml)
    meta = construir_metadato(len(G.nodes), len(G.edges), origen)
    validar_metadato(meta)
    with open(path_meta, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, sort_keys=True)
    return meta


def descargar_todo(dir_crudo):
    """LA descarga única autorizada (DA-07): depto + 4 radios. Devuelve dict."""
    import osmnx

    os.makedirs(dir_crudo, exist_ok=True)
    salidas = {}
    redes = [
        ("departamento", None),
        ("radio_2km", 2000),
        ("radio_5km", 5000),
        ("radio_10km", 10000),
        ("radio_20km", 20000),
    ]
    for nombre, radio in redes:
        graphml = os.path.join(dir_crudo, f"{nombre}.graphml")
        meta_path = os.path.join(dir_crudo, f"{nombre}.meta.json")
        if radio is None:
            G = osmnx.graph.graph_from_place(
                LUGAR_DEPTO, network_type="drive")
        else:
            G = osmnx.graph.graph_from_point(
                CENTRO_ARMENIA, dist=radio, dist_type="bbox",
                network_type="drive")
        meta = guardar_crudo(G, graphml, meta_path)
        salidas[nombre] = {"nodos": meta["nodos"], "aristas": meta["aristas"]}
    return salidas
