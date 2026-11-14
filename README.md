# Proyecto final · Análisis de Algoritmos · Quindío

> **Estado: BORRADOR.** Texto preparado por el agente; la revisión y la firma
> humana están pendientes (REPO-11). La ejecución de estos pasos en un entorno
> limpio es una tarea humana (R5-13) y debe registrarse con fecha, sistema y
> resultado.

Aplicación local que muestra los resultados de los requerimientos 1 a 4 del
proyecto y calcula **al momento** la ruta entre dos lugares y el itinerario de
un día. Todo el cálculo usa los módulos propios del proyecto (Dijkstra con cola
de prioridad, Held-Karp, heurística voraz y QuickHull); no se descarga la red ni
se vuelven a medir experimentos al ejecutarla (R5-02, R5-04, R5-06, R5-08).

## Contenido

- [Requisitos y versiones](#requisitos-y-versiones)
- [Instalación](#instalación)
- [Ejecutar la aplicación](#ejecutar-la-aplicación)
- [Pruebas y análisis estático](#pruebas-y-análisis-estático)
- [Reproducir los experimentos](#reproducir-los-experimentos)
- [Datos y resultados](#datos-y-resultados)
- [Riesgos conocidos](#riesgos-conocidos)
- [Estructura del código](#estructura-del-código)
- [Problemas comunes en Windows](#problemas-comunes-en-windows)

## Requisitos y versiones

- Python **3.14** (probado con 3.14.8 en Linux y 3.14.0 en Windows 11).
- Entorno virtual en `.venv/` (excluido del control de versiones).
- El manifiesto único de dependencias es [`manifiesto.txt`](manifiesto.txt)
  (REPO-08): una línea por paquete con la versión exacta y el requerimiento que
  lo usa.

Versiones exactas instaladas y verificadas en este entorno:

| Paquete | Para qué |
|---|---|
| `Flask==3.1.2` | marco web local de la aplicación (R5, DA-24) |
| `pytest==9.1.1` | ejecutar las pruebas (DA-25) |
| `ruff==0.17.3` | análisis estático (DA-23) |
| `osmnx==2.1.1` | descarga única de la red en R1 |
| `networkx==3.7` | preparación de R1 y verificación independiente (nunca en el cálculo de la app) |
| `numpy==2.5.4` | apoyo numérico de R3 y de las gráficas |
| `scipy==1.18.1` | referencia de la envolvente en R3 (nunca en el cálculo de la app) |
| `matplotlib==3.11.2` | gráficas de R2 y R4 |
| `geopandas==1.2.0` | preparación de R1 (transitiva de OSMnx) |
| `pyproj==3.8.0` | proyección UTM 18N, EPSG:32618 (DA-10) |
| `shapely==2.2.0` | verificación de contenedores en R3 |

Dependencias transitivas de Flask 3.1.2 (no se usan directamente):
`blinker==1.9.0`, `click==8.5.0`, `itsdangerous==2.2.0`, `jinja2==3.1.6`,
`markupsafe==3.0.4`, `werkzeug==3.1.9`. Las del resto de paquetes están en el
manifiesto.

## Instalación


**Linux / macOS**

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt        # solo la aplicación
.venv/bin/pip install -r requirements-dev.txt    # entorno completo (experimentos, pruebas, verificación)
```

**Windows (PowerShell)**

```powershell
git config core.autocrlf false        # antes de trabajar: evita convertir los saltos de línea de CSV y JSON
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt       # solo la aplicación
.venv\Scripts\python -m pip install -r requirements-dev.txt   # entorno completo
```

La instalación de Flask 3.1.2 desde PyPI fue autorizada por el usuario
(2026-10-27) conforme a GLOB-15/GLOB-16 y DA-24.
```

La instalación de Flask 3.1.2 desde PyPI fue autorizada por el usuario
(2026-10-27) conforme a GLOB-15/GLOB-16 y DA-24.

## Ejecutar la aplicación

```bash
PYTHONPATH=src .venv/bin/python -m quindio.app
```
En Windows (PowerShell):

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python -m quindio.app
```

Abre <http://127.0.0.1:5000>. Opciones: `--host` y `--puerto`
(por ejemplo `PYTHONPATH=src .venv/bin/python -m quindio.app --puerto=8000`).
El servidor de desarrollo de Flask escucha solo en `127.0.0.1`: es una
demostración local, no se publica.

Pantallas:

| Ruta | Qué muestra | Requerimiento |
|---|---|---|
| `/` | resumen de datos cargados y accesos | R5-01 |
| `/ruta` | origen y destino del catálogo: ruta dibujada en el mapa y tiempo de viaje al momento (Dijkstra con cola) | R5-02 |
| `/envolvente` | polígono de la envolvente sobre el mapa del departamento, leído de `resultados/r3/vertices_red.csv` | R5-03 |
| `/itinerario` | partida (por defecto Armenia) y de 6 a 8 atractivos: recorrido de Held-Karp y del voraz, con desplazamientos, visitas, totales y diferencia | R5-04 |
| `/resultados` | tablas y gráficas de R1 a R4 leídas de `resultados/` | R5-05 |

Si intenta ejecutarla sin `PYTHONPATH=src`, Python no encontrará el paquete
`quindio`; ese es el error más común.

## Pruebas y análisis estático

```bash
# Pruebas de la aplicación (humo, integración contra R2/R3/R4, doble de descarga)
.venv/bin/python -m pytest tests/app -q

# Toda la batería del proyecto
.venv/bin/python -m pytest -q

# Análisis estático de la aplicación y de sus pruebas
.venv/bin/ruff check src/quindio/app tests/app

# Análisis estático de todo el repositorio
.venv/bin/ruff check src tests experimentos verificacion
```

Las pruebas de `tests/app/` comparan lo que muestra la aplicación con los
archivos de resultados y con los módulos propios: tiempo de viaje contra
`resultados/r2/mediciones_anexo.csv` y `dijkstra_cola` (R5-02), número de
vértices contra la fila «Nodos de la red» de R3 (R5-03), recorridos y totales
del itinerario contra `resultados/r4/itinerario.json` (R5-04). Con las
funciones de descarga sustituidas por un doble que falla, la aplicación arranca
y responde (R5-06).

En Windows (PowerShell), con `$env:PYTHONPATH = "src"` definido en la misma ventana:

```powershell
.venv\Scripts\python -m pytest -q
.venv\Scripts\ruff check src tests experimentos verificacion
```

## Reproducir los experimentos

En Windows se usan los mismos comandos cambiando `.venv/bin/python` por
`.venv\Scripts\python` (por ejemplo
`.venv\Scripts\python experimentos\r1\procesar.py`). Los scripts y el arnés
de medición son portables: el arnés usa procesos `spawn` y obtiene la RAM
también en Windows.

Los experimentos se ejecutan **fuera** de la aplicación y escriben en
`resultados/`. Requieren el entorno completo del manifiesto. Todas las
mediciones usan el arnés propio (`src/quindio/medicion/arnes.py`): 5
repeticiones, mediana, semilla efectiva y huella de entrada.

```bash
# R1 — descarga única, pesos, componente y grafo procesado
#      (requiere red y autorización registrada, GLOB-15/DA-07)
.venv/bin/python experimentos/r1/descargar.py
.venv/bin/python experimentos/r1/descargar_radios.py
.venv/bin/python experimentos/r1/medir_componente.py
.venv/bin/python experimentos/r1/procesar.py

# R2 — pares, mediciones de Dijkstra (cola y lineal) y matriz 40×40
.venv/bin/python experimentos/r2/elegir_pares.py
.venv/bin/python experimentos/r2/medir_r2.py
.venv/bin/python experimentos/r2/tablas_r2.py

# R3 — envolvente propia frente a SciPy, tabla del Anexo y vértices
.venv/bin/python experimentos/r3/medir_r3.py
.venv/bin/python experimentos/r3/scipy_info_r3.py
.venv/bin/python experimentos/r3/tablas_r3.py

# R4 — instancias, curva de exactos, calidad de la heurística e itinerario
.venv/bin/python experimentos/r4/instancias.py
.venv/bin/python experimentos/r4/medir_curva.py
.venv/bin/python experimentos/r4/medir_calidad.py
.venv/bin/python experimentos/r4/itinerario.py
.venv/bin/python experimentos/r4/tablas_r4b.py
```

Verificación independiente (scripts aparte; pueden usar NetworkX, SciPy o
Shapely, nunca los módulos medidos ni la aplicación):

```bash
.venv/bin/python verificacion/r1_componente.py
.venv/bin/python verificacion/r1_asociacion.py
.venv/bin/python verificacion/dijkstra_contra_bellmanford.py
.venv/bin/python verificacion/r2_matriz.py
.venv/bin/python verificacion/r3_envolvente.py
.venv/bin/python verificacion/tsp_oraculo_itertools.py
```

## Datos y resultados

| Directorio | Contenido |
|---|---|
| `data/crudo/` | redes descargadas sin modificar (GraphML) y su metadato de descarga |
| `data/procesado/` | componente fuertemente conexa con pesos (`componente.graphml`), índices contiguos (`indices.json`, `grafo_idx.json`), asociaciones lugar→nodo (`asociaciones.csv`) y metadato (V/E antes y después) |
| `data/catalogo/` | catálogo de 40 lugares (`catalogo.csv`), con duración de visita justificada para los atractivos |
| `resultados/r1/` | tabla de tiempos de la componente y cifras de tamaño de la red |
| `resultados/r2/` | mediciones de Dijkstra, cociente entre versiones, pares, vecindad, gráfica y matriz de tiempos 40×40 |
| `resultados/r3/` | tabla del Anexo, mediciones e información de SciPy, y vértices de la envolvente (`vertices_red.csv`) |
| `resultados/r4/` | instancias, curva de exactos, calidad de la heurística, itinerario y sus tablas |
| `experimentos/` | scripts que generan `resultados/` (R1 a R4 y la demo del arnés) |
| `verificacion/` | comprobaciones independientes con bibliotecas |

La aplicación lee **solo** `data/procesado/`, `data/catalogo/catalogo.csv`,
`resultados/r2/matriz_tiempos.csv` y `resultados/r3/vertices_red.csv`; las
tablas y gráficas de `/resultados` salen de `resultados/`. No escribe en
ninguno de esos directorios.

## Problemas comunes en Windows

| Síntoma | Causa | Solución |
|---|---|---|
| `No module named 'quindio'` | falta `PYTHONPATH` | `$env:PYTHONPATH = "src"` en cada ventana nueva |
| «la ejecución de scripts está deshabilitada» al activar el venv | política de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, o usar `.venv\Scripts\python` sin activar |
| `git status` marca archivos como modificados sin cambios reales | Git for Windows trae `core.autocrlf=true` | `git config core.autocrlf false` y `git update-index --refresh` |
| un archivo generado con `>` se ve ilegible en GitHub | PowerShell 5.1 escribe UTF-16 con `>` | usar `\| Out-File -Encoding ascii archivo.txt` |
| tildes mal mostradas en la consola | página de códigos | `chcp 65001` |

## Riesgos conocidos

- **Teselas del mapa (R5-09).** El fondo del mapa son **teselas** de
  OpenStreetMap y la biblioteca del mapa (Leaflet) se carga desde un CDN, así
  que **el fondo y el mapa requieren conexión a internet al usar la
  aplicación**; ese acceso a la red está documentado aquí conforme a GLOB-15.
  Sin conexión, la página sigue respondiendo y muestra el tiempo de viaje, los
  vértices y las tablas, pero no el fondo del mapa.
- **Tiempo de carga (R5-10).** Se midió antes de decidir cómo cargar los datos
  (GLOB-11). En esta máquina (Python 3.14.8): cargar todo una sola vez al
  arrancar tarda **0,72 s** (la mayor parte es recorrer
  `data/procesado/componente.graphml` para obtener las coordenadas de los
  nodos; el grafo y la matriz suman menos de 0,02 s). Con los datos ya
  cargados, una consulta de ruta tarda **7 a 18 ms** (mediana 9 ms), un
  itinerario de 6 a 8 atractivos **2 a 9 ms**, `/resultados` 4 ms y
  `/envolvente` 2 ms. No se añadió ninguna otra caché.
- **Datos no recalculados.** La aplicación es demostrativa: muestra los
  resultados guardados y no vuelve a medir (R5-06). Si cambia un módulo de
  R2–R4, hay que regenerar `resultados/` con los scripts de arriba antes de
  comparar.
- **Firmas.** Documento técnico y sustentación firmados por David Posso (2026-11-04); itinerario R4-27 firmado (A12 y A13 por mayor ahorro, 10,081 h). Pendiente honesto: ejecución en entorno limpio (R5-13); este README sigue **BORRADOR** hasta registrarla.

## Estructura del código

```text
src/quindio/
  app/
    __init__.py      crear_app()
    __main__.py      python -m quindio.app
    datos.py         carga única de grafo, catálogo, matriz y vértices (solo lectura)
    calculo.py       ruta (Dijkstra cola) e itinerario (Held-Karp + voraz) al momento
    resultados.py    tablas y gráficas de R1–R4 desde resultados/
    web.py           rutas Flask y filtros de presentación
    plantillas/      HTML (Jinja) de las cuatro pantallas
  caminos/           Dijkstra propio (R2, solo lectura desde la app)
  recorrido/         Held-Karp y voraz propios (R4, solo lectura desde la app)
  envolvente/        QuickHull propio (R3; la app no lo importa, R5-03)
  red/               descarga, pesos, componente y asociaciones (R1, nunca desde la app)
  medicion/          arnés de medición (EXP; nunca desde la app)
```
