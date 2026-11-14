"""T1 R2b: tabla de vecindad + sorteo determinista de pares (DA-14, EXP-10).

Cercano = mismo municipio o cabeceras a ≤15 km (Geod, calculado del
catálogo). Sorteo con semilla 42+índice, reproducible y archivado.
Uso: .venv/bin/python experimentos/r2/elegir_pares.py
"""
import csv
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.medicion.arnes import derivar_semilla

RAIZ = Path(__file__).resolve().parents[2]
UMBRAL_VECINO_KM = 15.0


def main():
    from pyproj import Geod

    with open(RAIZ / "data" / "catalogo" / "catalogo.csv", encoding="utf-8") as fh:
        lugares = list(csv.DictReader(fh))
    cabs = {r["municipio"]: (float(r["longitud"]), float(r["latitud"]))
            for r in lugares if r["categoria"] == "cabecera"}
    geod = Geod(ellps="WGS84")
    munis = sorted(cabs)
    vecinos = {}
    for i, a in enumerate(munis):
        for b in munis[i + 1:]:
            _, _, m = geod.inv(cabs[a][0], cabs[a][1], cabs[b][0], cabs[b][1])
            if m / 1000.0 <= UMBRAL_VECINO_KM:
                vecinos.setdefault(a, set()).add(b)
                vecinos.setdefault(b, set()).add(a)
    with open(RAIZ / "resultados" / "r2" / "vecindad.csv", "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["municipio", "vecinos_le15km"])
        for m in munis:
            w.writerow([m, ";".join(sorted(vecinos.get(m, [])))])

    def cercanos(a, b):
        if a["municipio"] == b["municipio"]:
            return True
        return b["municipio"] in vecinos.get(a["municipio"], set())

    ids = [r["id"] for r in lugares]
    por_id = {r["id"]: r for r in lugares}
    pares_cercanos, pares_lejanos = [], []
    for i in range(len(ids)):
        for j in range(len(ids)):
            if i == j:
                continue
            (pares_cercanos if cercanos(por_id[ids[i]], por_id[ids[j]])
             else pares_lejanos).append((ids[i], ids[j]))
    rng = random.Random(derivar_semilla(200))
    diez = rng.sample(sorted(pares_cercanos), 10)
    resto_cerc = [p for p in sorted(pares_cercanos) if p not in diez]
    otros = rng.sample(sorted(resto_cerc), 5) + rng.sample(sorted(pares_lejanos), 5)
    with open(RAIZ / "resultados" / "r2" / "pares.csv", "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["origen", "destino", "cercano", "con_lineal"])
        for o, d in diez:
            w.writerow([o, d, "si", "si"])
        for o, d in otros:
            w.writerow([o, d, "si" if (o, d) in pares_cercanos else "no", "no"])
    print("cercanos:", len(pares_cercanos), "| lejanos:", len(pares_lejanos))
    print("pares: 10 con lineal + 10 solo cola = 20")


if __name__ == "__main__":
    main()
