"""T3+T4 R3b — tabla del Anexo (R3-08) y archivo de vértices (R3-11).

Lee SOLO `resultados/r3/mediciones.csv`, `resultados/r3/entradas_r3.json` y
`resultados/r3/scipy_info_r3.json` (GLOB-08): no vuelve a medir. Genera

- `resultados/r3/tabla_anexo_r3.csv` con las columnas del Anexo
  («Conjunto de puntos», n, «Vértices de la envolvente», «Tiempo propio (ms)»,
  «Tiempo SciPy (ms)», Cociente) más `generados` (DA-18);
- `resultados/r3/tabla_anexo_r3.md`, la misma tabla para el documento;
- comprueba el archivo de vértices de la red (R3-11) y la ficha de SciPy.

Verificaciones (R3-08, R3-10, R3-11): vértices propio == SciPy en cada fila,
misma `n` y misma huella de entrada entre las dos versiones, Cociente
recalculable desde las dos columnas de tiempo (DA-18: propio ÷ SciPy) y
conteo de vértices del archivo igual a la fila «Nodos de la red».

Uso: .venv/bin/python experimentos/r3/tablas_r3.py
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.envolvente.quickhull import cross, redondear_half_up
from quindio.envolvente.referencia import version_scipy
from quindio.medicion.arnes import cargar_filas

RAIZ = Path(__file__).resolve().parents[2]
R3 = RAIZ / "resultados" / "r3"
MEDICIONES = R3 / "mediciones.csv"
ENTRADAS = R3 / "entradas_r3.json"
SCIPY_INFO = R3 / "scipy_info_r3.json"
VERTICES = R3 / "vertices_red.csv"
TABLA_CSV = R3 / "tabla_anexo_r3.csv"
TABLA_MD = R3 / "tabla_anexo_r3.md"

COLUMNAS = ["Conjunto de puntos", "n", "Vértices de la envolvente",
            "Tiempo propio (ms)", "Tiempo SciPy (ms)", "Cociente", "generados"]
CONJUNTOS = (("red", "Nodos de la red"),
             ("cuadrado_1000", "Cuadrado, 1 000 puntos"),
             ("cuadrado_10000", "Cuadrado, 10 000 puntos"),
             ("cuadrado_50000", "Cuadrado, 50 000 puntos"))


def _comprobar_mediciones(por_id, entradas):
    """R3-07/R3-08: misma entrada entera, n tras dedup y vértices iguales."""
    esperados = {f"{clave}:{version}" for clave, _ in CONJUNTOS
                 for version in ("propio", "scipy")}
    if set(por_id) != esperados:
        raise ValueError(f"mediciones faltantes o sobrantes: "
                         f"{sorted(set(por_id) ^ esperados)}")
    filas = []
    for clave, nombre in CONJUNTOS:
        propio = por_id[f"{clave}:propio"]
        scipy = por_id[f"{clave}:scipy"]
        for fila in (propio, scipy):
            if fila["estado"] != "ok" or len(fila["tiempos_ms_crudos"]) != 5:
                raise ValueError(f"{fila['id_medicion']}: estado o crudos inválidos "
                                 "(EXP-03/EXP-08)")
        ref = entradas["conjuntos"][clave]
        if not (propio["info"]["n"] == scipy["info"]["n"] == ref["n"]):
            raise ValueError(f"{nombre}: n distinta entre versiones o testigo")
        if propio["info"]["generados"] != ref["generados"]:
            raise ValueError(f"{nombre}: generados distinto del testigo")
        vertices = propio["info"]["vertices"]
        if not (vertices == scipy["info"]["vertices"] == ref["vertices"]
                == propio["info"]["vertices_scipy"]
                == scipy["info"]["vertices_scipy"]):
            raise ValueError(f"{nombre}: vértices propio != SciPy (R3-08)")
        if not (propio["info"]["vertices_iguales_scipy"]
                and scipy["info"]["vertices_iguales_scipy"]):
            raise ValueError(f"{nombre}: falta la comprobación de vértices (R3-05)")
        if not (propio["huella_entrada"] == scipy["huella_entrada"]
                == ref["huella_entrada"]
                == propio["info"]["huella_conjunto"]):
            raise ValueError(f"{nombre}: huella de entrada distinta (EXP-11, R3-07)")
        t_propio = f"{propio['mediana_ms']:.3f}"
        t_scipy = f"{scipy['mediana_ms']:.3f}"
        # Cociente con los dos valores tal como se muestran (recalculable, R3-08).
        cociente = f"{float(t_propio) / float(t_scipy):.2f}"
        filas.append({
            "Conjunto de puntos": nombre,
            "n": ref["n"],
            "Vértices de la envolvente": vertices,
            "Tiempo propio (ms)": t_propio,
            "Tiempo SciPy (ms)": t_scipy,
            "Cociente": cociente,
            "generados": ref["generados"],
        })
    return filas


def _escribir_tabla(filas):
    with open(TABLA_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(filas)
    with open(TABLA_CSV, encoding="utf-8") as fh:
        releidas = list(csv.DictReader(fh))
    if set(releidas[0]) != set(COLUMNAS):
        raise ValueError("columnas del Anexo reducidas o renombradas (GLOB-09)")
    if [r["Conjunto de puntos"] for r in releidas] != [n for _, n in CONJUNTOS]:
        raise ValueError("filas del Anexo faltantes o fuera de orden (R3-08)")
    for fila in releidas:  # R3-08: Cociente recalculable desde los dos tiempos
        cociente = float(fila["Tiempo propio (ms)"]) / float(fila["Tiempo SciPy (ms)"])
        if f"{cociente:.2f}" != fila["Cociente"]:
            raise ValueError(f"{fila['Conjunto de puntos']}: Cociente no recalculable")
    lineas = ["| " + " | ".join(COLUMNAS) + " |",
              "|" + "---|" * len(COLUMNAS)]
    for fila in releidas:
        lineas.append("| " + " | ".join(fila[c] for c in COLUMNAS) + " |")
    nota = ("\n\nTiempos en milisegundos (ms): mediana de 5 repeticiones (EXP-03). "
            "`n` = puntos tras deduplicar; `generados` = puntos antes de "
            "deduplicar (DA-18). Cociente = tiempo propio ÷ tiempo SciPy (DA-18), "
            "recalculable desde las dos columnas de tiempo. Vértices: idénticos "
            "entre la versión propia y SciPy en las cuatro filas (R3-08).\n")
    TABLA_MD.write_text("\n".join(lineas) + nota, encoding="utf-8")
    return releidas


def _comprobar_vertices(vertices_red):
    """R3-11: archivo con enteros UTM + lon/lat; conteo == fila Nodos."""
    if not VERTICES.is_file():
        raise ValueError(f"falta el archivo de vértices {VERTICES}")
    with open(VERTICES, encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    if len(filas) != vertices_red:
        raise ValueError(f"vértices del archivo {len(filas)} != fila Nodos "
                         f"{vertices_red} (R3-11)")
    if [int(f["orden"]) for f in filas] != list(range(len(filas))):
        raise ValueError("columna orden no consecutiva desde 0")
    puntos = [(int(f["x_utm"]), int(f["y_utm"])) for f in filas]
    if len(set(puntos)) != len(puntos):
        raise ValueError("vértices UTM repetidos en el archivo")
    n = len(puntos)
    giros = [cross(puntos[i], puntos[(i + 1) % n], puntos[(i + 2) % n])
             for i in range(n)]
    if not all(giro > 0 for giro in giros):
        raise ValueError("giros no estrictamente a la izquierda (CCW, R3-13)")

    from pyproj import Transformer

    trans = Transformer.from_crs("epsg:4326", "epsg:32618", always_xy=True)
    for fila, (x, y) in zip(filas, puntos):
        utm = trans.transform(float(fila["lon"]), float(fila["lat"]))
        if (redondear_half_up(utm[0]), redondear_half_up(utm[1])) != (x, y):
            raise ValueError(f"lon/lat no corresponden al entero UTM {x},{y} "
                             "(R3-11)")
        if not fila["nodo_id"]:
            raise ValueError("vértice sin nodo_id de origen")
    return len(filas)


def _comprobar_scipy(por_id):
    """R3-10: ficha con algoritmo, lenguaje, versión y fuentes leídas."""
    if not SCIPY_INFO.is_file():
        raise ValueError(f"falta la ficha {SCIPY_INFO}")
    with open(SCIPY_INFO, encoding="utf-8") as fh:
        info = json.load(fh)
    version = version_scipy()["version"]
    if info.get("version_scipy") != version:
        raise ValueError(f"versión de SciPy de la ficha {info.get('version_scipy')} "
                         f"!= instalada {version}")
    if not (info.get("algoritmo") and info.get("lenguaje")):
        raise ValueError("ficha de SciPy sin algoritmo o lenguaje (R3-10)")
    fuentes = info.get("fuentes_leidas") or []
    if not fuentes or any(not f.get("fuente") or not f.get("cita") for f in fuentes):
        raise ValueError("ficha de SciPy sin fuentes leídas (R3-10)")
    if (por_id["red:propio"]["versiones"].get("scipy") != version
            or por_id["red:scipy"]["versiones"].get("scipy") != version):
        raise ValueError("versión de SciPy distinta entre la ficha y las mediciones")
    return version


def main():
    por_id = {f["id_medicion"]: f for f in cargar_filas(str(MEDICIONES))}
    with open(ENTRADAS, encoding="utf-8") as fh:
        entradas = json.load(fh)
    filas = _comprobar_mediciones(por_id, entradas)
    releidas = _escribir_tabla(filas)
    red = next(r for r in releidas if r["Conjunto de puntos"] == "Nodos de la red")
    vertices = _comprobar_vertices(int(red["Vértices de la envolvente"]))
    version = _comprobar_scipy(por_id)
    for fila in releidas:
        print(f"{fila['Conjunto de puntos']}: n={fila['n']} "
              f"vértices={fila['Vértices de la envolvente']} "
              f"propio={fila['Tiempo propio (ms)']} ms "
              f"scipy={fila['Tiempo SciPy (ms)']} ms "
              f"cociente={fila['Cociente']}")
    print(f"R3-11: {vertices} vértices en {VERTICES} == fila Nodos")
    print(f"R3-10: SciPy {version} (ficha con fuentes leídas)")
    print("Tabla:", TABLA_CSV)
    print("Markdown:", TABLA_MD)


if __name__ == "__main__":
    main()
