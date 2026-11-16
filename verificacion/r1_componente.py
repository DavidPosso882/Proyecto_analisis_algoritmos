"""Checks independientes R1 (solo verificación; NetworkX permitido aquí).

- R1-01: el crudo recargado tiene V/E del metadato.
- R1-04: el resultado es fuertemente conexo y del tamaño de la mayor
  componente calculada de forma independiente.
Uso: .venv/bin/python verificacion/r1_componente.py
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import networkx as nx

RAIZ = Path(__file__).resolve().parents[1]
NOMBRES = ["departamento", "radio_2km", "radio_5km", "radio_10km", "radio_20km"]


def main():
    import osmnx

    from quindio.red.componente import componente_mas_grande

    for nombre in NOMBRES:
        G = osmnx.io.load_graphml(
            os.path.join(str(RAIZ / "data" / "crudo"), nombre + ".graphml"))
        with open(os.path.join(
                str(RAIZ / "data" / "crudo"), nombre + ".meta.json"), encoding="utf-8") as fh:
            meta = json.load(fh)
        assert (len(G.nodes), len(G.edges)) == (meta["nodos"], meta["aristas"]), nombre
        C = componente_mas_grande(G)
        assert nx.is_strongly_connected(C), nombre
        mayor = max(len(s) for s in nx.strongly_connected_components(G))
        assert len(C.nodes) == mayor, nombre
        print(f"{nombre} OK: crudo==metadato ({meta['nodos']}/{meta['aristas']}), "
              f"componente {len(C.nodes)} nodos (mayor={mayor})")
    print("R1-01/R1-04 OK")


if __name__ == "__main__":
    main()
