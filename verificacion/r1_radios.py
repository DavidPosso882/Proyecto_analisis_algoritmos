"""R1-19 / DA-08: qué cubre cada «radio» de graph_from_point (dist_type="bbox").

OSMnx descargó las redes de 2, 5, 10 y 20 km con ``dist_type="bbox"`` (ver
``data/crudo/*.meta.json``): cada red es un CUADRADO de lado 2·r centrado en la
plaza de Bolívar de Armenia, no un círculo, y no se recorta al departamento.

Compara los ids de nodo de cada red con los de la red del departamento y
cuenta cuántos nodos del departamento caen dentro del cuadrado. Solo lee los
GraphML crudos con la biblioteca estándar (no importa OSMnx ni NetworkX); la
distancia al centro usa una aproximación equirectangular, suficiente para
contar nodos a esta escala.

Uso: python verificacion/r1_radios.py
"""
import math
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CRUDO = RAIZ / "data" / "crudo"
CENTRO = (4.53247, -75.67298)  # plaza de Bolívar, Armenia (catálogo C01)
M_LAT = 110574.0
M_LON = 111320.0 * math.cos(math.radians(CENTRO[0]))


def nodos(nombre):
    """{id: (lat, lon)} de un GraphML crudo."""
    claves, salida = {}, {}
    for evento, el in ET.iterparse(CRUDO / f"{nombre}.graphml", events=("start", "end")):
        etiqueta = el.tag.rsplit("}", 1)[-1]
        if evento == "start" and etiqueta == "key":
            claves[el.get("id")] = el.get("attr.name")
        elif evento == "end" and etiqueta == "node":
            datos = {claves.get(h.get("key")): h.text for h in el}
            salida[el.get("id")] = (float(datos["y"]), float(datos["x"]))
            el.clear()
    return salida


def dentro_del_cuadro(punto, r_m):
    return (abs((punto[0] - CENTRO[0]) * M_LAT) <= r_m
            and abs((punto[1] - CENTRO[1]) * M_LON) <= r_m)


def main():
    depto = nodos("departamento")
    print(f"departamento: {len(depto)} nodos")
    for r in (2, 5, 10, 20):
        red = nodos(f"radio_{r}km")
        del_depto = len(set(red) & set(depto))
        en_cuadro = sum(dentro_del_cuadro(p, r * 1000) for p in depto.values())
        print(f"radio {r} km (cuadro {2 * r}x{2 * r} km): {len(red)} nodos; "
              f"{del_depto} del departamento, {len(red) - del_depto} de otros departamentos; "
              f"cubre {en_cuadro} nodos del departamento ({100 * en_cuadro / len(depto):.1f} %)")
    lats = [p[0] for p in depto.values()]
    lons = [p[1] for p in depto.values()]
    print("distancia de Armenia a los bordes de la red del departamento (km): "
          f"N {(max(lats) - CENTRO[0]) * M_LAT / 1000:.1f}, "
          f"S {(CENTRO[0] - min(lats)) * M_LAT / 1000:.1f}, "
          f"E {(max(lons) - CENTRO[1]) * M_LON / 1000:.1f}, "
          f"O {(CENTRO[1] - min(lons)) * M_LON / 1000:.1f}")
    print("R1-19 OK")


if __name__ == "__main__":
    main()