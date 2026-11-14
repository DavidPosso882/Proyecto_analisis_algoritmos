"""Utilidades compartidas de R4b (UT-10): cargas, instancias y verificación.

Lee, sin modificarlos, la matriz de R2 (dirigida, sin simetrizar) y el
catálogo con ``duracion_min`` justificada (GLOB-22, DA-19). No importa OSMnx
ni NetworkX (R1-09) ni pandas. Los scripts de esta carpeta escriben solo en
``resultados/r4/`` y toda tabla o gráfica se genera desde esos archivos
(GLOB-08, EXP-09).

Convenio de tamaño: la instancia de curva/calidad tiene ``k`` lugares del
catálogo más Armenia como partida (R4-07: k lugares al azar «sin incluir la
partida»), es decir ``k + 1`` nodos en la matriz. El itinerario (R4-12) sigue
el mismo convenio y DA-22: la partida no se visita ni cuenta.
"""

import csv
import hashlib
import json
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ / "src"))

from quindio.medicion.arnes import (
    SEMILLA_MAESTRA,
    derivar_semilla,
    huella_maquina,
    versiones_libs,
)
from quindio.recorrido.exactos import fuerza_bruta, held_karp
from quindio.recorrido.voraz import vecino_mas_cercano

MATRIZ_CSV = RAIZ / "resultados" / "r2" / "matriz_tiempos.csv"
CATALOGO_CSV = RAIZ / "data" / "catalogo" / "catalogo.csv"
R4 = RAIZ / "resultados" / "r4"

PARTIDA = "C01"  # Armenia, plaza de Bolívar (§4). DA-22: no se visita ni cuenta.

KS_CURVA = tuple(range(5, 13))  # R4-07: k = 5, 6, ..., 12 (EV-13)
KS_CALIDAD = (5, 8, 10, 12)  # R4-11 / EXP-10
INSTANCIAS_CALIDAD = 5  # R4-11: al menos 5 instancias por k

TOLERANCIA = 1e-9  # DA-15: igualdad entre implementaciones propias
JORNADA_S = 11 * 3600  # R4-12: «cabe» sii total <= 11 h (DA-22)

# Índices estables de semilla (DA-17: semilla maestra 42 + índice).
INDICE_CURVA = 100
INDICE_CALIDAD = 200
INDICE_ITINERARIO = 900


def semilla_curva(k):
    """Semilla derivada de la instancia única de la curva en k (DA-17)."""
    return derivar_semilla(INDICE_CURVA + k)


def semilla_calidad(k, instancia):
    """Semilla derivada de la instancia ``instancia`` de calidad en k (DA-17)."""
    return derivar_semilla(INDICE_CALIDAD + 10 * k + instancia)


def semilla_itinerario():
    """Semilla derivada del sorteo de atractivos del itinerario (DA-17)."""
    return derivar_semilla(INDICE_ITINERARIO)


def cargar_matriz():
    """Devuelve (ids, celdas): ids en orden de cabecera y celdas en segundos."""
    with open(MATRIZ_CSV, newline="", encoding="utf-8") as fh:
        lector = csv.reader(fh)
        ids = next(lector)[1:]
        crudo = {fila[0]: fila[1:] for fila in lector}
    pos = {lid: i for i, lid in enumerate(ids)}
    celdas = [[float(crudo[a][pos[b]]) for b in ids] for a in ids]
    return ids, celdas


def cargar_catalogo():
    """Catálogo como diccionario id -> fila (duraciones GLOB-22)."""
    with open(CATALOGO_CSV, newline="", encoding="utf-8") as fh:
        return {fila["id"]: fila for fila in csv.DictReader(fh)}


def leer_csv(path):
    """Filas de un CSV como lista de diccionarios (vacía si no existe)."""
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def submatriz(celdas, pos, nodos):
    """Celdas dirigidas de ``nodos`` en ese orden (nodo 0 = partida)."""
    return [[celdas[pos[a]][pos[b]] for b in nodos] for a in nodos]


def duracion_s(fila_catalogo):
    """Duración de visita en segundos (cálculo interno en s, R4-13)."""
    return float(fila_catalogo["duracion_min"]) * 60.0


def costo_de(matriz, tour):
    """Costo del recorrido: suma de celdas dirigidas (R4-01)."""
    return sum(matriz[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))


def es_tour_valido(matriz, tour, partida=0):
    """El recorrido visita todo una vez y empieza y termina en la partida."""
    k = len(matriz)
    return (
        len(tour) == k + 1
        and tour[0] == partida
        and tour[-1] == partida
        and sorted(tour[:-1]) == list(range(k))
    )


def matriz_a_mano():
    """5 lugares asimétricos resueltos a mano: ciclo 0-1-2-3-4-0 cuesta 5.

    Toda arista del ciclo cuesta 1 y el resto 10, así que el óptimo es 5 y
    cualquier otro recorrido usa al menos una arista de costo 10.
    """
    k = 5
    return [
        [0.0 if i == j else (1.0 if j == (i + 1) % k else 10.0) for j in range(k)]
        for i in range(k)
    ]


def verificar_exactos():
    """Verificación previa (GLOB-06) de R4-06: bruta == Held-Karp == a mano."""
    matriz = matriz_a_mano()
    tour_bruta, total_bruta, _ = fuerza_bruta(matriz)
    tour_hk, total_hk, _ = held_karp(matriz)
    return (
        total_bruta == 5.0
        and total_hk == 5.0
        and es_tour_valido(matriz, tour_bruta)
        and es_tour_valido(matriz, tour_hk)
    )


def verificar_voraz(matriz, partida=0):
    """Verificación previa (GLOB-06) de R4-10: recorrido válido y costo exacto."""
    tour, total, _ = vecino_mas_cercano(matriz, partida)
    if not es_tour_valido(matriz, tour, partida):
        return False
    return abs(costo_de(matriz, tour) - total) <= TOLERANCIA * max(1.0, abs(total))


def huella_archivo(path):
    """sha256 del archivo de entrada entregado (EXP-11)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def huella_ids(ids):
    """sha256 del conjunto ordenado de lugares de una instancia (EXP-11)."""
    return hashlib.sha256("|".join(ids).encode("utf-8")).hexdigest()


def metadatos(**extra):
    """Metadatos de EXP-06/EXP-14 para cada archivo de resultados."""
    return {
        "fecha": datetime.now(UTC).isoformat(),
        "semilla_maestra": SEMILLA_MAESTRA,
        "python": platform.python_version(),
        "maquina": huella_maquina(),
        "versiones": versiones_libs(),
        "huella_matriz_tiempos": huella_archivo(MATRIZ_CSV),
        "huella_catalogo": huella_archivo(CATALOGO_CSV),
        **extra,
    }


def escribir_json(path, datos):
    """Escribe JSON UTF-8 con sangría (resultados legibles, GLOB-08)."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, indent=2, ensure_ascii=False, sort_keys=False)
        fh.write("\n")
