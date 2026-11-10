"""Ejecuta la aplicación local: ``PYTHONPATH=src python -m quindio.app``.

El servidor de desarrollo de Flask escucha solo en 127.0.0.1: es una
demostración local (DA-24); publicarla no es requisito (R5-01).
"""

import argparse

from .web import crear_app


def main():
    analizador = argparse.ArgumentParser(description="Aplicación local de R5")
    analizador.add_argument("--host", default="127.0.0.1")
    analizador.add_argument("--puerto", type=int, default=5000)
    argumentos = analizador.parse_args()
    crear_app().run(host=argumentos.host, port=argumentos.puerto)


if __name__ == "__main__":
    main()
