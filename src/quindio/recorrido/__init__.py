"""Exporta los métodos del TSP (R4): exactos + voraz."""
from .exactos import fuerza_bruta, held_karp, tamano_tabla  # noqa: F401
from .voraz import vecino_mas_cercano  # noqa: F401
