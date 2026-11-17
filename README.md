# Rutas del Paisaje Cultural Cafetero

Proyecto final de **Análisis de Algoritmos** (2026-2) · Ingeniería de Sistemas y
Computación · Universidad del Quindío.

Sistema de planificación de rutas sobre la red vial real del Quindío, con análisis
teórico y experimental de sus algoritmos: componente fuertemente conexa (R1),
Dijkstra en dos versiones (R2), envolvente convexa con QuickHull (R3), problema
del viajante asimétrico con fuerza bruta, Held-Karp y una heurística voraz (R4), y
una aplicación web local que muestra los resultados y calcula rutas e itinerarios
al momento (R5).

Todos los algoritmos evaluables son de **implementación propia en Python puro**.
Las bibliotecas externas solo se usan para descargar y preparar datos, graficar,
la interfaz y verificar resultados de forma independiente.

**Integrantes:** Juan Diego García Albarracín · David Alfonso Posso Cano ·
Sebastián David España García.

## Contenido

- [Requisitos y versiones](#requisitos-y-versiones)
- [Instalación](#instalación)
- [Ejecutar la aplicación](#ejecutar-la-aplicación)
- [Pruebas y análisis estático](#pruebas-y-análisis-estático)
- [Reproducir los experimentos](#reproducir-los-experimentos)
- [Datos y resultados](#datos-y-resultados)
- [Máquinas de medición](#máquinas-de-medición)
- [Problemas comunes en Windows](#problemas-comunes-en-windows)
- [Riesgos y limitaciones conocidas](#riesgos-y-limitaciones-conocidas)
- [Estructura del código](#estructura-del-código)
- [Documentación](#documentación)
- [Estado de la entrega](#estado-de-la-entrega)

## Requisitos y versiones

- Python **3.14** (probado con 3.14.8 en Linux y 3.14.0 en Windows 11).
- Git. En Windows, configurar `git config core.autocrlf false` antes de trabajar.
- Entorno virtual en `.venv/` (excluido del control de versiones).
- Conexión a internet solo para instalar paquetes y para el fondo del mapa de la
  aplicación.

El manifiesto de dependencias es [`manifiesto.txt`](manifiesto.txt): una línea por
paquete con su versión exacta y el requerimiento que lo usa. Hay dos archivos
instalables:

- [`requirements.txt`](requirements.txt): solo la aplicación (Flask y sus dependencias).
- [`requirements-dev.txt`](requirements-dev.txt): entorno completo (experimentos,
  pruebas y verificación).

| Paquete | Para qué |
|---|---|
| `Flask==3.1.2` | aplicación web local (R5) |
| `pytest==9.1.1` | pruebas automáticas |
| `ruff==0.17.3` | análisis estático |
| `osmnx==2.1.1` | descarga de la red y pesos (R1) |
| `networkx==3.7` | componente en R1 (vía OSMnx) y verificación independiente; nunca en los algoritmos propios |
| `numpy==2.5.4` | coordenadas enteras para la referencia de R3 y gráficas |
| `scipy==1.18.1` | referencia de la envolvente en R3 y verificación; nunca en los algoritmos propios |
| `matplotlib==3.11.2` | gráficas de R2 y R4 |
| `geopandas==1.2.0` | preparación de datos de R1 (requerida por OSMnx) |
| `pyproj==3.8.0` | proyección UTM 18N (EPSG:32618) |
| `shapely==2.2.0` | verificación de la envolvente |

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
git config core.autocrlf false        # evita convertir los saltos de línea de CSV y JSON
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt       # solo la aplicación
.venv\Scripts\python -m pip install -r requirements-dev.txt   # entorno completo
```

## Ejecutar la aplicación

Linux / macOS:

```bash
PYTHONPATH=src .venv/bin/python -m quindio.app
```

Windows (PowerShell):

```powershell
$env:PYTHONPATH = "src"
.venv\Scripts\python -m quindio.app
```

Abrir <http://127.0.0.1:5000>. Opciones: `--host` y `--puerto` (por ejemplo
`--puerto=8000`). El servidor escucha solo en `127.0.0.1`: es una demostración
local.

Sin `PYTHONPATH=src`, Python no encuentra el paquete `quindio`; es el error más
común.

| Ruta | Qué muestra | Requerimiento |
|---|---|---|
| `/` | resumen de los datos cargados y accesos a los módulos | R5 |
| `/ruta` | origen y destino del catálogo: ruta en el mapa y tiempo de viaje, calculados al momento con Dijkstra con cola de prioridad | R5.1 |
| `/envolvente` | polígono de la envolvente sobre el mapa, leído de `resultados/r3/vertices_red.csv` | R5.1 |
| `/itinerario` | partida (por defecto Armenia) y de 6 a 8 atractivos: recorridos de Held-Karp y del voraz, con desplazamientos, visitas, totales y diferencia | R5.1 |
| `/resultados` | tablas y gráficas de R1 a R4 leídas de `resultados/` | R5.1 |

## Pruebas y análisis estático

Linux / macOS:

```bash
# Toda la batería del proyecto (100 pruebas)
PYTHONPATH=src .venv/bin/python -m pytest -q

# Solo las pruebas de la aplicación
PYTHONPATH=src .venv/bin/python -m pytest tests/app -q

# Análisis estático
.venv/bin/ruff check src tests experimentos verificacion
```

Windows (PowerShell), con `$env:PYTHONPATH = "src"` definido en la misma ventana:

```powershell
.venv\Scripts\python -m pytest -q
.venv\Scripts\ruff check src tests experimentos verificacion
```

Las pruebas de `tests/app/` comparan lo que muestra la aplicación con los archivos
de resultados y con los módulos propios: tiempo de viaje contra
`resultados/r2/mediciones_anexo.csv` y `dijkstra_cola`, número de vértices contra
la tabla de R3 y recorridos del itinerario contra `resultados/r4/itinerario.json`.
También comprueban que la aplicación arranca y responde con las funciones de
descarga sustituidas por un doble que falla.

## Reproducir los experimentos

Los experimentos se ejecutan **fuera** de la aplicación, requieren el entorno
completo y escriben en `resultados/`. Todas las mediciones usan el arnés propio
(`src/quindio/medicion/arnes.py`): proceso hijo, 5 repeticiones, mediana,
semilla documentada, huella de la entrada y tope de 5 minutos.

En Windows se usan los mismos comandos cambiando `.venv/bin/python` por
`.venv\Scripts\python` (por ejemplo `.venv\Scripts\python experimentos\r1\procesar.py`).
Los scripts y el arnés son portables.

```bash
# R1 — descarga única, pesos, componente y grafo procesado
#      (la descarga solo hace falta si se borran los archivos de data/crudo/)
.venv/bin/python experimentos/r1/descargar.py
.venv/bin/python experimentos/r1/descargar_radios.py
.venv/bin/python experimentos/r1/medir_componente.py
.venv/bin/python experimentos/r1/procesar.py

# R2 — pares, mediciones de Dijkstra (cola y lineal) y matriz 40 × 40
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
.venv/bin/python experimentos/r4/ejemplo_voraz.py   # ejemplo de R4.5 (lee resultados, no mide)

# Comparación entre máquinas (lee resultados/linux/ y resultados/r1–r4; no mide)
.venv/bin/python experimentos/comparar_maquinas.py
```

Notas para volver a medir:

- Los scripts de medición son **reanudables**: no repiten las mediciones que ya
  están en su CSV (`resultados/r1/t_componente.csv`, `resultados/r2/mediciones.csv`,
  `resultados/r3/mediciones.csv`, `resultados/r4/curva_exactos.csv`,
  `resultados/r4/calidad_exactos.csv`). Para medir de nuevo, borrar ese CSV antes.
- `experimentos/r1/procesar.py` no sobrescribe `data/procesado/`: para
  regenerarlo, borrar antes los archivos de esa carpeta.
- La fuerza bruta con k = 11 tarda más de un minuto y con k = 12 se detiene a los
  5 minutos como «no completada»; la serie de R4 completa tarda entre 15 y 25
  minutos.

Verificación independiente (scripts aparte que pueden usar NetworkX, SciPy o
Shapely; nunca los módulos medidos ni la aplicación):

```bash
.venv/bin/python verificacion/r1_componente.py
.venv/bin/python verificacion/r1_asociacion.py
.venv/bin/python verificacion/r1_radios.py
.venv/bin/python verificacion/dijkstra_contra_bellmanford.py
.venv/bin/python verificacion/r2_matriz.py
.venv/bin/python verificacion/r3_envolvente.py
.venv/bin/python verificacion/tsp_oraculo_itertools.py
```

## Datos y resultados

| Directorio | Contenido |
|---|---|
| `data/crudo/` | redes descargadas de OpenStreetMap el 2026-10-27, sin modificar (GraphML), con su metadato de descarga |
| `data/procesado/` | componente fuertemente conexa con pesos (`componente.graphml`), índices contiguos (`indices.json`, `grafo_idx.json`), asociaciones lugar → nodo (`asociaciones.csv`) y metadato (V y E antes y después) |
| `data/catalogo/` | catálogo de 40 lugares (`catalogo.csv`), con fuente y verificación de cada coordenada y duración justificada de cada atractivo |
| `resultados/r1/` | tiempos de la componente y estimación de memoria |
| `resultados/r2/` | mediciones de Dijkstra, pares, vecindad, cociente entre versiones, gráfica y matriz de tiempos 40 × 40 |
| `resultados/r3/` | mediciones, ficha de SciPy, tabla del Anexo y vértices de la envolvente (`vertices_red.csv`) |
| `resultados/r4/` | instancias, curva de exactos, calidad de la heurística, itinerario y sus tablas y gráfica |
| `resultados/linux/` | mediciones originales de la máquina A (Linux), sin cambios, para la comparación |
| `resultados/comparacion/` | razón Windows / Linux por medición y resumen por requerimiento |
| `experimentos/` | scripts que generan `resultados/` |
| `verificacion/` | comprobaciones independientes con bibliotecas |

La aplicación lee **solo** `data/procesado/`, `data/catalogo/catalogo.csv`,
`resultados/r2/matriz_tiempos.csv` y `resultados/r3/vertices_red.csv`; las tablas
y gráficas de `/resultados` salen de `resultados/`. No escribe en ninguno de esos
directorios.

## Máquinas de medición

Cada requerimiento se midió completo en cada máquina; nunca se mezclan
mediciones de las dos en una misma tabla o gráfica.

| | Máquina A | Máquina B (resultados vigentes) |
|---|---|---|
| Procesador | AMD Ryzen 7 5800H (8 núcleos / 16 hilos) | Intel Core i5-1135G7, 11.ª gen. (4 núcleos / 8 hilos) |
| RAM | 16 GB DDR4-3200 | 16 GB |
| Sistema operativo | Fedora Linux 44 | Windows 11 Home Single Language (compilación 26200) |
| Python | 3.14.8 | 3.14.0 |
| Resultados | `resultados/linux/` | `resultados/r1` a `resultados/r4` |

Las versiones exactas instaladas en la máquina B están en
`docs/entorno/pip_freeze_windows.txt`.

## Problemas comunes en Windows

| Síntoma | Causa | Solución |
|---|---|---|
| `No module named 'quindio'` | falta `PYTHONPATH` | `$env:PYTHONPATH = "src"` en cada ventana nueva |
| «la ejecución de scripts está deshabilitada» al activar el entorno | política de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, o usar `.venv\Scripts\python` sin activar |
| `git status` marca archivos como modificados sin cambios reales | Git for Windows trae `core.autocrlf=true` | `git config core.autocrlf false` y `git update-index --refresh` |
| un archivo generado con `>` se ve ilegible en GitHub | PowerShell 5.1 escribe UTF-16 con `>` | usar `\| Out-File -Encoding ascii archivo.txt` |
| tildes mal mostradas en la consola | página de códigos | `chcp 65001` |

## Riesgos y limitaciones conocidas

- **Teselas del mapa.** El fondo del mapa son teselas de OpenStreetMap y la
  biblioteca Leaflet se carga desde un CDN, así que **el mapa requiere conexión a
  internet**. Sin conexión, la aplicación sigue mostrando el tiempo de viaje, los
  vértices y las tablas, pero no el fondo del mapa.
- **Tiempo de carga.** La aplicación carga los datos una sola vez al arrancar
  (0,72 s en la máquina A; la mayor parte es leer las coordenadas de
  `componente.graphml`). Después, una consulta de ruta tarda entre 7 y 18 ms y un
  itinerario de 6 a 8 atractivos entre 2 y 9 ms.
- **Datos no recalculados.** La aplicación es demostrativa: muestra los resultados
  guardados y no vuelve a medir. Si cambia un módulo de R2 a R4, hay que regenerar
  `resultados/` con los scripts antes de comparar.
- **Lugares lejos de la red.** Cinco lugares quedan a más de 500 m de su nodo
  (A12, A15, A03, A13 y F07); el nodo asociado funciona como punto de acceso por
  carretera y el tiempo calculado no incluye el último tramo a pie.
- **Nodos compartidos.** El Valle de Cocora (A03) y la Reserva Acaime (A12)
  comparten nodo, igual que Génova (C07) y la Cooperativa de Caficultores de
  Génova (T05); por eso la matriz asigna 0 s entre cada par. Es una limitación del
  modelo, que solo representa vías para carros, y está documentada en la sección
  R1.4 del documento técnico.

## Estructura del código

```text
src/quindio/
  red/           descarga, pesos, componente, asociaciones y grafo procesado (R1; nunca desde la app)
  caminos/       Dijkstra lineal y con cola de prioridad (R2)
  envolvente/    QuickHull entero (R3) y referencia SciPy aislada (la app no la importa)
  recorrido/     fuerza bruta, Held-Karp y vecino más cercano dirigido (R4)
  medicion/      arnés de medición (nunca desde la app)
  app/
    __init__.py      crear_app()
    __main__.py      python -m quindio.app
    datos.py         carga única de grafo, catálogo, matriz y vértices (solo lectura)
    calculo.py       ruta (Dijkstra con cola) e itinerario (Held-Karp + voraz) al momento
    resultados.py    tablas y gráficas de R1–R4 desde resultados/
    web.py           rutas Flask y filtros de presentación
    plantillas/      HTML (Jinja) de las pantallas
tests/           pruebas de pytest, espejo de src/quindio/
experimentos/    scripts que generan resultados/
verificacion/    comprobaciones independientes
specs/           plan, contratos y especificaciones R1–R5 (desarrollo guiado por especificaciones)
docs/            documento técnico, anexo de uso de IA y registros del entorno
```

## Documentación

- [`docs/documento_tecnico.md`](docs/documento_tecnico.md): arquitectura, análisis
  de cada requerimiento, conclusiones y anexo de uso de IA.
- [`docs/uso_ia.md`](docs/uso_ia.md): registro de uso de inteligencia artificial
  por integrante y por tarea.
- [`docs/entorno/`](docs/entorno/): versiones instaladas y registros de prueba en
  Windows.
- [`specs/`](specs/): plan del proyecto, contratos y especificación de cada
  requerimiento.

## Estado de la entrega

- Documento técnico y README revisados y aprobados por el grupo el **16 de
  noviembre de 2026**: Juan Diego García Albarracín, David Alfonso Posso Cano y
  Sebastián David España García.
- Pruebas: las 100 pruebas automáticas pasan y `ruff` no reporta errores (verificado en la máquina B).
- Ejecución de estos pasos en un entorno limpio (clonado desde cero): registrada
  en [`docs/entorno/ejecucion_limpia.md`](docs/entorno/ejecucion_limpia.md).