"""Descarga única autorizada DA-07/GLOB-15: depto + 4 radios a data/crudo/.

Uso: .venv/bin/python experimentos/r1/descargar.py
Falla si los destinos existen (GLOB-17). No re-ejecutar sin autorización.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.red.descarga import descargar_todo

RAIZ = Path(__file__).resolve().parents[2]


def main():
    salidas = descargar_todo(str(RAIZ / "data" / "crudo"))
    for nombre, info in salidas.items():
        print(f"{nombre} nodos={info['nodos']} aristas={info['aristas']}")


if __name__ == "__main__":
    main()
