"""T4 R3b — SciPy instalado: algoritmo, lenguaje y versión con fuente leída (R3-10).

Lee de la instalación local (sin red, GLOB-15):
- docstring instalado de ``scipy.spatial.ConvexHull`` (sección Notes), a
  través del módulo de referencia;
- ``COPYING_QHULL.txt`` del árbol de SciPy (Qhull © 1993-2020, autores);
- extensión compilada ``_qhull*.so`` (tipo de archivo y bibliotecas enlazadas).
Registra también la versión de SciPy instalada y el ``dtype`` de la entrada
que exige la biblioteca (``double``, según su propio docstring), dato que
explica la diferencia con la aritmética entera exacta de la versión propia
(R3-10/R3-17).

Este script NO importa ``scipy``: toma ``ConvexHull`` de
`quindio.envolvente.referencia` (único módulo que importa SciPy, excepción
GLOB-03) y localiza los archivos con ``importlib`` (GLOB-03, R3-12).

La cita del artículo (QuickHull, Barber-Dobkin-Huhdanpaa, ACM TOMS 22(4),
1996) es la registrada en `specs/R3.md` (Spec R3a, R3-04/R3-09) y en
`src/quindio/envolvente/referencia.py`; aquí solo se referencia.

Salidas: `resultados/r3/scipy_info_r3.json` y `resultados/r3/scipy_info_r3.md`.
Uso: .venv/bin/python experimentos/r3/scipy_info_r3.py
"""
import json
import platform
import re
import subprocess
import sys
from datetime import UTC, datetime
from importlib.metadata import version as version_instalada
from importlib.util import find_spec
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from quindio.envolvente.referencia import ConvexHull, version_scipy

RAIZ = Path(__file__).resolve().parents[2]
R3 = RAIZ / "resultados" / "r3"
SALIDA_JSON = R3 / "scipy_info_r3.json"
SALIDA_MD = R3 / "scipy_info_r3.md"


def _carpeta_spatial():
    """Ruta de scipy/spatial sin importar SciPy (GLOB-03)."""
    spec = find_spec("scipy")
    if spec is None or spec.origin is None:
        raise ValueError("SciPy no está instalado en este entorno")
    ruta = Path(spec.origin).resolve().parent / "spatial"
    if not ruta.is_dir():
        raise ValueError(f"no se encontró {ruta}")
    return ruta


def _ruta_relativa(ruta):
    """Ruta relativa a la raíz del repo (evita rutas de máquina en resultados)."""
    try:
        return str(Path(ruta).resolve().relative_to(RAIZ))
    except ValueError:
        return str(ruta)


def _doc_convexhull():
    """Cita literal de la sección Notes del docstring instalado."""
    doc = ConvexHull.__doc__ or ""
    inicio = doc.find("Notes")
    fin = doc.find("References", inicio)
    if inicio < 0 or fin < 0:
        raise ValueError("ConvexHull.__doc__ sin secciones Notes/References")
    notas = " ".join(doc[inicio:fin].split())
    return notas.split("-----", 1)[-1].strip()


def _licencia_qhull():
    """Primeras líneas útiles de COPYING_QHULL.txt del árbol instalado."""
    ruta = _carpeta_spatial() / "qhull_src" / "COPYING_QHULL.txt"
    if not ruta.is_file():
        raise ValueError(f"no se encontró {ruta}")
    lineas = [ln.strip() for ln in ruta.read_text(encoding="utf-8").splitlines()
              if ln.strip()]
    return _ruta_relativa(ruta).replace("\\", "/"), " ".join(lineas[:14])


def _extension():
    """Extensión compilada _qhull: nombre, tipo y bibliotecas enlazadas.

    En Linux/Mac la extensión es ``.so`` y se listan sus bibliotecas con ``ldd``;
    en Windows es ``.pyd`` y ``ldd`` no existe, así que el enlace se informa
    como no disponible.
    """
    carpeta = _carpeta_spatial()
    halladas = sorted(list(carpeta.glob("_qhull*.so")) + list(carpeta.glob("_qhull*.pyd")))
    if not halladas:
        raise ValueError("no se encontró la extensión compilada _qhull (.so o .pyd)")
    ruta = halladas[0]
    enlace = "no disponible"
    if ruta.suffix == ".so":
        try:
            salida = subprocess.run(["ldd", str(ruta)], capture_output=True,
                                    text=True, check=False)
            if salida.returncode == 0:
                # Sin direcciones de carga: la ficha debe ser reproducible.
                lineas = [re.sub(r"\s*\(0x[0-9a-f]+\)", "", ln).strip()
                          for ln in salida.stdout.splitlines()]
                enlace = " ".join(ln for ln in lineas
                                  if "=>" in ln or "linux-vdso" in ln)
        except OSError:
            enlace = "ldd no disponible"
    else:
        enlace = "no disponible en Windows (DLL de extensión .pyd; ldd no existe)"
    return {"archivo": _ruta_relativa(ruta).replace("\\", "/"),
            "bytes": ruta.stat().st_size,
            "tipo": "extensión compilada de CPython (no Python puro)",
            "bibliotecas_enlazadas": enlace}

def main():
    R3.mkdir(parents=True, exist_ok=True)
    version = version_instalada("scipy")
    ruta_licencia, cita_licencia = _licencia_qhull()
    extension = _extension()
    info_proyecto = version_scipy()
    if info_proyecto.get("version") != version:
        raise ValueError(f"referencia declara SciPy {info_proyecto.get('version')} "
                         f"!= instalada {version}")
    fuentes = [
        {"fuente": "docstring instalado de scipy.spatial.ConvexHull (Notes), "
                   "leído desde quindio.envolvente.referencia",
         "cita": _doc_convexhull()},
        {"fuente": f"archivo instalado {ruta_licencia}",
         "cita": cita_licencia},
        {"fuente": f"extensión compilada {extension['archivo']}",
         "cita": (f"{extension['tipo']}; bibliotecas enlazadas: "
                  f"{extension['bibliotecas_enlazadas']}")},
    ]
    datos = {
        "requerimiento": "R3-10",
        "biblioteca": "scipy.spatial.ConvexHull",
        "version_scipy": version,
        "algoritmo": "Qhull, que implementa QuickHull",
        "cita_algoritmo": ("Barber, Dobkin y Huhdanpaa, «The Quickhull algorithm "
                           "for convex hulls», ACM TOMS 22(4), 1996; cita "
                           "registrada en specs/R3.md (Spec R3a, R3-04/R3-09) y "
                           "en src/quindio/envolvente/referencia.py"),
        "lenguaje": ("núcleo de Qhull en C, empaquetado como extensión "
                     "compilada de CPython; la interfaz pública es Python"),
        "version_qhull_empacada": "Qhull © 1993-2020 (archivo COPYING instalado)",
        "entrada_que_exige": ("ndarray de double (docstring: points : ndarray of "
                              "floats / points : ndarray of double)"),
        "fuentes_leidas": fuentes,
        "extension": extension,
        "python": platform.python_version(),
        "fecha": datetime.now(UTC).isoformat(),
        "version_registrada_por_referencia": info_proyecto,
    }
    with open(SALIDA_JSON, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, indent=2, sort_keys=True, ensure_ascii=False)

    lineas = [
        "# R3-10 — algoritmo, lenguaje y versión de SciPy (instalación local)",
        "",
        f"- Biblioteca: `{datos['biblioteca']}`.",
        f"- Versión de SciPy instalada: `{datos['version_scipy']}`.",
        f"- Algoritmo: {datos['algoritmo']}.",
        f"- Cita del algoritmo: {datos['cita_algoritmo']}.",
        f"- Lenguaje: {datos['lenguaje']}.",
        f"- Qhull empaquetado: {datos['version_qhull_empacada']}.",
        f"- Entrada que exige SciPy: {datos['entrada_que_exige']}.",
        "",
        "## Fuentes leídas en la instalación",
        "",
    ]
    for i, fuente in enumerate(fuentes, 1):
        lineas.append(f"{i}. `{fuente['fuente']}`: {fuente['cita']}")
    lineas += ["", (f"Generado por `experimentos/r3/scipy_info_r3.py` "
                    f"(Python {datos['python']}).")]
    SALIDA_MD.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("scipy:", datos["version_scipy"], "| algoritmo:", datos["algoritmo"])
    print("JSON:", SALIDA_JSON)
    print("MD:", SALIDA_MD)


if __name__ == "__main__":
    main()
