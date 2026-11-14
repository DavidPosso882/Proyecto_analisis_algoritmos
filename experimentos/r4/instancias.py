"""T2 (R4-07, R4-20, DA-17): archivo de instancias reproducible.

Partida fija: Armenia (``C01``, §4). Cada instancia son ``k`` lugares
distintos del catálogo, de cualquier categoría, sin Armenia y sin repetir
(R4-07), sorteados sin reemplazo con ``random.Random(semilla)`` (R4-20).

Semillas derivadas (DA-17, EXP-06): maestra 42 + índice estable.
- Serie «curva»: una instancia por k = 5..12, índice 100 + k.
- Serie «calidad»: 5 instancias por k = 5, 8, 10 y 12; la instancia 1 es la
  de la curva, reutilizada como instancia 1 de R4.11 (DA-17); las instancias
  2..5 usan índice 200 + 10·k + instancia.

Salidas: ``resultados/r4/instancias.csv`` y ``resultados/r4/instancias_meta.json``.
Uso: .venv/bin/python experimentos/r4/instancias.py
"""

import csv
import random

from comun import (
    INSTANCIAS_CALIDAD,
    KS_CALIDAD,
    KS_CURVA,
    MATRIZ_CSV,
    PARTIDA,
    R4,
    RAIZ,
    cargar_catalogo,
    cargar_matriz,
    derivar_semilla,
    escribir_json,
    huella_ids,
    metadatos,
    semilla_calidad,
    semilla_curva,
)

INSTANCIAS_CSV = R4 / "instancias.csv"
INSTANCIAS_META = R4 / "instancias_meta.json"

COLUMNAS = [
    "serie",
    "k",
    "instancia",
    "nodos",
    "partida",
    "semilla",
    "indice_semilla",
    "ids",
    "huella",
]


def sortear(pool, k, semilla):
    """k lugares distintos sin reemplazo con semilla derivada (R4-07, R4-20)."""
    return random.Random(semilla).sample(pool, k)


def fila(serie, k, instancia, semilla, indice, elegidos):
    return {
        "serie": serie,
        "k": k,
        "instancia": instancia,
        "nodos": k + 1,  # Armenia + los k lugares (R4-07)
        "partida": PARTIDA,
        "semilla": semilla,
        "indice_semilla": indice,
        "ids": "|".join(elegidos),
        "huella": huella_ids(elegidos),
    }


def validar(filas, ids):
    """Invariantes de R4-07 y R4-20 sobre el archivo generado."""
    conjunto_ids = set(ids)
    for registro in filas:
        k = int(registro["k"])
        elegidos = registro["ids"].split("|")
        assert len(elegidos) == k, registro
        assert len(set(elegidos)) == k, f"R4-07: lugares repetidos en k={k}"
        assert PARTIDA not in elegidos, f"R4-07: Armenia dentro de la instancia k={k}"
        assert set(elegidos) <= conjunto_ids, f"R4-07: id fuera del catálogo k={k}"

    curva = {int(r["k"]): r["ids"] for r in filas if r["serie"] == "curva"}
    assert sorted(curva) == list(KS_CURVA), "R4-07: falta algún k de la curva"

    for k in KS_CALIDAD:
        calidad = [r for r in filas if r["serie"] == "calidad" and int(r["k"]) == k]
        assert len(calidad) == INSTANCIAS_CALIDAD, f"R4-11: faltan instancias en k={k}"
        conjuntos = [frozenset(r["ids"].split("|")) for r in calidad]
        assert len(set(conjuntos)) == len(conjuntos), (
            f"R4-20: instancias repetidas en k={k}"
        )
        assert conjunto_reutilizado(calidad, curva[k]), (
            f"DA-17: la instancia 1 de k={k} debe ser la de la curva"
        )


def conjunto_reutilizado(calidad, ids_curva):
    """La instancia 1 de calidad es exactamente la instancia de la curva."""
    primera = next(r for r in calidad if int(r["instancia"]) == 1)
    return primera["ids"] == ids_curva


def main():
    ids, _ = cargar_matriz()
    catalogo = cargar_catalogo()
    assert list(catalogo) == ids, "catálogo y matriz en distinto orden"
    pool = [lid for lid in ids if lid != PARTIDA]

    filas = []
    curva = {}
    for k in KS_CURVA:
        indice = 100 + k
        semilla = semilla_curva(k)
        assert semilla == derivar_semilla(indice)
        elegidos = sortear(pool, k, semilla)
        curva[k] = elegidos
        filas.append(fila("curva", k, 1, semilla, indice, elegidos))

    for k in KS_CALIDAD:
        for instancia in range(1, INSTANCIAS_CALIDAD + 1):
            if instancia == 1:
                indice = 100 + k
                semilla = semilla_curva(k)
                elegidos = list(curva[k])
            else:
                indice = 200 + 10 * k + instancia
                semilla = semilla_calidad(k, instancia)
                assert semilla == derivar_semilla(indice)
                elegidos = sortear(pool, k, semilla)
            filas.append(fila("calidad", k, instancia, semilla, indice, elegidos))

    validar(filas, ids)

    with open(INSTANCIAS_CSV, "w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)

    meta = metadatos(
        archivo=str(INSTANCIAS_CSV.relative_to(RAIZ)),
        matriz_tiempos=str(MATRIZ_CSV.relative_to(RAIZ)),
        partida=PARTIDA,
        ks_curva=list(KS_CURVA),
        ks_calidad=list(KS_CALIDAD),
        instancias_calidad=INSTANCIAS_CALIDAD,
        derivacion_semilla="42 + indice estable (curva 100+k; calidad 200+10k+i)",
        columnas=COLUMNAS,
        filas=filas,
    )
    escribir_json(INSTANCIAS_META, meta)

    for k in KS_CURVA:
        print(f"curva k={k:2d} nodos={k + 1:2d} semilla={semilla_curva(k)} "
              f"ids={'|'.join(curva[k])}")
    print(f"instancias: {len(filas)} filas -> {INSTANCIAS_CSV}")


if __name__ == "__main__":
    main()
