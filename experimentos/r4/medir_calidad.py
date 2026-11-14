"""T3 (R4-11, DA-17, EXP-03/04/08): calidad de la heurística frente a HK.

Para k = 5, 8, 10 y 12 con 5 instancias distintas por k (``resultados/r4/
instancias.csv``, serie «calidad»; la instancia 1 de cada k es la de la curva,
DA-17). Cada instancia se mide con los dos métodos sobre la MISMA matriz
(EXP-11): Held-Karp (óptimo) y vecino más cercano dirigido (DA-13). Los
tiempos van por el arnés UT-01 (mediana de 5, una sola si pasa de un minuto,
``no_completada`` si pasa de 5 minutos).

La brecha (H-HK)/HK×100 no se calcula aquí: se recalcula desde este CSV en
``tablas_r4b.py`` (R4-11, DA-18, GLOB-08).

Salida: ``resultados/r4/calidad_exactos.csv`` (esquema del arnés, EXP-14).
Uso: .venv/bin/python experimentos/r4/medir_calidad.py
"""

from comun import (
    INSTANCIAS_CALIDAD,
    KS_CALIDAD,
    PARTIDA,
    R4,
    cargar_matriz,
    leer_csv,
    submatriz,
    verificar_exactos,
    verificar_voraz,
)

from quindio.medicion.arnes import cargar_filas, guardar_incremental, medir
from quindio.recorrido.exactos import held_karp
from quindio.recorrido.voraz import vecino_mas_cercano

INSTANCIAS_CSV = R4 / "instancias.csv"
SALIDA = R4 / "calidad_exactos.csv"

VERIFICACION = (
    "GLOB-06: Held-Karp == fuerza bruta == 5 (caso a mano) y voraz con costo "
    "recalculado igual al reportado, antes de medir"
)


def fn_held_karp(matriz, partida):
    """Algoritmo medido: solo la llamada propia (EXP-02)."""
    tour, total, info = held_karp(matriz, partida)
    return None, {
        "total_s": total,
        "recorrido": tour,
        "entradas_tabla": info["entradas_tabla"],
    }


def fn_voraz(matriz, partida):
    """Algoritmo medido: solo la llamada propia (EXP-02)."""
    tour, total, _ = vecino_mas_cercano(matriz, partida)
    return None, {"total_s": total, "recorrido": tour}


def verificacion_voraz(matriz):
    """Verificación previa (GLOB-06) de la instancia que se va a medir."""

    def comprobar():
        return verificar_voraz(matriz, 0)

    return comprobar


def main():
    ids, celdas = cargar_matriz()
    pos = {lid: i for i, lid in enumerate(ids)}
    instancias = {
        (int(r["k"]), int(r["instancia"])): r
        for r in leer_csv(INSTANCIAS_CSV)
        if r["serie"] == "calidad"
    }
    assert sorted(instancias) == [
        (k, i) for k in KS_CALIDAD for i in range(1, INSTANCIAS_CALIDAD + 1)
    ], "faltan instancias de calidad"
    existentes = {f["id_medicion"]: f for f in cargar_filas(str(SALIDA))}

    for k in KS_CALIDAD:
        for instancia in range(1, INSTANCIAS_CALIDAD + 1):
            registro = instancias[(k, instancia)]
            nodos = [PARTIDA] + registro["ids"].split("|")
            matriz = submatriz(celdas, pos, nodos)
            semilla = int(registro["semilla"])
            for metodo, fn in (("held_karp", fn_held_karp), ("voraz", fn_voraz)):
                mid = f"calidad:k={k}:i={instancia}:{metodo}"
                fila = existentes.get(mid)
                if fila is None:
                    fila = medir(
                        fn,
                        (matriz, 0),
                        id_medicion=mid,
                        semilla=semilla,
                        metodo_verificacion=VERIFICACION,
                        verificacion=verificar_exactos
                        if metodo == "held_karp"
                        else verificacion_voraz(matriz),
                    )
                    guardar_incremental(str(SALIDA), fila)
                mediana = fila["mediana_ms"]
                detalle = f"{mediana:.3f} ms" if mediana is not None else "sin tiempo"
                print(f"{mid:34s} estado={fila['estado']:14s} {detalle} "
                      f"total_s={fila['info']['total_s']:.3f}", flush=True)

    print(f"CSV: {SALIDA}")


if __name__ == "__main__":
    main()
