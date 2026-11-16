"""T2+T3+T4 (GLOB-08, GLOB-09, EXP-09): tablas, gráfica y cifras de R4b.

Todo se genera SOLO desde los archivos de resultados:

- ``resultados/r4/instancias.csv`` (R4-07, R4-20, DA-17)
- ``resultados/r4/curva_exactos.csv`` (R4-08, EXP-14)
- ``resultados/r4/calidad_exactos.csv`` (R4-11)
- ``resultados/r4/itinerario.json`` (R4-12, R4-13)

Salidas (en ``resultados/r4/``): ``tabla_exactos.csv``, ``grafica_k_ms.png``,
``calidad_brechas.csv``, ``tabla_calidad.csv``, ``tabla_itinerario.csv`` y
``cifras_r4b.json``. La gráfica no traza los k ``no_completada`` (R4-09) y la
brecha se recalcula por instancia desde el CSV (R4-11, DA-18); una brecha
negativa más allá de la tolerancia de DA-15 es un fallo y corta la ejecución.

Redondeo solo al presentar (R4-13): tiempos del itinerario en minutos con 2
decimales y en horas con 3; brechas con 4 decimales. Los archivos de
resultados conservan los segundos y los porcentajes sin redondear.

Uso: .venv/bin/python experimentos/r4/tablas_r4b.py
"""

import csv
import json

from comun import (
    INSTANCIAS_CALIDAD,
    JORNADA_S,
    KS_CALIDAD,
    KS_CURVA,
    R4,
    TOLERANCIA,
    cargar_catalogo,
    escribir_json,
    leer_csv,
    metadatos,
)

from quindio.medicion.arnes import (
    ESTADO_NO_COMPLETADA,
    UMBRAL_UNA_SOLA_S,
    cargar_filas,
)

INSTANCIAS_CSV = R4 / "instancias.csv"
CURVA_CSV = R4 / "curva_exactos.csv"
CALIDAD_CSV = R4 / "calidad_exactos.csv"
ITINERARIO_JSON = R4 / "itinerario.json"

TABLA_EXACTOS = R4 / "tabla_exactos.csv"
GRAFICA = R4 / "grafica_k_ms.png"
BRECHAS_CSV = R4 / "calidad_brechas.csv"
TABLA_CALIDAD = R4 / "tabla_calidad.csv"
TABLA_ITINERARIO = R4 / "tabla_itinerario.csv"
CIFRAS = R4 / "cifras_r4b.json"

BYTES_POR_ENTRADA = 8  # R4-05: un flotante de Python por entrada
DECIMALES_MIN = 2
DECIMALES_H = 3
DECIMALES_BRECHA = 4


def indexar_curva(filas):
    """(k, método) -> fila del arnés, desde los id_medicion."""
    indice = {}
    for fila in filas:
        _, parte_k, metodo = fila["id_medicion"].split(":")
        indice[(int(parte_k.split("=")[1]), metodo)] = fila
    return indice


def mayor_k(serie):
    """Mayor k con estado completado (R4-08, comprobación automática)."""
    completados = [k for k, f in serie.items() if f["estado"] != ESTADO_NO_COMPLETADA]
    return max(completados) if completados else None


def comprobar_serie(nombre, serie):
    """R4-08: la serie llega a 12 o al primer no_completada, sin huecos."""
    mayor = mayor_k(serie)
    assert mayor is not None, f"{nombre}: sin mediciones completadas"
    assert sorted(k for k in serie if k <= mayor) == list(range(min(KS_CURVA), mayor + 1)), (
        f"R4-08: huecos en la serie de {nombre}"
    )
    no_completadas = sorted(
        k for k, f in serie.items() if f["estado"] == ESTADO_NO_COMPLETADA
    )
    assert all(k == mayor + 1 for k in no_completadas), (
        f"R4-08: {nombre} no completó un k que no es el siguiente a {mayor}"
    )
    assert set(serie) <= set(KS_CURVA), f"{nombre}: k fuera de 5..12"
    return mayor, no_completadas


def tabla_exactos(curva):
    """Tabla del Anexo (columnas ampliadas) desde la curva medida (GLOB-09)."""
    filas = []
    for k in KS_CURVA:
        bruta = curva.get((k, "fuerza_bruta"))
        hk = curva.get((k, "held_karp"))
        entradas = hk["info"]["entradas_tabla"] if hk else ""
        filas.append(
            {
                "k": k,
                "nodos": k + 1,
                "Tiempo fuerza bruta (ms)": _ms(bruta),
                "Tiempo Held-Karp (ms)": _ms(hk),
                "estado_fuerza_bruta": bruta["estado"] if bruta else "",
                "estado_held_karp": hk["estado"] if hk else "",
                "entradas_tabla_hk": entradas,
                "memoria_estimada_hk_mb": (
                    round(entradas * BYTES_POR_ENTRADA / (1024 * 1024), 3)
                    if entradas != ""
                    else ""
                ),
            }
        )
    return filas


def _ms(fila):
    if fila is None or fila["mediana_ms"] is None:
        return ""
    return f"{fila['mediana_ms']:.3f}"


def escribir_tabla(path, columnas, filas):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(filas)


def grafica_k_ms(curva):
    """R4-09: ms frente a k, una curva por solución, sin k no completados."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    series = (("fuerza bruta", "fuerza_bruta", "o"), ("Held-Karp", "held_karp", "s"))
    puntos = {}
    for etiqueta, metodo, marcador in series:
        completados = [
            (k, fila) for (k, m), fila in sorted(curva.items())
            if m == metodo and fila["estado"] != ESTADO_NO_COMPLETADA
        ]
        assert all(f["estado"] == "ok" for _, f in completados), (
            "R4-09: no se trazan valores de ejecuciones no completadas"
        )
        puntos[etiqueta] = [k for k, _ in completados]
        plt.plot(
            puntos[etiqueta],
            [f["mediana_ms"] for _, f in completados],
            marker=marcador,
            label=etiqueta,
        )
    plt.xlabel("k")
    plt.ylabel("tiempo (ms)")
    plt.yscale("log")
    plt.xticks(list(KS_CURVA))
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.title("Tiempo de las soluciones exactas frente a k (escala logarítmica)")
    plt.savefig(GRAFICA, dpi=110, bbox_inches="tight")
    plt.close()
    return puntos


def comprobar_arness(curva):
    """EXP-03/EXP-04/EXP-08 desde el CSV: crudos, mediana y no completadas."""
    crudos_por_serie = {}
    for (k, metodo), fila in sorted(curva.items()):
        crudos = fila["tiempos_ms_crudos"]
        if fila["estado"] == ESTADO_NO_COMPLETADA:
            assert crudos == [], f"EXP-08: no_completada con tiempos en k={k}"
            crudos_por_serie.setdefault(metodo, {})[k] = 0
            continue
        assert len(crudos) in (1, 5), f"EXP-03: {len(crudos)} crudos en k={k}/{metodo}"
        if len(crudos) == 5:
            mediana = sorted(crudos)[2]
        else:
            assert crudos[0] > UMBRAL_UNA_SOLA_S * 1000, (
                f"EXP-04: una sola medición de {crudos[0]} ms en k={k}/{metodo}"
            )
            mediana = crudos[0]
        assert abs(mediana - fila["mediana_ms"]) <= 1e-9, (
            f"EXP-03: la mediana no es el tercer crudo en k={k}/{metodo}"
        )
        crudos_por_serie.setdefault(metodo, {})[k] = len(crudos)
    return crudos_por_serie


def brechas_calidad(calidad, instancias):
    """Recalcula la brecha por instancia desde el CSV (R4-11, DA-18)."""
    por_instancia = {}
    for (k, instancia, metodo), fila in calidad.items():
        clave = (k, instancia)
        por_instancia.setdefault(clave, {})[metodo] = fila

    filas = []
    for (k, instancia) in sorted(por_instancia):
        datos = por_instancia[(k, instancia)]
        assert set(datos) == {"held_karp", "voraz"}, (k, instancia)
        hk = datos["held_karp"]["info"]["total_s"]
        heuristica = datos["voraz"]["info"]["total_s"]
        brecha = (heuristica - hk) / hk * 100
        registro = instancias[("calidad", k, instancia)]
        filas.append(
            {
                "k": k,
                "instancia": instancia,
                "semilla": int(registro["semilla"]),
                "nodos": int(registro["nodos"]),
                "ids": registro["ids"],
                "heldkarp_s": hk,
                "heuristica_s": heuristica,
                "brecha_pct": brecha,
            }
        )

    assert len(filas) == len(KS_CALIDAD) * INSTANCIAS_CALIDAD, "R4-11: faltan instancias"
    negativas = [f for f in filas if f["brecha_pct"] < -TOLERANCIA * 100]
    assert not negativas, f"R4-11: brecha negativa (fallo): {negativas}"
    return filas


def resumen_brechas(por_instancia):
    """Promedio y máximo de la brecha por k y en total (R4-11)."""
    resumen = {}
    for k in KS_CALIDAD:
        valores = [f["brecha_pct"] for f in por_instancia if f["k"] == k]
        assert len(valores) == INSTANCIAS_CALIDAD, f"R4-11: k={k} con {len(valores)}"
        resumen[k] = {
            "instancias": len(valores),
            "promedio": sum(valores) / len(valores),
            "maximo": max(valores),
            "minimo": min(valores),
        }
    todos = [f["brecha_pct"] for f in por_instancia]
    resumen["global"] = {
        "instancias": len(todos),
        "promedio": sum(todos) / len(todos),
        "maximo": max(todos),
        "minimo": min(todos),
    }
    return resumen


def tabla_itinerario(itinerario):
    """Tabla del Anexo desde el JSON, en minutos y horas al presentar (R4-13)."""
    filas = []
    for fila in itinerario["tabla"]:
        filas.append(
            {
                "Orden": fila["orden"],
                "Lugar": f"{fila['lugar']} {fila['nombre']}",
                "Desplazamiento desde el anterior (min)": (
                    f"{fila['desplazamiento_s'] / 60:.{DECIMALES_MIN}f}"
                ),
                "Visita (min)": (
                    f"{fila['visita_s'] / 60:.{DECIMALES_MIN}f}"
                    if fila["visita_s"] is not None
                    else "—"
                ),
                "Tiempo acumulado (h)": f"{fila['acumulado_s'] / 3600:.{DECIMALES_H}f}",
            }
        )
    totales = itinerario["totales"]
    filas.extend(
        [
            {
                "Orden": "Totales",
                "Lugar": "Tiempo total de visitas",
                "Desplazamiento desde el anterior (min)": "",
                "Visita (min)": f"{totales['visitas_s'] / 60:.{DECIMALES_MIN}f}",
                "Tiempo acumulado (h)": "",
            },
            {
                "Orden": "Totales",
                "Lugar": "Tiempo total de desplazamientos",
                "Desplazamiento desde el anterior (min)": (
                    f"{totales['desplazamientos_s'] / 60:.{DECIMALES_MIN}f}"
                ),
                "Visita (min)": "",
                "Tiempo acumulado (h)": "",
            },
            {
                "Orden": "Totales",
                "Lugar": "Duración total de la jornada",
                "Desplazamiento desde el anterior (min)": "",
                "Visita (min)": "",
                "Tiempo acumulado (h)": f"{totales['jornada_s'] / 3600:.{DECIMALES_H}f}",
            },
            {
                "Orden": "Totales",
                "Lugar": f"Cabe en la jornada de {JORNADA_S / 3600:.0f} h",
                "Desplazamiento desde el anterior (min)": "",
                "Visita (min)": "",
                "Tiempo acumulado (h)": "sí" if totales["cabe"] else "no",
            },
        ]
    )
    return filas


def comprobar_itinerario(itinerario):
    """R4-12: total = visitas + desplazamientos, acumulado y «cabe» coherentes."""
    tabla = itinerario["tabla"]
    totales = itinerario["totales"]
    visitas_s = sum(f["visita_s"] for f in tabla if f["visita_s"] is not None)
    desplazamientos_s = sum(f["desplazamiento_s"] for f in tabla)
    assert abs(visitas_s - totales["visitas_s"]) <= 1e-6, "R4-12: visitas"
    assert abs(desplazamientos_s - totales["desplazamientos_s"]) <= 1e-6, (
        "R4-12: desplazamientos"
    )
    assert abs(visitas_s + desplazamientos_s - totales["jornada_s"]) <= 1e-6, (
        "R4-12: jornada != visitas + desplazamientos"
    )
    acumulados = [f["acumulado_s"] for f in tabla]
    assert acumulados == sorted(acumulados), "R4-12: el acumulado decrece"
    assert abs(acumulados[-1] - totales["jornada_s"]) <= 1e-6, "R4-12: acumulado final"
    assert totales["cabe"] is (totales["jornada_s"] <= JORNADA_S), (
        "R4-12: «cabe» no coincide con total <= 11 h"
    )
    assert 1 <= itinerario["final"]["n_atractivos"] <= 8, "R4-12: cantidad final"
    return {
        "n_atractivos_inicial": itinerario["inicial"]["n_atractivos"],
        "n_atractivos_final": itinerario["final"]["n_atractivos"],
        "visitas_s": totales["visitas_s"],
        "desplazamientos_s": totales["desplazamientos_s"],
        "jornada_s": totales["jornada_s"],
        "cabe": totales["cabe"],
    }


def main():
    instancias = {}
    for fila in leer_csv(INSTANCIAS_CSV):
        instancias[(fila["serie"], int(fila["k"]), int(fila["instancia"]))] = fila

    curva = indexar_curva(cargar_filas(str(CURVA_CSV)))
    mayores = {}
    no_completadas = {}
    for metodo in ("fuerza_bruta", "held_karp"):
        serie = {k: f for (k, m), f in curva.items() if m == metodo}
        mayores[metodo], no_completadas[metodo] = comprobar_serie(metodo, serie)

    # R4-07 / EXP-11: misma instancia para ambos métodos en cada k.
    for k in KS_CURVA:
        bruta = curva.get((k, "fuerza_bruta"))
        hk = curva.get((k, "held_karp"))
        if bruta is not None and hk is not None:
            assert bruta["huella_entrada"] == hk["huella_entrada"], (
                f"R4-07: k={k} con entradas distintas entre métodos"
            )
        registro = instancias[("curva", k, 1)]
        elegidos = registro["ids"].split("|")
        assert len(set(elegidos)) == k and "C01" not in elegidos, (
            f"R4-07: instancia inválida en k={k}"
        )

    tabla = tabla_exactos(curva)
    escribir_tabla(
        TABLA_EXACTOS,
        [
            "k",
            "nodos",
            "Tiempo fuerza bruta (ms)",
            "Tiempo Held-Karp (ms)",
            "estado_fuerza_bruta",
            "estado_held_karp",
            "entradas_tabla_hk",
            "memoria_estimada_hk_mb",
        ],
        tabla,
    )

    # R4-06: ambos métodos dan el mismo óptimo en los k que la bruta resuelve.
    igualdad = {}
    for k in range(min(KS_CURVA), mayores["fuerza_bruta"] + 1):
        bruta = curva[(k, "fuerza_bruta")]["info"]["total_s"]
        hk = curva[(k, "held_karp")]["info"]["total_s"]
        igualdad[k] = abs(bruta - hk) <= TOLERANCIA * max(1.0, abs(hk))
        assert igualdad[k], f"R4-06: k={k} bruta={bruta} hk={hk}"

    puntos = grafica_k_ms(curva)
    for etiqueta, ks in puntos.items():
        excluidos = sorted(set(KS_CURVA) - set(ks))
        assert excluidos == no_completadas[
            "fuerza_bruta" if etiqueta == "fuerza bruta" else "held_karp"
        ], f"R4-09: puntos excluidos inesperados en {etiqueta}"

    crudos = comprobar_arness(curva)

    calidad = {}
    for fila in cargar_filas(str(CALIDAD_CSV)):
        partes = fila["id_medicion"].split(":")
        k = int(partes[1].split("=")[1])
        instancia = int(partes[2].split("=")[1])
        calidad[(k, instancia, partes[3])] = fila
    por_instancia = brechas_calidad(calidad, instancias)
    conjuntos = {
        k: {instancias[("calidad", k, i)]["ids"] for i in range(1, INSTANCIAS_CALIDAD + 1)}
        for k in KS_CALIDAD
    }
    for k, sets in conjuntos.items():
        assert len(sets) == INSTANCIAS_CALIDAD, f"R4-11/R4-20: instancias repetidas en k={k}"

    with open(BRECHAS_CSV, "w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(
            fh,
            fieldnames=[
                "k",
                "instancia",
                "semilla",
                "nodos",
                "ids",
                "heldkarp_s",
                "heuristica_s",
                "brecha_pct",
            ],
        )
        escritor.writeheader()
        for fila in por_instancia:
            escritor.writerow({**fila, "brecha_pct": repr(fila["brecha_pct"])})

    resumen = resumen_brechas(por_instancia)
    escribir_tabla(
        TABLA_CALIDAD,
        [
            "k",
            "Instancias",
            "Brecha promedio (%)",
            "Brecha máxima (%)",
            "Brecha mínima (%)",
        ],
        [
            {
                "k": k,
                "Instancias": datos["instancias"],
                "Brecha promedio (%)": f"{datos['promedio']:.{DECIMALES_BRECHA}f}",
                "Brecha máxima (%)": f"{datos['maximo']:.{DECIMALES_BRECHA}f}",
                "Brecha mínima (%)": f"{datos['minimo']:.{DECIMALES_BRECHA}f}",
            }
            for k, datos in resumen.items()
            if k != "global"
        ],
    )

    with open(ITINERARIO_JSON, encoding="utf-8") as fh:
        itinerario = json.load(fh)
    cifras_itinerario = comprobar_itinerario(itinerario)
    filas_itinerario = tabla_itinerario(itinerario)
    escribir_tabla(
        TABLA_ITINERARIO,
        [
            "Orden",
            "Lugar",
            "Desplazamiento desde el anterior (min)",
            "Visita (min)",
            "Tiempo acumulado (h)",
        ],
        filas_itinerario,
    )

    catalogo = cargar_catalogo()
    cifras = metadatos(
        fuentes={
            "instancias": str(INSTANCIAS_CSV.relative_to(R4.parents[1])),
            "curva": str(CURVA_CSV.relative_to(R4.parents[1])),
            "calidad": str(CALIDAD_CSV.relative_to(R4.parents[1])),
            "itinerario": str(ITINERARIO_JSON.relative_to(R4.parents[1])),
        },
        comprobaciones={
            "R4-06_totales_optimos_iguales": True,
            "R4-07_misma_instancia_por_k": True,
            "R4-07_instancias_sin_armenia_y_sin_repetir": True,
            "R4-08_mayor_k_es_el_ultimo_completado": True,
            "R4-09_sin_puntos_no_completados": True,
            "R4-11_brecha_negativa_ausente": True,
            "R4-12_totales_acumulado_y_cabe": True,
            "EXP-03_mediana_de_cinco_crudos": True,
            "EXP-04_una_sola_medicion_si_pasa_de_un_minuto": True,
            "EXP-08_no_completada_sin_tiempo": True,
        },
        curva={
            "convenio_nodos": (
                "k lugares del catálogo sin Armenia + Armenia como partida "
                "(nodos = k + 1)"
            ),
            "tiempos_crudos_por_medicion": {
                str(metodo): {str(k): n for k, n in serie.items()}
                for metodo, serie in crudos.items()
            },
            "mayor_k_fuerza_bruta": mayores["fuerza_bruta"],
            "mayor_k_held_karp": mayores["held_karp"],
            "no_completadas": no_completadas,
            "totales_optimos_iguales_k": sorted(igualdad),
            "puntos_graficados": puntos,
            "unidad_tiempo": "ms",
        },
        calidad={
            "por_k": {str(k): v for k, v in resumen.items() if k != "global"},
            "global": resumen["global"],
            "brecha_negativa": False,
            "tolerancia_da15": TOLERANCIA,
            "formula": "(heuristica - heldkarp) / heldkarp * 100",
        },
        itinerario={
            **cifras_itinerario,
            "jornada_h": cifras_itinerario["jornada_s"] / 3600,
            "partida": catalogo[itinerario["partida"]["id"]]["nombre"],
            "quitas": [q["atractivo"] for q in itinerario["quitas"]],
            "firma_r4_27": itinerario["firma_r4_27"]["estado"],
        },
        presentacion={
            "decimales_min": DECIMALES_MIN,
            "decimales_h": DECIMALES_H,
            "decimales_brecha": DECIMALES_BRECHA,
            "nota": "los archivos de resultados conservan segundos y porcentajes sin redondear",
        },
        archivos=[
            str(TABLA_EXACTOS.name),
            str(GRAFICA.name),
            str(BRECHAS_CSV.name),
            str(TABLA_CALIDAD.name),
            str(TABLA_ITINERARIO.name),
        ],
    )
    escribir_json(CIFRAS, cifras)

    print(f"mayor k: fuerza bruta {mayores['fuerza_bruta']}, "
          f"Held-Karp {mayores['held_karp']}; no completadas {no_completadas}")
    print(f"R4-06 totales óptimos iguales en k={sorted(igualdad)}")
    print("brecha global: promedio {:.4f} % máximo {:.4f} %".format(
        resumen["global"]["promedio"], resumen["global"]["maximo"]))
    for k in KS_CALIDAD:
        print("  k={:2d}: prom {:.4f} % máx {:.4f} %".format(
            k, resumen[k]["promedio"], resumen[k]["maximo"]))
    print("itinerario: {} atractivos, {:.3f} h, cabe={}".format(
        cifras_itinerario["n_atractivos_final"],
        cifras_itinerario["jornada_s"] / 3600,
        cifras_itinerario["cabe"]))
    print(f"tablas y gráfica en {R4}")


if __name__ == "__main__":
    main()
