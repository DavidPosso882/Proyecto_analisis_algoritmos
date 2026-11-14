"""Pesos distancia/tiempo por arista (R1-03, DA-09).

Velocidad con la imputación de la versión instalada (R1-18, osmnx 2.1.1
`routing.add_edge_speeds` con defaults): media de `maxspeed` por tipo de vía;
tipos sin ningún `maxspeed` toman la media global; convierte mph→kph;
colapsa listas (vía: primer elemento; maxspeed: media); exige algún dato o
`hwy_speeds`/`fallback` (aquí hay datos: red drive del Quindío).
`routing.add_edge_travel_times` calcula travel_time(s) = length / speed.
Se copian a `distancia_m` y `tiempo_viaje_s` (R1-03). El tiempo es una
estimación del modelo, no el tiempo real de recorrido.
"""
import math


def tiempo_viaje_s(distancia_m, speed_kph):
    """Puro y testeable: s = m / (km/h en m/s)."""
    if speed_kph <= 0:
        raise ValueError("velocidad no positiva")
    return distancia_m / (speed_kph * 1000.0 / 3600.0)


def aplicar_pesos(G):
    """Agrega speed_kph/travel_time vía OSMnx y copia distancia_m/tiempo_viaje_s."""
    import osmnx

    osmnx.routing.add_edge_speeds(G)
    osmnx.routing.add_edge_travel_times(G)
    for _, _, _, datos in G.edges(keys=True, data=True):
        datos["distancia_m"] = float(datos["length"])
        datos["tiempo_viaje_s"] = float(datos["travel_time"])
    return G


def verificar_pesos(G, tolerancia_rel=1e-9):
    """R1-03: toda arista con ambos atributos finitos ≥ 0 y d/t == v (DA-15)."""
    n = 0
    for _, _, _, datos in G.edges(keys=True, data=True):
        d = datos["distancia_m"]
        t = datos["tiempo_viaje_s"]
        v_kph = datos["speed_kph"]
        assert math.isfinite(d) and d >= 0
        assert math.isfinite(t) and t >= 0
        v_ms = v_kph * 1000.0 / 3600.0
        assert math.isclose(d / t, v_ms, rel_tol=tolerancia_rel) if t > 0 else True
        n += 1
    return n
