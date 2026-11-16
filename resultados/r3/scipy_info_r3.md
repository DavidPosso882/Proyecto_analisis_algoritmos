# R3-10 — algoritmo, lenguaje y versión de SciPy (instalación local)

- Biblioteca: `scipy.spatial.ConvexHull`.
- Versión de SciPy instalada: `1.18.1`.
- Algoritmo: Qhull, que implementa QuickHull.
- Cita del algoritmo: Barber, Dobkin y Huhdanpaa, «The Quickhull algorithm for convex hulls», ACM TOMS 22(4), 1996; cita registrada en specs/R3.md (Spec R3a, R3-04/R3-09) y en src/quindio/envolvente/referencia.py.
- Lenguaje: núcleo de Qhull en C, empaquetado como extensión compilada de CPython; la interfaz pública es Python.
- Qhull empaquetado: Qhull © 1993-2020 (archivo COPYING instalado).
- Entrada que exige SciPy: ndarray de double (docstring: points : ndarray of floats / points : ndarray of double).

## Fuentes leídas en la instalación

1. `docstring instalado de scipy.spatial.ConvexHull (Notes), leído desde quindio.envolvente.referencia`: The convex hull is computed using the `Qhull library <http://www.qhull.org/>`__.
2. `archivo instalado .venv/Lib/site-packages/scipy/spatial/qhull_src/COPYING_QHULL.txt`: Qhull, Copyright (c) 1993-2020 C.B. Barber Arlington, MA and The National Science and Technology Research Center for Computation and Visualization of Geometric Structures (The Geometry Center) University of Minnesota email: qhull@qhull.org This software includes Qhull from C.B. Barber and The Geometry Center. Files derived from Qhull 1.0 are copyrighted by the Geometry Center.  The remaining files are copyrighted by C.B. Barber.  Qhull is free software and may be obtained via http from www.qhull.org.  It may be freely copied, modified, and redistributed under the following conditions:
3. `extensión compilada .venv/Lib/site-packages/scipy/spatial/_qhull.cp314-win_amd64.pyd`: extensión compilada de CPython (no Python puro); bibliotecas enlazadas: no disponible en Windows (DLL de extensión .pyd; ldd no existe)

Generado por `experimentos/r3/scipy_info_r3.py` (Python 3.14.0).
