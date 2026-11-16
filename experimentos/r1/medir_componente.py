"""R1-05: mide la llamada R1-04 sobre cada red ya cargada (UT-01).

Pesos aplicados antes (fuera de región, EXP-02). 5 filas con etiquetas del
Anexo. Reanudable (EXP-16). Uso: .venv/bin/python experimentos/r1/medir_componente.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.medicion.arnes import (
    guardar_incremental,
    ids_completados,
    medir,
)
from quindio.red.componente import componente_mas_grande
from quindio.red.descarga import (
    ETIQUETA_DEPTO,
    ETIQUETAS_RADIO,
    RADIOS_M,
)
from quindio.red.pesos import aplicar_pesos, verificar_pesos

RAIZ = Path(__file__).resolve().parents[2]
NOMBRES = {2000: "radio_2km", 5000: "radio_5km",
           10000: "radio_10km", 20000: "radio_20km"}
SALIDA = RAIZ / "resultados" / "r1" / "t_componente.csv"


def fn_componente(grafo):
    """Nivel módulo: picklable para spawn. Solo la llamada R1-04."""
    C = componente_mas_grande(grafo)
    return None, {"V": len(grafo.nodes), "E": len(grafo.edges),
                  "V_mas_E": len(grafo.nodes) + len(grafo.edges),
                  "V_comp": len(C.nodes), "E_comp": len(C.edges)}


def medir_red(G, id_medicion, semilla):
    return medir(fn_componente, (G,), id_medicion=id_medicion, semilla=semilla,
                 metodo_verificacion="verificacion/r1_componente.py (NetworkX independiente)",
                 verificacion=lambda: True)


def main():
    import osmnx

    from quindio.medicion.arnes import derivar_semilla

    hechos = ids_completados(str(SALIDA))
    trabajos = [("departamento", ETIQUETA_DEPTO, 0)]
    trabajos += [(NOMBRES[r], ETIQUETAS_RADIO[r], i + 1)
                 for i, r in enumerate(RADIOS_M)]
    for nombre, etiqueta, idx in trabajos:
        if etiqueta in hechos:
            print(etiqueta, "ya medida, se omite")
            continue
        G = osmnx.io.load_graphml(
            os.path.join(str(RAIZ / "data" / "crudo"), nombre + ".graphml"))
        aplicar_pesos(G)
        n_aristas = verificar_pesos(G)
        fila = medir_red(G, etiqueta, derivar_semilla(100 + idx))
        fila["info"]["n_aristas_con_pesos"] = n_aristas
        guardar_incremental(str(SALIDA), fila)
        info = fila["info"]
        med = f"mediana_ms={fila['mediana_ms']:.1f}" if fila["mediana_ms"] else "sin tiempo"
        print(f"{etiqueta} {fila['estado']} {med} V={info['V']} E={info['E']} V+E={info['V_mas_E']}")
    print("CSV:", SALIDA)


if __name__ == "__main__":
    main()
