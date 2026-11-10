"""Datos de solo lectura que la aplicación carga una vez al arrancar (R5-06).

Lee los artefactos ya calculados por R1–R4: el grafo procesado
(``data/procesado/``, R1-08), el catálogo con duraciones (``data/catalogo/``,
GLOB-22) y la matriz dirigida de R2 (``resultados/r2/matriz_tiempos.csv``,
R2-11). No descarga la red, no vuelve a medir y no recalcula la envolvente:
los vértices salen de ``resultados/r3/vertices_red.csv`` (R3-11, R5-03).

Solo biblioteca estándar: JSON, CSV y el XML del GraphML; el cálculo no usa
bibliotecas externas de grafos ni de cómputo científico (R5-08, GLOB-03).
"""

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PROCESADO = RAIZ / "data" / "procesado"
CATALOGO_CSV = RAIZ / "data" / "catalogo" / "catalogo.csv"
RESULTADOS = RAIZ / "resultados"

GRAFO_JSON = PROCESADO / "grafo_idx.json"
INDICES_JSON = PROCESADO / "indices.json"
COMPONENTE_GRAPHML = PROCESADO / "componente.graphml"
ASOCIACIONES_CSV = PROCESADO / "asociaciones.csv"
MATRIZ_CSV = RESULTADOS / "r2" / "matriz_tiempos.csv"
VERTICES_CSV = RESULTADOS / "r3" / "vertices_red.csv"

CATEGORIA_ATRACTIVO = "atractivo"


def leer_csv(ruta):
    """Filas de un CSV como lista de diccionarios."""
    with open(ruta, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def leer_json(ruta):
    """Contenido de un JSON."""
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def leer_csv_resultados(nombre):
    """CSV de ``resultados/`` por ruta relativa (GLOB-08)."""
    return leer_csv(RESULTADOS / nombre)


def leer_json_resultados(nombre):
    """JSON de ``resultados/`` por ruta relativa (GLOB-08)."""
    return leer_json(RESULTADOS / nombre)


def _cargar_grafo():
    """(n, ady): lista de adyacencia plana del grafo procesado (R1-09)."""
    grafo = leer_json(GRAFO_JSON)
    ady = tuple(tuple((int(v), float(t)) for v, t in vecinos) for vecinos in grafo["ady"])
    return int(grafo["n"]), ady


def _cargar_coordenadas(n):
    """(lon, lat) por índice contiguo, leídas del GraphML procesado (R1-08).

    Se recorre el XML una vez con ``iterparse``: la app no necesita el grafo
    completo, solo la posición de cada nodo para dibujar la ruta en el mapa.
    """
    idx_a_nodo = leer_json(INDICES_JSON)["idx_a_nodo"]
    claves = {}
    posicion = {}
    for evento, elemento in ET.iterparse(COMPONENTE_GRAPHML, events=("start", "end")):
        etiqueta = elemento.tag.rsplit("}", 1)[-1]
        if evento == "start" and etiqueta == "key":
            claves[elemento.get("id")] = elemento.get("attr.name")
        elif evento == "end" and etiqueta == "node":
            valores = {
                claves.get(hijo.get("key")): hijo.text
                for hijo in elemento
                if hijo.tag.rsplit("}", 1)[-1] == "data"
            }
            posicion[int(elemento.get("id"))] = (
                float(valores["x"]),
                float(valores["y"]),
            )
            elemento.clear()
    coordenadas = [posicion[nodo] for nodo in idx_a_nodo]
    if len(coordenadas) != n:
        raise ValueError("las coordenadas no cubren todos los nodos de la componente")
    return coordenadas


def _cargar_matriz():
    """(ids, celdas): matriz dirigida de R2-11 en segundos, sin simetrizar."""
    with open(MATRIZ_CSV, newline="", encoding="utf-8") as fh:
        lector = csv.reader(fh)
        ids = next(lector)[1:]
        crudo = {fila[0]: fila[1:] for fila in lector if fila}
    pos = {lid: i for i, lid in enumerate(ids)}
    celdas = [[float(crudo[a][pos[b]]) for b in ids] for a in ids]
    return ids, celdas


class Datos:
    """Artefactos de solo lectura que la app necesita para responder."""

    def __init__(self):
        self.catalogo = leer_csv(CATALOGO_CSV)
        self.por_id = {fila["id"]: fila for fila in self.catalogo}
        self.n, self.ady = _cargar_grafo()
        self.idx = {
            fila["id"]: int(fila["idx"]) for fila in leer_csv(ASOCIACIONES_CSV)
        }
        self.coordenadas = _cargar_coordenadas(self.n)
        self.matriz_ids, self.matriz_seg = _cargar_matriz()
        self.matriz_pos = {lid: i for i, lid in enumerate(self.matriz_ids)}
        # R5-03: los vértices se leen del archivo de R3-11, sin recalcular.
        self.vertices = leer_csv(VERTICES_CSV)

    def atractivos(self):
        """Filas del catálogo con categoría «atractivo» (R5-04)."""
        return [
            fila for fila in self.catalogo if fila["categoria"] == CATEGORIA_ATRACTIVO
        ]

    def nombre(self, lugar_id):
        """Nombre legible de un lugar del catálogo."""
        return self.por_id[lugar_id]["nombre"]

    def duracion_s(self, lugar_id):
        """Duración de la visita en segundos (cálculo interno en s, R4-13)."""
        return float(self.por_id[lugar_id]["duracion_min"]) * 60.0
