"""Componente fuertemente conexa (R1-04, R1-10).

Llamada literal exigida por el enunciado (EV-23). Interno (R1-16, verificado
en networkx 3.7): `strongly_connected_components` = Tarjan iterativo con las
mejoras de Tarjan y Zwick (no recursivo), lineal en V + E. Si el grafo ya es
fuertemente conexo retorna el mismo objeto sin copiar (R1-17); si no, nuevo
MultiDiGraph con la componente mayor.
"""
import osmnx as ox


def componente_mas_grande(G):
    """R1-04: llamada literal, sin sustituir ni strongly=False (R1-11)."""
    return ox.truncate.largest_component(G, strongly=True)
