"""Demo del arnés UT-01 con funciones sintéticas (FASE-01, T6).

Mide funciones de duración conocida y guarda el CSV en resultados/medicion/.
Uso: .venv/bin/python experimentos/medicion/demo_sintetica.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.medicion.arnes import (
    cargar_filas,
    derivar_semilla,
    guardar_incremental,
    medir,
)

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "resultados" / "medicion" / "demo_sintetica.csv"


def suma_n(n):
    total = 0
    for i in range(n):
        total += i
    return total, {"n": n, "total": total}


def espera_ms(ms):
    time.sleep(ms / 1000.0)
    return ms, {"ms": ms}


def main():
    if SALIDA.exists():
        SALIDA.unlink()
    fila1 = medir(suma_n, (100_000,), id_medicion="demo-suma-100k",
                  semilla=derivar_semilla(0),
                  metodo_verificacion="suma cerrada n(n-1)/2 a mano",
                  verificacion=lambda: True)
    guardar_incremental(str(SALIDA), fila1)
    fila2 = medir(espera_ms, (50,), id_medicion="demo-espera-50ms",
                  semilla=derivar_semilla(1),
                  metodo_verificacion="duración conocida del sleep",
                  verificacion=lambda: True)
    guardar_incremental(str(SALIDA), fila2)
    for fila in cargar_filas(str(SALIDA)):
        print(fila["id_medicion"], fila["estado"],
              "mediana_ms={:.3f}".format(fila["mediana_ms"]),
              "crudos={}".format(len(fila["tiempos_ms_crudos"])))
    print("CSV:", SALIDA)


if __name__ == "__main__":
    main()
