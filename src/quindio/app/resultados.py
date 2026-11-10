"""Tablas y gráficas del Anexo R1–R4 leídas de ``resultados/`` (R5-05, GLOB-08).

Ninguna cifra se recalcula: cada tabla se arma con los archivos que generaron
los experimentos y cada gráfica es el PNG guardado en ``resultados/``. Cada
bloque trae una lectura breve con la unidad de tiempo (GLOB-10) y las columnas
del Anexo, que pueden ampliarse pero no reducirse (GLOB-09).
"""

import json

from .datos import leer_csv_resultados, leer_json_resultados

# Orden del Anexo para la tabla de tiempo de R1 (radios crecientes y total).
ORDEN_R1 = (
    "Radio de 2 km",
    "Radio de 5 km",
    "Radio de 10 km",
    "Radio de 20 km",
    "Departamento completo",
)


def bloques():
    """Bloques de tablas y gráficas de R1 a R4, en el orden del Anexo."""
    return [_r1(), _r2(), _r3(), _r4()]


def _tabla(titulo, columnas, filas, unidad, lectura):
    return {
        "titulo": titulo,
        "columnas": columnas,
        "filas": filas,
        "unidad": unidad,
        "lectura": lectura,
    }


def _tabla_de_archivo(titulo, nombre, unidad, lectura):
    """Tabla con las columnas y filas del CSV de resultados, sin retocarlas."""
    filas = leer_csv_resultados(nombre)
    columnas = list(filas[0].keys()) if filas else []
    return _tabla(
        titulo,
        columnas,
        [[fila[columna] for columna in columnas] for fila in filas],
        unidad,
        lectura,
    )


def _r1():
    cifras = leer_json_resultados("r1/cifras_r1a.json")["departamento"]
    tamano = _tabla(
        "Tamaño de la red antes y después de quedarse con la componente",
        ["Red", "Nodos", "Aristas"],
        [
            ["Red descargada", cifras["V"], cifras["E_multi"]],
            ["Componente fuertemente conexa", cifras["Vc"], cifras["Ec_multi"]],
        ],
        "Recuento de nodos y aristas; sin unidad de tiempo.",
        (
            f"La componente conserva {cifras['Vc']} de {cifras['V']} nodos y "
            f"{cifras['Ec_multi']} de {cifras['E_multi']} aristas (multigrafo). "
            "El resto del proyecto trabaja solo con la componente, que es donde "
            "existe camino dirigido entre cualquier par de nodos."
        ),
    )

    medidas = {
        fila["id_medicion"]: fila for fila in leer_csv_resultados("r1/t_componente.csv")
    }
    filas = []
    for nombre in ORDEN_R1:
        fila = medidas[nombre]
        # V, E y V + E viajan en la columna `info` del registro EXP-14.
        detalle = json.loads(fila["info"])
        filas.append(
            [
                nombre,
                detalle["V"],
                detalle["E"],
                detalle["V_mas_E"],
                f"{float(fila['mediana_ms']):.3f}",
            ]
        )
    tiempos = _tabla(
        "Tiempo de obtener la componente",
        ["Red", "V", "E", "V + E", "Tiempo (ms)"],
        filas,
        "Tiempo en milisegundos (mediana de 5 ejecuciones, EXP-05).",
        (
            "El tiempo crece con V + E, como corresponde a una búsqueda de "
            "componentes en tiempo lineal; el orden de las filas es el del Anexo "
            "(radios crecientes y departamento completo)."
        ),
    )
    return {
        "id": "r1",
        "titulo": "Requerimiento 1 · Modelo de la red vial",
        "tablas": [tamano, tiempos],
        "graficas": [],
    }


def _r2():
    cociente = leer_json_resultados("r2/cociente.json")
    tabla_cociente = _tabla(
        "Cociente entre versiones (10 pares medidos con ambas)",
        ["Mediana", "Mínimo", "Máximo"],
        [
            [
                f"{cociente['mediana']:.2f}",
                f"{cociente['minimo']:.2f}",
                f"{cociente['maximo']:.2f}",
            ]
        ],
        "Cociente de tiempos (lineal / cola de prioridad); adimensional.",
        (
            "La versión lineal tarda alrededor de 177 veces lo que la de cola en "
            "la red del departamento: la brecha refleja la complejidad O(V²) "
            "frente a O((V + E) log V), además del costo de las estructuras "
            "usadas en cada implementación propia."
        ),
    )
    tabla_mediciones = _tabla_de_archivo(
        "Mediciones de Dijkstra (una fila por consulta y por versión)",
        "r2/mediciones_anexo.csv",
        "Tiempo de viaje en segundos; tiempo de ejecución en milisegundos.",
        (
            "Cada par se midió con la versión de cola de prioridad y, en 10 "
            "pares, también con la lineal. El tiempo de viaje coincide entre "
            "versiones y es el que la aplicación vuelve a calcular al momento "
            "(R5-02)."
        ),
    )
    return {
        "id": "r2",
        "titulo": "Requerimiento 2 · Caminos mínimos",
        "tablas": [tabla_mediciones, tabla_cociente],
        "graficas": [
            {
                "titulo": "Nodos explorados frente a tiempo (ms), ambas versiones",
                "archivo": "r2/grafica_nodos_ms.png",
                "lectura": (
                    "Eje horizontal: nodos explorados; eje vertical: tiempo en "
                    "milisegundos. Se espera que la versión de cola quede muy por "
                    "debajo de la lineal para el mismo número de nodos."
                ),
            }
        ],
        "enlaces": [
            {
                "texto": "Matriz de tiempos 40 × 40 (segundos, dirigida)",
                "archivo": "r2/matriz_tiempos.csv",
            }
        ],
    }


def _r3():
    tabla = _tabla_de_archivo(
        "Envolvente convexa: tiempos propios y de referencia",
        "r3/tabla_anexo_r3.csv",
        "Tiempo en milisegundos; `n` es el número de puntos tras deduplicar.",
        (
            "La fila «Nodos de la red» es la que usa el mapa de la aplicación: "
            "sus vértices se leen del archivo de R3-11 sin recalcular (R5-03). El "
            "cociente es propio / referencia y se mantiene entre 4,6 y 11,0; tiende "
            "a crecer con el tamaño del conjunto porque la referencia está compilada "
            "y la implementación propia es Python puro."
        ),
    )
    return {
        "id": "r3",
        "titulo": "Requerimiento 3 · Envolvente convexa de la red vial",
        "tablas": [tabla],
        "graficas": [],
    }


def _r4():
    exactos = _tabla_de_archivo(
        "Soluciones exactas: fuerza bruta y Held-Karp",
        "r4/tabla_exactos.csv",
        "Tiempo en milisegundos; `nodos` = k lugares más la partida.",
        (
            "Held-Karp es órdenes de magnitud más rápido que la fuerza bruta al "
            "crecer k: O(k²·2^k) frente a O(k!). Los estados «no completada» "
            "marcan las ejecuciones que pasaron el límite de tiempo."
        ),
    )
    calidad = _tabla_de_archivo(
        "Calidad de la heurística voraz frente al óptimo de Held-Karp",
        "r4/tabla_calidad.csv",
        "Brecha en porcentaje: (heurística − Held-Karp) / Held-Karp × 100.",
        (
            "La brecha es siempre no negativa porque Held-Karp es óptimo; el "
            "promedio y el máximo crecen con k, que es la razón por la que el "
            "itinerario de la aplicación muestra los dos recorridos y su "
            "diferencia (R5-04)."
        ),
    )
    itinerario = _tabla_de_archivo(
        "Itinerario de un día (partida: C01 Plaza de Bolívar – Armenia)",
        "r4/tabla_itinerario.csv",
        "Desplazamientos y visitas en minutos; tiempo acumulado en horas.",
        (
            "El acumulado suma desplazamientos y visitas desde la partida. Al "
            "final se reportan el total de visitas, el de desplazamientos y la "
            "duración de la jornada, tal como pide el Anexo."
        ),
    )
    return {
        "id": "r4",
        "titulo": "Requerimiento 4 · Ruta óptima de recorrido",
        "tablas": [exactos, calidad, itinerario],
        "graficas": [
            {
                "titulo": "Tiempo (ms) frente a k para fuerza bruta y Held-Karp",
                "archivo": "r4/grafica_k_ms.png",
                "lectura": (
                    "Eje horizontal: k (lugares visitados, sin contar la partida); "
                    "eje vertical: tiempo en milisegundos, escala logarítmica. La "
                    "curva de la fuerza bruta se dispara al crecer k."
                ),
            }
        ],
        "enlaces": [],
    }
