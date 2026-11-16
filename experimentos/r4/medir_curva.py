"""T2 (R4-07/08/09, DA-17, EXP-03/04/08): curva de tiempo frente a k.

Una instancia por k (serie «curva» de ``resultados/r4/instancias.csv``), la
MISMA para fuerza bruta y Held-Karp (R4-07, EXP-11). Cada medición pasa por el
arnés UT-01: 5 repeticiones y mediana; si la primera pasa de un minuto se mide
una sola vez (EXP-04); si una ejecución pasa de 5 minutos se detiene y se
registra ``no_completada`` sin tiempo (EXP-08). La serie de cada método se
corta en su primer k ``no_completada`` (R4-08): no se sube más k para ese
método.

Región medida: solo el algoritmo (la matriz ya viene recortada, EXP-02).
Reanudable: no repite filas ya escritas, incluidas las ``no_completada``
(EXP-16), y conserva la regla de corte al reanudar.

Salida: ``resultados/r4/curva_exactos.csv`` (esquema del arnés, EXP-14).
Uso: .venv/bin/python experimentos/r4/medir_curva.py
"""

from comun import (
    KS_CURVA,
    PARTIDA,
    R4,
    cargar_matriz,
    leer_csv,
    submatriz,
    verificar_exactos,
)

from quindio.medicion.arnes import (
    ESTADO_NO_COMPLETADA,
    cargar_filas,
    guardar_incremental,
    medir,
)
from quindio.recorrido.exactos import fuerza_bruta, held_karp

INSTANCIAS_CSV = R4 / "instancias.csv"
SALIDA = R4 / "curva_exactos.csv"

VERIFICACION = (
    "R4-06/GLOB-06: fuerza bruta == Held-Karp == 5 (caso a mano) antes de medir"
)


def fn_fuerza_bruta(matriz, partida):
    """Algoritmo medido: solo la llamada propia (EXP-02)."""
    tour, total, info = fuerza_bruta(matriz, partida)
    return None, {
        "total_s": total,
        "recorrido": tour,
        "permutaciones": info["permutaciones"],
    }


def fn_held_karp(matriz, partida):
    """Algoritmo medido: solo la llamada propia (EXP-02)."""
    tour, total, info = held_karp(matriz, partida)
    return None, {
        "total_s": total,
        "recorrido": tour,
        "entradas_tabla": info["entradas_tabla"],
    }


def main():
    ids, celdas = cargar_matriz()
    pos = {lid: i for i, lid in enumerate(ids)}
    instancias = {
        int(r["k"]): r for r in leer_csv(INSTANCIAS_CSV) if r["serie"] == "curva"
    }
    assert sorted(instancias) == list(KS_CURVA), "faltan instancias de la curva"
    existentes = {f["id_medicion"]: f for f in cargar_filas(str(SALIDA))}
    metodos = (("fuerza_bruta", fn_fuerza_bruta), ("held_karp", fn_held_karp))

    for metodo, fn in metodos:
        for k in KS_CURVA:
            mid = f"curva:k={k}:{metodo}"
            fila = existentes.get(mid)
            if fila is None:
                registro = instancias[k]
                nodos = [PARTIDA] + registro["ids"].split("|")
                matriz = submatriz(celdas, pos, nodos)
                fila = medir(
                    fn,
                    (matriz, 0),
                    id_medicion=mid,
                    semilla=int(registro["semilla"]),
                    metodo_verificacion=VERIFICACION,
                    verificacion=verificar_exactos,
                )
                guardar_incremental(str(SALIDA), fila)
            mediana = fila["mediana_ms"]
            detalle = f"{mediana:.3f} ms" if mediana is not None else "sin tiempo"
            print(f"{mid:28s} estado={fila['estado']:14s} {detalle} "
                  f"crudos={len(fila['tiempos_ms_crudos'])}", flush=True)
            if fila["estado"] == ESTADO_NO_COMPLETADA:
                print(f"R4-08: serie de {metodo} se detiene en k={k}", flush=True)
                break

    print(f"CSV: {SALIDA}")


if __name__ == "__main__":
    main()
