"""R1b: procesa el depto (pesos + componente + asociación + guardado).

Lee data/crudo/departamento.* y data/catalogo/catalogo.csv; escribe
data/procesado/ una sola vez (GLOB-17).
Uso: .venv/bin/python experimentos/r1/procesar.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.red.asociacion import (
    asociar,
    cargar_catalogo,
    proyectar_nodos,
    proyectar_puntos,
    reportar_lejanos,
)
from quindio.red.componente import componente_mas_grande
from quindio.red.pesos import aplicar_pesos, verificar_pesos
from quindio.red.procesado import guardar_procesado

RAIZ = Path(__file__).resolve().parents[2]


def main():
    import osmnx

    G = osmnx.io.load_graphml(str(RAIZ / "data" / "crudo" / "departamento.graphml"))
    aplicar_pesos(G)
    n_aristas = verificar_pesos(G)
    C = componente_mas_grande(G)
    lugares = cargar_catalogo(str(RAIZ / "data" / "catalogo" / "catalogo.csv"))
    asocs = asociar(proyectar_puntos(lugares), proyectar_nodos(C))
    meta = guardar_procesado(str(RAIZ / "data" / "procesado"), G, C, asocs)
    print(f"pesos en {n_aristas} aristas")
    print(f"antes V={meta['red_antes']['nodos']} E={meta['red_antes']['aristas']}")
    print(f"comp  V={meta['componente']['nodos']} E={meta['componente']['aristas']}")
    print("lejanos >500 m:", reportar_lejanos(asocs))
    print("PROCESADO-OK")


if __name__ == "__main__":
    main()
