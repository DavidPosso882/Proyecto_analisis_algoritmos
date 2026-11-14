"""Pruebas de la aplicación local R5 (UT-11): R5-01 a R5-08.

Cada bloque cubre el criterio de verificación del PLAN:

- R5-01: humo; la app arranca y sirve la pantalla principal sin error.
- R5-02: para un par del archivo de R2-08, ruta y tiempo de la app son iguales
  al módulo de R2 (cola de prioridad) y al ``tiempo_viaje_s`` del CSV.
- R5-03: los vértices dibujados son los del archivo R3-11 y su número coincide
  con la fila «Nodos de la red» de R3-08.
- R5-04: selección fija de 6 a 8 atractivos → recorridos y totales idénticos a
  R4, diferencia voraz − Held-Karp >= 0, y rechazo fuera de rango.
- R5-05: cada tabla y gráfica del Anexo R1–R4 se sirve y proviene de
  ``resultados/`` (GLOB-08).
- R5-06: con las funciones de descarga sustituidas por un doble que falla, la
  app arranca y responde.
- R5-07: el README trae ejecución, experimentos, versiones y datos.
- R5-08: la app solo importa módulos propios de R2/R4 y el marco; nunca
  NetworkX, OSMnx, SciPy, descarga ni medición.
"""

import ast
import csv
import json
import re
import sys
import types
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as version_instalada
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
APP = RAIZ / "src" / "quindio" / "app"
RESULTADOS = RAIZ / "resultados"
README = RAIZ / "README.md"
PARTIDA = "C01"

# R5-08: solo marco (Flask), biblioteca estándar y módulos propios de R2/R4.
PERMITIDOS = {
    "argparse",
    "csv",
    "flask",
    "json",
    "math",
    "pathlib",
    "quindio",
    "xml",
}
PROHIBIDOS = {
    "geopandas",
    "networkx",
    "numpy",
    "osmnx",
    "pandas",
    "requests",
    "scipy",
    "shapely",
    "urllib",
}
MODULOS_PROPIOS = {"quindio.caminos", "quindio.recorrido"}


def _filas(nombre):
    """Filas de un CSV de ``resultados/`` (solo lectura, GLOB-08)."""
    with open(RESULTADOS / nombre, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _json(nombre):
    """Contenido de un JSON de ``resultados/``."""
    return json.loads((RESULTADOS / nombre).read_text(encoding="utf-8"))


def _json_de(html, ident):
    """Bloque ``<script id=... type="application/json">`` de la página."""
    patron = (
        '<script id="' + re.escape(ident) + '" type="application/json">(.*?)</script>'
    )
    encontrado = re.search(patron, html, re.DOTALL)
    assert encontrado is not None, f"falta el bloque de datos {ident}"
    return json.loads(encontrado.group(1))


PARES_COLA = [f for f in _filas("r2/mediciones_anexo.csv") if f["version"] == "cola_prioridad"]
ITINERARIO_R4 = _json("r4/itinerario.json")


@pytest.fixture(scope="module")
def datos():
    """Artefactos que la app carga al arrancar (una vez por módulo)."""
    from quindio.app.datos import Datos

    return Datos()


@pytest.fixture(scope="module")
def cliente():
    from quindio.app import crear_app

    return crear_app().test_client()


# --- R5-01 -----------------------------------------------------------------


def test_humo_pantalla_principal(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    texto = respuesta.get_data(as_text=True)
    assert "Quindío" in texto
    assert "ruta" in texto and "envolvente" in texto and "itinerario" in texto


# --- R5-02 -----------------------------------------------------------------


@pytest.mark.parametrize(
    "par", PARES_COLA, ids=lambda p: f"{p['origen']}-{p['destino']}"
)
def test_ruta_igual_a_modulo_r2_y_al_csv(cliente, datos, par):
    from quindio.caminos.dijkstra import dijkstra_cola

    origen, destino = par["origen"], par["destino"]
    respuesta = cliente.get("/ruta", query_string={"origen": origen, "destino": destino})
    assert respuesta.status_code == 200
    cuerpo = _json_de(respuesta.get_data(as_text=True), "datos-ruta")

    tiempo_modulo, camino, explorados = dijkstra_cola(
        datos.n, datos.ady, datos.idx[origen], datos.idx[destino]
    )
    assert cuerpo["tiempo_s"] == float(par["tiempo_viaje_s"])  # CSV R2-08
    assert cuerpo["tiempo_s"] == tiempo_modulo  # módulo R2
    assert cuerpo["nodos_explorados"] == int(par["nodos_explorados"]) == explorados
    assert cuerpo["ruta_nodos"] == camino
    assert len(cuerpo["puntos"]) == len(camino)
    assert cuerpo["puntos"][0] == list(datos.coordenadas[datos.idx[origen]])
    assert cuerpo["puntos"][-1] == list(datos.coordenadas[datos.idx[destino]])


def test_ruta_muestra_mapa_y_tiempo(cliente):
    html = cliente.get("/ruta", query_string={"origen": "C01", "destino": "A03"})
    texto = html.get_data(as_text=True)
    assert 'id="mapa"' in texto
    assert "min" in texto  # tiempo de viaje en minutos para lectura humana
    assert 'id="tiempo-viaje"' in texto


def test_ruta_rechaza_lugar_desconocido(cliente):
    respuesta = cliente.get("/ruta", query_string={"origen": "ZZZ", "destino": "A03"})
    assert respuesta.status_code == 400


# --- R5-03 -----------------------------------------------------------------


def test_envolvente_desde_archivo_igual_a_fila_nodos(cliente):
    vertices = _filas("r3/vertices_red.csv")
    fila = {f["Conjunto de puntos"]: f for f in _filas("r3/tabla_anexo_r3.csv")}[
        "Nodos de la red"
    ]
    respuesta = cliente.get("/envolvente")
    assert respuesta.status_code == 200
    cuerpo = _json_de(respuesta.get_data(as_text=True), "datos-envolvente")

    assert len(cuerpo["vertices"]) == int(fila["Vértices de la envolvente"])
    assert len(cuerpo["vertices"]) == len(vertices)
    assert [str(v["nodo_id"]) for v in cuerpo["vertices"]] == [
        v["nodo_id"] for v in vertices
    ]
    assert [v["lat"] for v in cuerpo["vertices"]] == [float(v["lat"]) for v in vertices]


# --- R5-04 -----------------------------------------------------------------


def test_itinerario_igual_a_r4(cliente, datos):
    from quindio.recorrido.voraz import vecino_mas_cercano

    partida = ITINERARIO_R4["partida"]["id"]
    final = ITINERARIO_R4["final"]
    respuesta = cliente.post(
        "/itinerario",
        data={"partida": partida, "atractivos": list(reversed(final["atractivos"]))},
    )
    assert respuesta.status_code == 200
    cuerpo = _json_de(respuesta.get_data(as_text=True), "datos-itinerario")

    assert sorted(cuerpo["atractivos"]) == sorted(final["atractivos"])
    assert cuerpo["hk"]["tour_ids"] == final["tour_ids"]
    assert cuerpo["hk"]["desplazamientos_s"] == final["desplazamientos_s"]
    assert cuerpo["hk"]["visitas_s"] == final["visitas_s"]
    assert cuerpo["diferencia_s"] == pytest.approx(
        cuerpo["voraz"]["desplazamientos_s"] - cuerpo["hk"]["desplazamientos_s"]
    )
    assert cuerpo["diferencia_s"] >= 0

    nodos = cuerpo["nodos"]
    # La app usa la matriz dirigida de R2-11 tal cual (R5-08, R2-11).
    matriz = [
        [datos.matriz_seg[datos.matriz_pos[a]][datos.matriz_pos[b]] for b in nodos]
        for a in nodos
    ]
    _, total_voraz, _ = vecino_mas_cercano(matriz, 0)
    assert cuerpo["voraz"]["desplazamientos_s"] == total_voraz


@pytest.mark.parametrize("cantidad", [5, 9])
def test_itinerario_rechaza_cantidad_fuera_de_rango(cliente, cantidad):
    atractivos = [a for a in _atractivos() if a != PARTIDA][:cantidad]
    respuesta = cliente.post(
        "/itinerario", data={"partida": PARTIDA, "atractivos": atractivos}
    )
    assert respuesta.status_code == 400
    texto = respuesta.get_data(as_text=True)
    assert "6" in texto and "8" in texto


def test_itinerario_rechaza_atractivo_que_no_es_atractivo(cliente):
    atractivos = [a for a in _atractivos() if a != PARTIDA][:5] + ["C02"]
    respuesta = cliente.post(
        "/itinerario", data={"partida": PARTIDA, "atractivos": atractivos}
    )
    assert respuesta.status_code == 400


def test_itinerario_partida_por_defecto_es_armenia(cliente):
    texto = cliente.get("/itinerario").get_data(as_text=True)
    assert f'<option value="{PARTIDA}" selected>' in texto
    assert "Armenia" in texto
    assert "6 y 8" in texto


def test_itinerario_diferencia_no_negativa_en_otra_seleccion(cliente):
    atractivos = [a for a in _atractivos() if a != PARTIDA][:8]
    respuesta = cliente.post(
        "/itinerario", data={"partida": PARTIDA, "atractivos": atractivos}
    )
    assert respuesta.status_code == 200
    cuerpo = _json_de(respuesta.get_data(as_text=True), "datos-itinerario")
    assert cuerpo["diferencia_s"] >= 0
    assert len(cuerpo["nodos"]) == len(atractivos) + 1


def _atractivos():
    with open(
        RAIZ / "data" / "catalogo" / "catalogo.csv", newline="", encoding="utf-8"
    ) as fh:
        return [f["id"] for f in csv.DictReader(fh) if f["categoria"] == "atractivo"]


# --- R5-05 -----------------------------------------------------------------


def test_resultados_traen_las_tablas_del_anexo(cliente):
    texto = cliente.get("/resultados").get_data(as_text=True)
    cifras = _json("r1/cifras_r1a.json")["departamento"]
    t_componente = {f["id_medicion"]: f for f in _filas("r1/t_componente.csv")}
    cociente = _json("r2/cociente.json")

    # R1: dos tablas (tamaño antes/después y tiempo de la componente).
    assert str(cifras["V"]) in texto and str(cifras["E_multi"]) in texto
    assert str(cifras["Vc"]) in texto and str(cifras["Ec_multi"]) in texto
    for nombre in ("Radio de 2 km", "Radio de 20 km", "Departamento completo"):
        info = json.loads(t_componente[nombre]["info"])
        assert str(info["V_mas_E"]) in texto
    assert f'{float(t_componente["Departamento completo"]["mediana_ms"]):.3f}' in texto

    # R2: gráfica y tabla del cociente.
    assert "grafica_nodos_ms.png" in texto
    assert f'{cociente["mediana"]:.2f}' in texto
    assert f'{cociente["minimo"]:.2f}' in texto
    assert f'{cociente["maximo"]:.2f}' in texto

    # R3: tabla del Anexo.
    for fila in _filas("r3/tabla_anexo_r3.csv"):
        assert fila["Conjunto de puntos"] in texto
        assert f'{float(fila["Tiempo propio (ms)"]):.3f}' in texto

    # R4: gráfica, dos tablas e itinerario.
    assert "grafica_k_ms.png" in texto
    exactos = _filas("r4/tabla_exactos.csv")
    for fila in exactos:
        for columna in ("Tiempo fuerza bruta (ms)", "Tiempo Held-Karp (ms)"):
            if fila[columna]:  # vacío = ejecución no completada (R4-07)
                assert f'{float(fila[columna]):.3f}' in texto
        assert fila["estado_fuerza_bruta"] in texto
    for fila in _filas("r4/tabla_calidad.csv"):
        assert f'{float(fila["Brecha promedio (%)"]):.4f}' in texto
    for fila in _filas("r4/tabla_itinerario.csv"):
        if fila["Orden"] == "1":
            assert fila["Lugar"] in texto


def test_resultados_sirven_las_graficas_de_resultados(cliente):
    for nombre in ("r2/grafica_nodos_ms.png", "r4/grafica_k_ms.png"):
        respuesta = cliente.get(f"/resultados/archivo/{nombre}")
        assert respuesta.status_code == 200
        assert respuesta.mimetype == "image/png"
        assert respuesta.get_data() == (RESULTADOS / nombre).read_bytes()


def test_resultados_no_sirven_archivos_fuera_de_resultados(cliente):
    assert cliente.get("/resultados/archivo/..%2F..%2FREADME.md").status_code == 404
    assert cliente.get("/resultados/archivo/no_existe.csv").status_code == 404


# --- R5-06 -----------------------------------------------------------------


def test_app_arranca_con_descarga_que_falla(monkeypatch):
    import quindio.red as paquete_red
    import quindio.red.descarga as descarga_real

    def falla(*args, **kwargs):
        raise AssertionError("R5-06: la app no debe descargar la red")

    for nombre in dir(descarga_real):
        if not nombre.startswith("_") and callable(getattr(descarga_real, nombre)):
            monkeypatch.setattr(descarga_real, nombre, falla)

    class _DescargaQueFalla(types.ModuleType):
        def __getattr__(self, nombre):
            raise AssertionError(f"R5-06: la app importó la descarga ({nombre})")

    doble = _DescargaQueFalla("quindio.red.descarga")
    monkeypatch.setitem(sys.modules, "quindio.red.descarga", doble)
    monkeypatch.setattr(paquete_red, "descarga", doble, raising=False)

    from quindio.app import crear_app

    cliente = crear_app().test_client()
    for url in (
        "/",
        "/ruta?origen=C01&destino=A03",
        "/envolvente",
        "/itinerario",
        "/resultados",
    ):
        assert cliente.get(url).status_code == 200, url


def test_app_no_importa_descarga_ni_medicion():
    for ruta in sorted(APP.glob("*.py")):
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        importados = _importados(arbol)
        for nombre in importados:
            assert not nombre.startswith("quindio.red"), f"{ruta.name}: {nombre}"
            assert not nombre.startswith("quindio.medicion"), f"{ruta.name}: {nombre}"
            assert "descarga" not in nombre, f"{ruta.name}: {nombre}"


# --- R5-07 -----------------------------------------------------------------


def test_readme_tiene_ejecucion_experimentos_versiones_y_datos():
    texto = README.read_text(encoding="utf-8")
    for esperado in (
        "PYTHONPATH=src",
        "-m quindio.app",
        "Flask==",
        "python -m pytest",
        "ruff check",
        "experimentos/r1/descargar.py",
        "experimentos/r2/medir_r2.py",
        "experimentos/r3/medir_r3.py",
        "experimentos/r4/itinerario.py",
        "verificacion/",
        "data/crudo",
        "data/procesado",
        "data/catalogo",
        "resultados/",
        "teselas",
    ):
        assert esperado in texto, f"falta «{esperado}» en README"


def test_readme_fija_las_versiones_instaladas():
    texto = README.read_text(encoding="utf-8")
    assert f"Flask=={version_instalada('flask')}" in texto
    for paquete in ("pytest", "ruff", "matplotlib"):
        try:
            real = version_instalada(paquete)
        except PackageNotFoundError:  # pragma: no cover - entorno sin la herramienta
            continue
        assert re.search(rf"{paquete}=={re.escape(real)}", texto, re.IGNORECASE), paquete


# --- R5-08 -----------------------------------------------------------------


def test_app_solo_importa_modulos_permitidos():
    for ruta in sorted(APP.glob("*.py")):
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        for nombre in _importados(arbol):
            raiz = nombre.split(".")[0]
            assert raiz not in PROHIBIDOS, f"{ruta.name} importa {nombre}"
            assert raiz in PERMITIDOS, f"{ruta.name} importa {nombre}"
            if nombre.startswith("quindio."):
                assert any(
                    nombre == propio or nombre.startswith(propio + ".")
                    for propio in MODULOS_PROPIOS
                ), f"{ruta.name} importa {nombre}"


def test_calculo_solo_usa_modulos_propios():
    fuente = (APP / "calculo.py").read_text(encoding="utf-8")
    assert "dijkstra_cola" in fuente
    assert "held_karp" in fuente
    assert "vecino_mas_cercano" in fuente


def _importados(arbol):
    """Nombres de módulo importados (absolutos); las relativas se omiten."""
    nombres = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres.extend(alias.name for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and not nodo.level and nodo.module:
            nombres.append(nodo.module)
    return nombres
