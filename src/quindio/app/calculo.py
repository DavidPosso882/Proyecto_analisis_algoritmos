"""Cálculo al momento de la app: solo los módulos propios de R2 y R4 (R5-08).

- Rutas: ``dijkstra_cola`` (cola de prioridad, O((V + E) log V)), cargado del
  grafo procesado en cada consulta (R5-02).
- Itinerario: ``held_karp`` (DP sobre subconjuntos, O(k²·2^k)) y
  ``vecino_mas_cercano`` (voraz), sobre la matriz dirigida de R2-11 (R5-04).

La envolvente no se calcula aquí: se lee del archivo de R3-11 (R5-03).
El cálculo no usa bibliotecas externas de grafos, de enrutamiento ni de cómputo
científico (R5-08).
"""

from quindio.caminos.dijkstra import dijkstra_cola
from quindio.recorrido.exactos import held_karp
from quindio.recorrido.voraz import vecino_mas_cercano

MIN_ATRACTIVOS = 6
MAX_ATRACTIVOS = 8


class SeleccionInvalida(ValueError):
    """Selección del itinerario que no cumple las reglas de R5-04."""


def ruta(datos, origen, destino):
    """Ruta y tiempo al momento con Dijkstra de cola (R5-02).

    Devuelve el tiempo en segundos, los nodos explorados, la secuencia de
    índices de la ruta y sus coordenadas (lon, lat) para el mapa.
    """
    tiempo_s, camino, explorados = dijkstra_cola(
        datos.n, datos.ady, datos.idx[origen], datos.idx[destino]
    )
    return {
        "origen": origen,
        "destino": destino,
        "tiempo_s": tiempo_s,
        "nodos_explorados": explorados,
        "ruta_nodos": camino,
        "puntos": [datos.coordenadas[i] for i in camino],
        "alcanzable": bool(camino),
    }


def itinerario(datos, partida, atractivos):
    """Itinerario de un día con Held-Karp y con el voraz (R5-04).

    Los atractivos se ordenan como en el catálogo para que el resultado no
    dependa del orden en que se marcaron; Held-Karp devuelve el óptimo, cuyo
    valor no depende de ese orden.
    """
    elegidos = _validar(datos, partida, atractivos)
    nodos = [partida, *elegidos]
    matriz = [
        [datos.matriz_seg[datos.matriz_pos[a]][datos.matriz_pos[b]] for b in nodos]
        for a in nodos
    ]
    tour_hk, total_hk, info_hk = held_karp(matriz, 0)
    tour_voraz, total_voraz, _ = vecino_mas_cercano(matriz, 0)
    return {
        "partida": partida,
        "nombre_partida": datos.nombre(partida),
        "atractivos": elegidos,
        "nodos": nodos,
        "hk": _detalle(datos, nodos, matriz, tour_hk, total_hk),
        "voraz": _detalle(datos, nodos, matriz, tour_voraz, total_voraz),
        "diferencia_s": total_voraz - total_hk,
        "entradas_tabla_hk": info_hk["entradas_tabla"],
    }


def _validar(datos, partida, atractivos):
    """Rechaza partida desconocida y selecciones fuera de 6 a 8 (R5-04)."""
    if partida not in datos.por_id:
        raise SeleccionInvalida(f"lugar de partida desconocido: {partida}")
    if len(atractivos) < MIN_ATRACTIVOS or len(atractivos) > MAX_ATRACTIVOS:
        raise SeleccionInvalida(
            f"debe elegir entre {MIN_ATRACTIVOS} y {MAX_ATRACTIVOS} atractivos "
            f"(eligió {len(atractivos)})"
        )
    if len(set(atractivos)) != len(atractivos):
        raise SeleccionInvalida("los atractivos no pueden repetirse")
    for lugar_id in atractivos:
        fila = datos.por_id.get(lugar_id)
        if fila is None:
            raise SeleccionInvalida(f"lugar desconocido: {lugar_id}")
        if fila["categoria"] != "atractivo":
            raise SeleccionInvalida(
                f"{lugar_id} no es un atractivo del catálogo "
                f"(categoría «{fila['categoria']}»)"
            )
        if lugar_id == partida:
            raise SeleccionInvalida("la partida no puede ser uno de los atractivos")
    return sorted(atractivos, key=datos.matriz_pos.__getitem__)


def _detalle(datos, nodos, matriz, tour, total_s):
    """Recorrido con sus desplazamientos, visitas y acumulado (R4-12)."""
    filas = []
    visitas_s = 0.0
    acumulado_s = 0.0
    for paso in range(1, len(tour)):
        desde, hasta = tour[paso - 1], tour[paso]
        regreso = paso == len(tour) - 1
        lugar_id = nodos[hasta]
        desplazamiento_s = matriz[desde][hasta]
        visita_s = 0.0 if regreso else datos.duracion_s(lugar_id)
        visitas_s += visita_s
        acumulado_s += desplazamiento_s + visita_s
        filas.append(
            {
                "orden": "Regreso" if regreso else paso,
                "id": lugar_id,
                "lugar": datos.nombre(lugar_id),
                "desplazamiento_s": desplazamiento_s,
                "visita_s": None if regreso else visita_s,
                "acumulado_s": acumulado_s,
            }
        )
    return {
        "tour_ids": [nodos[i] for i in tour],
        "desplazamientos_s": total_s,
        "visitas_s": visitas_s,
        "jornada_s": total_s + visitas_s,
        "filas": filas,
    }
