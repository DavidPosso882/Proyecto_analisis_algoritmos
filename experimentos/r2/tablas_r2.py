"""T3+T4 R2b: CSV Anexo, gráfica, cociente y matriz desde mediciones (GLOB-08).

Todo se genera desde resultados/r2/mediciones.csv; nada a mano.
Uso: .venv/bin/python experimentos/r2/tablas_r2.py
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

RAIZ = Path(__file__).resolve().parents[2]
R2 = RAIZ / "resultados" / "r2"


def cargar():
    import sys
    csv.field_size_limit(sys.maxsize)
    with open(R2 / "mediciones.csv", encoding="utf-8") as fh:
        filas = []
        for r in csv.DictReader(fh):
            r["mediana_ms"] = float(r["mediana_ms"]) if r["mediana_ms"] else None
            r["tiempos_ms_crudos"] = json.loads(r["tiempos_ms_crudos"])
            r["info"] = json.loads(r["info"])
            filas.append(r)
    return filas


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    filas = cargar()
    pares = [f for f in filas if f["id_medicion"].startswith("par:")]
    mats = [f for f in filas if f["id_medicion"].startswith("mat:")]
    assert all(f["estado"] == "ok" for f in pares + mats)

    # R2-08: CSV exacto del Anexo
    with open(R2 / "mediciones_anexo.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["origen", "destino", "version", "tiempo_viaje_s",
                    "nodos_explorados", "tiempo_ms"])
        for f in pares:
            _, o, d, ver = f["id_medicion"].split(":")
            w.writerow([o, d, ver, f["info"]["tiempo_viaje_s"],
                        f["info"]["nodos_explorados"], f"{f['mediana_ms']:.3f}"])

    # 10 lineales ⊆ 20 cola (R2 salida)
    cola = {(f["id_medicion"].split(":")[1], f["id_medicion"].split(":")[2])
            for f in pares if f["id_medicion"].endswith(":cola_prioridad")}
    lineal = {(f["id_medicion"].split(":")[1], f["id_medicion"].split(":")[2])
              for f in pares if f["id_medicion"].endswith(":lineal")}
    assert lineal <= cola and len(cola) == 20 and len(lineal) == 10

    # R2-06b: mismos tiempos exactos + R2-10 cocientes
    cocientes = []
    for o, d in sorted(lineal):
        tc = next(f for f in pares if f["id_medicion"] == f"par:{o}:{d}:cola_prioridad")
        tl = next(f for f in pares if f["id_medicion"] == f"par:{o}:{d}:lineal")
        assert tc["info"]["tiempo_viaje_s"] == tl["info"]["tiempo_viaje_s"], (o, d)
        cocientes.append(tl["mediana_ms"] / tc["mediana_ms"])
    cocientes.sort()
    por_par = []
    for o, d in sorted(lineal):
        tc = next(f for f in pares if f["id_medicion"] == f"par:{o}:{d}:cola_prioridad")
        tl = next(f for f in pares if f["id_medicion"] == f"par:{o}:{d}:lineal")
        por_par.append(f"{o}->{d}={tl['mediana_ms'] / tc['mediana_ms']:.0f}x")
    coc = {"mediana": cocientes[len(cocientes) // 2], "minimo": cocientes[0],
           "maximo": cocientes[-1], "por_par": por_par}
    with open(R2 / "cociente.json", "w", encoding="utf-8") as fh:
        json.dump(coc, fh, indent=2)
    print("cociente lineal/cola: mediana={:.0f} min={:.0f} max={:.0f}".format(coc["mediana"], coc["minimo"], coc["maximo"]))

    # R2-09: gráfica nodos-vs-ms, 2 series
    for ver, color, marcador in (("cola_prioridad", "tab:blue", "o"), ("lineal", "tab:orange", "s")):
        xs = [f["info"]["nodos_explorados"] for f in pares if f["id_medicion"].endswith(ver)]
        ys = [f["mediana_ms"] for f in pares if f["id_medicion"].endswith(ver)]
        plt.scatter(xs, ys, c=color, marker=marcador, label=ver)
    plt.xlabel("nodos explorados")
    plt.ylabel("tiempo (ms)")
    plt.legend()
    plt.savefig(R2 / "grafica_nodos_ms.png", dpi=100)
    plt.close()
    print("gráfica:", R2 / "grafica_nodos_ms.png")

    # R2-11: matriz dirigida sin simetrizar, diagonal 0, header==ids
    with open(RAIZ / "data" / "catalogo" / "catalogo.csv", encoding="utf-8") as fh:
        ids = [r["id"] for r in csv.DictReader(fh)]
    with open(RAIZ / "data" / "procesado" / "asociaciones.csv", encoding="utf-8") as fh:
        idx_de = {r["id"]: int(r["idx"]) for r in csv.DictReader(fh)}
    dist_de = {}
    for f in mats:
        lid = f["id_medicion"].split(":")[1]
        dist_de[lid] = f["info"]["distancias"]
    assert set(dist_de) == set(ids) and len(ids) == 40
    for lid in ids:
        assert dist_de[lid][idx_de[lid]] == 0.0
        assert all(v != float("inf") for v in dist_de[lid]), lid  # R1-10
    with open(R2 / "matriz_tiempos.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id"] + ids)
        for i in ids:
            w.writerow([i] + [f"{dist_de[i][idx_de[j]]:.3f}" for j in ids])
    print("matriz 40x40:", R2 / "matriz_tiempos.csv")


if __name__ == "__main__":
    main()
