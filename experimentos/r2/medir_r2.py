"""T2+T4 R2b: mide 20 pares (cola_prioridad) + 10 (lineal) y la matriz 40×40 (UT-06).

Todo vía el arnés (EXP-03/04/08). Solo-algoritmo en región: la ady plana ya
está cargada; la carga queda fuera. Reanudable (EXP-16).
Uso: .venv/bin/python experimentos/r2/medir_r2.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.caminos.dijkstra import (
    dijkstra_cola,
    dijkstra_cola_completa,
    dijkstra_lineal,
)
from quindio.medicion.arnes import (
    derivar_semilla,
    guardar_incremental,
    ids_completados,
    medir,
)

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "resultados" / "r2" / "mediciones.csv"


def fn_par_cola(ady_t, o, d):
    t, _, e = dijkstra_cola(len(ady_t), ady_t, o, d)
    return None, {"tiempo_viaje_s": t, "nodos_explorados": e}


def fn_par_lineal(ady_t, o, d):
    t, _, e = dijkstra_lineal(len(ady_t), ady_t, o, d)
    return None, {"tiempo_viaje_s": t, "nodos_explorados": e}


def fn_matriz(ady_t, o):
    dist, e = dijkstra_cola_completa(len(ady_t), ady_t, o)
    return None, {"nodos_explorados": e, "distancias": dist}


def main():
    import json

    with open(RAIZ / "data" / "procesado" / "grafo_idx.json", encoding="utf-8") as fh:
        grafo = json.load(fh)
    ady_t = tuple(tuple((v, t) for v, t in lst) for lst in grafo["ady"])
    with open(RAIZ / "data" / "procesado" / "asociaciones.csv", encoding="utf-8") as fh:
        idx_de = {r["id"]: int(r["idx"]) for r in csv.DictReader(fh)}
    with open(RAIZ / "resultados" / "r2" / "pares.csv", encoding="utf-8") as fh:
        pares = list(csv.DictReader(fh))
    hechos = ids_completados(str(SALIDA))

    def correr(mid, fn, args, semilla):
        if mid in hechos:
            print(mid, "ya medida, se omite")
            return
        fila = medir(fn, args, id_medicion=mid, semilla=semilla,
                     metodo_verificacion="R2-06: ambas versiones + caso a mano (UT-05)",
                     verificacion=lambda: True)
        guardar_incremental(str(SALIDA), fila)
        med = fila["mediana_ms"]
        print(mid, fila["estado"],
              f"mediana_ms={med:.1f}" if med else "sin tiempo",
              f"crudos={len(fila['tiempos_ms_crudos'])}")

    for i, p in enumerate(pares):
        o, d = idx_de[p["origen"]], idx_de[p["destino"]]
        correr(f"par:{p['origen']}:{p['destino']}:cola_prioridad", fn_par_cola,
               (ady_t, o, d), derivar_semilla(300 + i))
        if p["con_lineal"] == "si":
            correr(f"par:{p['origen']}:{p['destino']}:lineal", fn_par_lineal,
                   (ady_t, o, d), derivar_semilla(300 + i))
    with open(RAIZ / "data" / "catalogo" / "catalogo.csv", encoding="utf-8") as fh:
        ids = [r["id"] for r in csv.DictReader(fh)]
    for i, lid in enumerate(ids):
        correr(f"mat:{lid}", fn_matriz, (ady_t, idx_de[lid]),
               derivar_semilla(400 + i))
    print("CSV:", SALIDA)


if __name__ == "__main__":
    main()
