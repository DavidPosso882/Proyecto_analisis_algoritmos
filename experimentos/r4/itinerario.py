"""T4 (R4-12/R4-13, DA-19/DA-22): itinerario de un día desde Armenia.

Partida: Armenia (``C01``, plaza de Bolívar, §4). DA-22: la partida no se
visita, no suma tiempo de visita y no cuenta entre los atractivos.

Criterios ESCRITOS ANTES DE CALCULAR (DA-22, R4-27). Se serializan en
``resultados/r4/itinerario_criterio_previo.json`` antes de la primera llamada
a Held-Karp, junto con la selección ya sorteada, y no se modifican después:

1. Selección inicial: 8 atractivos (categoría ``atractivo`` del catálogo) por
   sorteo sin reemplazo con semilla derivada 42 + 900 (DA-17), de modo que la
   elección no depende de los tiempos de desplazamiento.
2. Quita: mientras la jornada (visitas + desplazamientos, incluido el regreso)
   supere 11 h, se quita el atractivo cuya quita deja la menor jornada, es
   decir el mayor ahorro de tiempo total (visita + desplazamiento); desempate
   por menor id. Tras cada quita se recalcula Held-Karp. Se registra el ahorro
   de cada atractivo quitado como evidencia (DA-22, R4-27) y la cantidad final
   de atractivos, que puede ser menor que 6 (DA-22).

Cálculo interno en segundos, sin redondear (R4-13); la tabla redondea solo al
presentar (``tablas_r4b.py``). «Cabe» sii jornada <= 11 h (DA-22).

Salidas: ``resultados/r4/itinerario_criterio_previo.json`` y
``resultados/r4/itinerario.json``.
Uso: .venv/bin/python experimentos/r4/itinerario.py
"""

import random

from comun import (
    JORNADA_S,
    PARTIDA,
    R4,
    RAIZ,
    cargar_catalogo,
    cargar_matriz,
    duracion_s,
    escribir_json,
    huella_archivo,
    metadatos,
    semilla_itinerario,
    submatriz,
)

from quindio.recorrido.exactos import held_karp

CRITERIO_PREVIO = R4 / "itinerario_criterio_previo.json"
SALIDA = R4 / "itinerario.json"

ATRACTIVOS_INICIALES = 8
CATEGORIA = "atractivo"

CRITERIO_SELECCION = (
    "Selección inicial: 8 atractivos (categoría «atractivo» del catálogo) por "
    "sorteo sin reemplazo con semilla derivada 42+900 (DA-17), sin mirar los "
    "tiempos de desplazamiento."
)
CRITERIO_QUITA = (
    "Quita (DA-22): mientras la jornada (visitas + desplazamientos, incluido el "
    "regreso) supere 11 h, se quita el atractivo cuya quita deja la menor "
    "jornada, es decir el mayor ahorro de tiempo total (visita + "
    "desplazamiento); desempate por menor id; se recalcula Held-Karp tras cada "
    "quita y se registra el ahorro como evidencia para R4-27."
)


def calcular_tour(celdas, pos, catalogo, atractivos):
    """Held-Karp sobre Armenia + atractivos, en segundos (R4-12, R4-13)."""
    nodos = [PARTIDA] + list(atractivos)
    matriz = submatriz(celdas, pos, nodos)
    tour, desplazamientos_s, info = held_karp(matriz, 0)
    visitas_s = sum(duracion_s(catalogo[a]) for a in atractivos)
    jornada_s = visitas_s + desplazamientos_s
    return {
        "atractivos": list(atractivos),
        "nodos": nodos,
        "tour": tour,
        "tour_ids": [nodos[i] for i in tour],
        "matriz": matriz,
        "visitas_s": visitas_s,
        "desplazamientos_s": desplazamientos_s,
        "jornada_s": jornada_s,
        "cabe": jornada_s <= JORNADA_S,
        "entradas_tabla": info["entradas_tabla"],
    }


def sortear_atractivos(catalogo):
    """8 atractivos por sorteo reproducible (criterio 1, previo al cálculo)."""
    pool = sorted(
        lid for lid, fila in catalogo.items()
        if fila["categoria"] == CATEGORIA and lid != PARTIDA
    )
    return random.Random(semilla_itinerario()).sample(pool, ATRACTIVOS_INICIALES)


def quitar(celdas, pos, catalogo, calculo):
    """Aplica el criterio de quita (criterio 2) y devuelve (pasos, final)."""
    pasos = []
    actual = calculo
    while not actual["cabe"] and len(actual["atractivos"]) > 1:
        candidatos = []
        for quitado in actual["atractivos"]:
            resto = [a for a in actual["atractivos"] if a != quitado]
            evaluado = calcular_tour(celdas, pos, catalogo, resto)
            ahorro_s = actual["jornada_s"] - evaluado["jornada_s"]
            candidatos.append((ahorro_s, quitado, evaluado))
        candidatos.sort(key=lambda c: (-c[0], c[1]))
        ahorro_s, quitado, evaluado = candidatos[0]
        pasos.append(
            {
                "paso": len(pasos) + 1,
                "atractivo": quitado,
                "nombre": catalogo[quitado]["nombre"],
                "ahorro_s": ahorro_s,
                "jornada_antes_s": actual["jornada_s"],
                "jornada_despues_s": evaluado["jornada_s"],
                "atractivos_restantes": len(evaluado["atractivos"]),
                "justificacion": (
                    "mayor ahorro de tiempo total (visita + desplazamiento) "
                    "según el criterio de quita registrado antes de calcular"
                ),
            }
        )
        actual = evaluado
    return pasos, actual


def filas_tabla(calculo, catalogo, matriz):
    """Filas de la tabla del Anexo en segundos (R4-13: sin redondear)."""
    tour = calculo["tour"]
    nodos = calculo["nodos"]
    filas = []
    acumulado_s = 0.0
    for paso, indice in enumerate(tour[1:-1], start=1):
        anterior = tour[paso - 1]
        desplazamiento_s = matriz[anterior][indice]
        visita_s = duracion_s(catalogo[nodos[indice]])
        acumulado_s += desplazamiento_s + visita_s
        filas.append(
            {
                "orden": paso,
                "lugar": nodos[indice],
                "nombre": catalogo[nodos[indice]]["nombre"],
                "desplazamiento_s": desplazamiento_s,
                "visita_s": visita_s,
                "acumulado_s": acumulado_s,
            }
        )
    regreso_s = matriz[tour[-2]][0]
    acumulado_s += regreso_s
    filas.append(
        {
            "orden": "Regreso",
            "lugar": PARTIDA,
            "nombre": catalogo[PARTIDA]["nombre"],
            "desplazamiento_s": regreso_s,
            "visita_s": None,
            "acumulado_s": acumulado_s,
        }
    )
    return filas, acumulado_s


def main():
    ids, celdas = cargar_matriz()
    pos = {lid: i for i, lid in enumerate(ids)}
    catalogo = cargar_catalogo()

    elegidos = sortear_atractivos(catalogo)
    previo = metadatos(
        archivo=str(CRITERIO_PREVIO.relative_to(RAIZ)),
        partida={
            "id": PARTIDA,
            "nombre": catalogo[PARTIDA]["nombre"],
            "se_visita": False,
            "suma_visita": False,
            "cuenta_como_atractivo": False,
        },
        jornada_limite_s=JORNADA_S,
        criterio_seleccion=CRITERIO_SELECCION,
        criterio_quita=CRITERIO_QUITA,
        semilla_seleccion=semilla_itinerario(),
        seleccion_inicial=elegidos,
        atractivos_iniciales=ATRACTIVOS_INICIALES,
        firma_r4_27={
            "decision_humana": "R4-27: elegir atractivos y justificar las quitas",
            "estado": "pendiente",
            "nota": "criterios y selección registrados antes de calcular (DA-22)",
        },
        orden_de_escritura="criterio y selección antes de la primera llamada a Held-Karp",
    )
    escribir_json(CRITERIO_PREVIO, previo)  # PRE-REGISTRO antes de calcular

    inicial = calcular_tour(celdas, pos, catalogo, elegidos)
    pasos, final = quitar(celdas, pos, catalogo, inicial)
    filas, acumulado_s = filas_tabla(final, catalogo, final["matriz"])

    assert abs(acumulado_s - final["jornada_s"]) <= 1e-6, "acumulado != jornada"
    assert (
        abs(final["jornada_s"] - final["visitas_s"] - final["desplazamientos_s"])
        <= 1e-9
    ), "R4-12: jornada != visitas + desplazamientos"
    assert final["cabe"] is (final["jornada_s"] <= JORNADA_S), "R4-12: cabe"

    resultado = metadatos(
        archivo=str(SALIDA.relative_to(RAIZ)),
        huella_criterio_previo=huella_archivo(CRITERIO_PREVIO),
        criterio=previo["criterio_quita"],
        criterio_seleccion=previo["criterio_seleccion"],
        semilla_seleccion=previo["semilla_seleccion"],
        jornada_limite_s=JORNADA_S,
        partida=previo["partida"],
        firma_r4_27=previo["firma_r4_27"],
        seleccion_inicial=elegidos,
        inicial={
            "n_atractivos": len(inicial["atractivos"]),
            "tour_ids": inicial["tour_ids"],
            "visitas_s": inicial["visitas_s"],
            "desplazamientos_s": inicial["desplazamientos_s"],
            "jornada_s": inicial["jornada_s"],
            "cabe": inicial["cabe"],
        },
        quitas=pasos,
        final={
            "n_atractivos": len(final["atractivos"]),
            "atractivos": final["atractivos"],
            "tour_ids": final["tour_ids"],
            "visitas_s": final["visitas_s"],
            "desplazamientos_s": final["desplazamientos_s"],
            "jornada_s": final["jornada_s"],
            "cabe": final["cabe"],
            "entradas_tabla_hk": final["entradas_tabla"],
        },
        definicion_acumulado=(
            "por fila: desplazamiento hasta el lugar + visita; la fila Regreso "
            "suma solo el desplazamiento de vuelta"
        ),
        tabla=filas,
        totales={
            "visitas_s": final["visitas_s"],
            "desplazamientos_s": final["desplazamientos_s"],
            "jornada_s": final["jornada_s"],
            "acumulado_s": acumulado_s,
            "cabe": final["cabe"],
        },
    )
    escribir_json(SALIDA, resultado)

    print(f"selección inicial: {len(elegidos)} atractivos, jornada "
          f"{inicial['jornada_s'] / 3600:.3f} h, cabe={inicial['cabe']}")
    for paso in pasos:
        print(f"  quita {paso['paso']}: {paso['atractivo']} "
              f"ahorro={paso['ahorro_s'] / 60:.2f} min -> "
              f"{paso['jornada_despues_s'] / 3600:.3f} h")
    print(f"final: {len(final['atractivos'])} atractivos, jornada "
          f"{final['jornada_s'] / 3600:.3f} h, cabe={final['cabe']}")
    print(f"tour: {' -> '.join(final['tour_ids'])}")
    print(f"JSON: {SALIDA}")


if __name__ == "__main__":
    main()
