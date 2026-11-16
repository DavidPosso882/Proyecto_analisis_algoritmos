"""Asociación lugar → nodo por vecino euclidiano UTM (R1-06, R1-07, R1-12).

Mismo CRS en lugares y nodos (DA-10, EPSG:32618); orden de ejes explícito
lon,lat con always_xy (R1-12); barrido completo sin árbol espacial;
desempate por menor id de nodo; reporte estricto > 500 m (R1-07, DA-11).
"""
import csv
import math

EPSG_UTM = "epsg:32618"


def cargar_catalogo(path):
    """Lee id, latitud, longitud del catálogo canónico."""
    with open(path, encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    lugares = []
    for fila in filas:
        lugares.append({
            "id": fila["id"],
            "lat": float(fila["latitud"]),
            "lon": float(fila["longitud"]),
        })
    return lugares


def proyectar_puntos(lugares):
    """(lon, lat) → (x, y) UTM 18N con el mismo CRS que los nodos."""
    from pyproj import Transformer

    trans = Transformer.from_crs("epsg:4326", EPSG_UTM, always_xy=True)
    return [(l["id"],) + tuple(trans.transform(l["lon"], l["lat"])) for l in lugares]


def proyectar_nodos(G):
    """Nodos del grafo → dict nodo_id: (x, y) en EPSG:32618."""
    import osmnx

    P = osmnx.projection.project_graph(G, to_crs=EPSG_UTM)
    return {n: (float(d["x"]), float(d["y"])) for n, d in P.nodes(data=True)}


def asociar(puntos_utm, nodos_utm):
    """Barrido completo: por lugar, nodo de menor distancia; empate: menor id.

    puntos_utm: [(id, x, y), ...]; nodos_utm: {nodo: (x, y)} ordenados por id.
    Devuelve {id: (nodo, distancia_m)}.
    """
    ordenados = sorted(nodos_utm.items(), key=lambda kv: kv[0])
    resultado = {}
    for lid, px, py in puntos_utm:
        mejor_nodo, mejor_d = None, math.inf
        for nodo, (nx_, ny_) in ordenados:
            d = math.hypot(px - nx_, py - ny_)
            if d < mejor_d:  # estricto: el primer (menor id) gana empates
                mejor_d = d
                mejor_nodo = nodo
        resultado[lid] = (mejor_nodo, mejor_d)
    return resultado


def reportar_lejanos(asociaciones, umbral_m=500.0):
    """IDs con distancia ESTRICTAMENTE mayor que el umbral (R1-07, DA-05)."""
    return sorted(lid for lid, (_, d) in asociaciones.items() if d > umbral_m)


def en_bbox(puntos_utm, nodos_utm):
    """Todo lugar dentro del cuadro envolvente de la red (R1-12)."""
    xs = [xy[0] for xy in nodos_utm.values()]
    ys = [xy[1] for xy in nodos_utm.values()]
    fuera = [lid for lid, x, y in puntos_utm
             if not (min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys))]
    return fuera
