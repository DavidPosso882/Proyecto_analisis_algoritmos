"""Completa los 4 radios pendientes (mismo lote DA-07; el depto ya está).

Omite archivos existentes (GLOB-17). Sale 0 solo si los 4 quedan listos.
Uso: .venv/bin/python experimentos/r1/descargar_radios.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.red.descarga import (
    CENTRO_ARMENIA,
    RADIOS_M,
    guardar_crudo,
)

RAIZ = Path(__file__).resolve().parents[2]
NOMBRES = {2000: "radio_2km", 5000: "radio_5km",
           10000: "radio_10km", 20000: "radio_20km"}


def main():
    import osmnx

    dir_crudo = str(RAIZ / "data" / "crudo")
    for radio in RADIOS_M:
        nombre = NOMBRES[radio]
        graphml = os.path.join(dir_crudo, f"{nombre}.graphml")
        meta_path = os.path.join(dir_crudo, f"{nombre}.meta.json")
        if os.path.exists(graphml) and os.path.exists(meta_path):
            print(nombre, "ya existe, se omite")
            continue
        G = osmnx.graph.graph_from_point(
            CENTRO_ARMENIA, dist=radio, dist_type="bbox", network_type="drive")
        meta = guardar_crudo(G, graphml, meta_path)
        print(f"{nombre} nodos={meta['nodos']} aristas={meta['aristas']}")
    print("RADIOS-OK")


if __name__ == "__main__":
    main()
