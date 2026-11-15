"""R4.5: ejemplo de por qué el voraz no siempre encuentra el óptimo.

Toma una instancia ya medida de la serie «calidad» (por defecto k = 5,
instancia 2) y, solo con archivos de ``resultados/`` (GLOB-08), imprime:

- la submatriz de tiempos de la instancia, en minutos;
- cada elección del voraz con las alternativas que tenía en ese momento;
- los dos recorridos tramo a tramo y la diferencia total.

No vuelve a medir ni a resolver: los recorridos salen de
``resultados/r4/calidad_exactos.csv`` y los tiempos de
``resultados/r2/matriz_tiempos.csv``.

Uso: python experimentos/r4/ejemplo_voraz.py [k] [instancia]
"""
import csv
import json
import sys
from itertools import pairwise
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
R4 = RAIZ / "resultados" / "r4"
PARTIDA = "C01"


def main():
    k = sys.argv[1] if len(sys.argv) > 1 else "5"
    inst = sys.argv[2] if len(sys.argv) > 2 else "2"
    csv.field_size_limit(2**31 - 1)
    with open(RAIZ / "resultados" / "r2" / "matriz_tiempos.csv", newline="", encoding="utf-8") as fh:
        filas = list(csv.reader(fh))
    ids = filas[0][1:]
    m = {f[0]: {ids[j]: float(x) / 60 for j, x in enumerate(f[1:])} for f in filas[1:]}
    with open(R4 / "instancias.csv", newline="", encoding="utf-8") as fh:
        fila = next(r for r in csv.DictReader(fh)
                    if r["serie"] == "calidad" and r["k"] == k and r["instancia"] == inst)
    nodos = [PARTIDA] + fila["ids"].split("|")
    with open(R4 / "calidad_exactos.csv", newline="", encoding="utf-8") as fh:
        info = {r["id_medicion"]: json.loads(r["info"]) for r in csv.DictReader(fh)}
    tours = {metodo: [nodos[i] for i in info[f"calidad:k={k}:i={inst}:{metodo}"]["recorrido"]]
             for metodo in ("held_karp", "voraz")}
    with open(RAIZ / "data" / "catalogo" / "catalogo.csv", newline="", encoding="utf-8") as fh:
        nombres = {r["id"]: f"{r['nombre']} ({r['municipio']})" for r in csv.DictReader(fh)}

    print(f"Instancia calidad k={k} i={inst}")
    for n in nodos:
        print(f"  {n}: {nombres[n]}")
    print("\nTiempos en minutos (fila = desde, columna = hasta):")
    print("       " + "".join(f"{b:>8}" for b in nodos))
    for a in nodos:
        print(f"  {a:>4} " + "".join(f"{m[a][b]:8.1f}" for b in nodos))

    print("\nElecciones del voraz (alternativas disponibles en cada paso):")
    t = tours["voraz"]
    for i in range(len(t) - 2):
        pendientes = [b for b in nodos if b not in t[:i + 1]]
        opciones = ", ".join(f"{b} {m[t[i]][b]:.1f}" for b in sorted(pendientes, key=lambda b: m[t[i]][b]))
        print(f"  desde {t[i]} elige {t[i + 1]}  [{opciones}]")

    totales = {}
    for metodo, t in tours.items():
        tramos = [(a, b, m[a][b]) for a, b in pairwise(t)]
        totales[metodo] = sum(x for _, _, x in tramos)
        print(f"\n{metodo}: " + " | ".join(f"{a}->{b} {x:.1f}" for a, b, x in tramos)
              + f"  TOTAL {totales[metodo]:.1f} min")
    dif = totales["voraz"] - totales["held_karp"]
    print(f"\nDiferencia: {dif:.1f} min ({100 * dif / totales['held_karp']:.2f} %)")


if __name__ == "__main__":
    main()