"""Aplicación web local (R5-01, DA-24): Flask con datos y cálculo propios.

Arranca con ``PYTHONPATH=src .venv/bin/python -m quindio.app`` (R5-01). No
descarga la red ni recalcula experimentos (R5-06): carga una sola vez el grafo
procesado, el catálogo y la matriz de R2-11 (R5-10: la carga se midió antes de
decidir que fuera única, sin otras cachés). Las rutas y el itinerario se
calculan en el momento con los módulos propios de R2 y R4 (R5-02, R5-04).
"""

import math

from flask import Flask, abort, render_template, request, send_from_directory

from . import resultados as tablero
from .calculo import (
    MAX_ATRACTIVOS,
    MIN_ATRACTIVOS,
    SeleccionInvalida,
    itinerario,
    ruta,
)
from .datos import RESULTADOS, Datos

PARTIDA_POR_DEFECTO = "C01"  # Armenia, plaza de Bolívar (DA-22)


def _duracion(segundos):
    """Segundos → «M min» o «H h MM min» cuando supera los 60 minutos."""
    total_min = round(segundos / 60.0)
    if total_min < 60:
        return f"{segundos / 60.0:.2f} min"
    horas, resto = divmod(total_min, 60)
    if resto == 0:
        return f"{horas} h"
    return f"{horas} h {resto:02d} min"


def _horas(segundos):
    """Segundos → horas con tres decimales (presentación)."""
    return f"{segundos / 3600.0:.3f}"


def crear_app():
    """Crea la aplicación Flask y carga los artefactos de solo lectura."""
    app = Flask(__name__, template_folder="plantillas")
    datos = Datos()
    app.extensions["quindio"] = datos
    app.jinja_env.filters["duracion"] = _duracion
    app.jinja_env.filters["horas"] = _horas

    @app.get("/")
    def inicio():
        return render_template(
            "inicio.html",
            datos=datos,
            n_atractivos=len(datos.atractivos()),
            n_vertices=len(datos.vertices),
        )

    @app.get("/ruta")
    def ver_ruta():
        origen = request.args.get("origen", PARTIDA_POR_DEFECTO)
        destino = request.args.get("destino", "A03")
        for lugar in (origen, destino):
            if lugar not in datos.idx:
                abort(400, description=f"lugar desconocido: {lugar}")
        resultado = ruta(datos, origen, destino)
        return render_template(
            "ruta.html",
            catalogo=datos.catalogo,
            origen=origen,
            destino=destino,
            resultado=resultado,
            datos_json=_json_ruta(resultado),
        )

    @app.get("/envolvente")
    def ver_envolvente():
        vertices = [
            {
                "orden": int(fila["orden"]),
                "nodo_id": int(fila["nodo_id"]),
                "x_utm": int(fila["x_utm"]),
                "y_utm": int(fila["y_utm"]),
                "lon": float(fila["lon"]),
                "lat": float(fila["lat"]),
            }
            for fila in datos.vertices
        ]
        return render_template(
            "envolvente.html",
            vertices=vertices,
            datos_json={"vertices": vertices},
        )

    @app.route("/itinerario", methods=["GET", "POST"])
    def ver_itinerario():
        partida = request.form.get("partida") or request.args.get(
            "partida", PARTIDA_POR_DEFECTO
        )
        seleccion = request.form.getlist("atractivos")
        contexto = {
            "catalogo": datos.catalogo,
            "atractivos": datos.atractivos(),
            "partida": partida,
            "seleccion": seleccion,
            "minimo": MIN_ATRACTIVOS,
            "maximo": MAX_ATRACTIVOS,
            "resultado": None,
            "error": None,
            "datos_json": None,
        }
        if request.method != "POST":
            return render_template("itinerario.html", **contexto)
        try:
            resultado = itinerario(datos, partida, seleccion)
        except SeleccionInvalida as exc:
            contexto["error"] = str(exc)
            return render_template("itinerario.html", **contexto), 400
        contexto["resultado"] = resultado
        contexto["datos_json"] = resultado
        return render_template("itinerario.html", **contexto)

    @app.get("/resultados")
    def ver_resultados():
        return render_template("resultados.html", bloques=tablero.bloques())

    @app.get("/resultados/archivo/<path:nombre>")
    def archivo_resultados(nombre):
        return send_from_directory(RESULTADOS, nombre)

    return app


def _json_ruta(resultado):
    """Payload del mapa: sin ``inf`` si el destino no fuera alcanzable."""
    alcanzable = resultado["alcanzable"] and math.isfinite(resultado["tiempo_s"])
    return {
        "origen": resultado["origen"],
        "destino": resultado["destino"],
        "tiempo_s": resultado["tiempo_s"] if alcanzable else None,
        "nodos_explorados": resultado["nodos_explorados"],
        "ruta_nodos": resultado["ruta_nodos"],
        "puntos": resultado["puntos"],
    }
