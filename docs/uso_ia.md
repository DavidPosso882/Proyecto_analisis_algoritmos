# Registro de uso de inteligencia artificial

Anexo del documento técnico (sección 8). Cada integrante registra las tareas en
las que usó IA. La responsabilidad sobre el contenido entregado es de las
personas del grupo: todo lo propuesto por la IA se revisó, se ejecutó y se
verificó antes de incluirlo.

## David Posso — planificación, verificación y cierre R1–R5 (2026-10-27 a 2026-11-04)

- **Herramienta:** el Gentleman (Pi), harness de desarrollo empleado como apoyo de redacción y generación de borradores de código.
- **Modo de uso:** la IA propuso el plan de trabajo, borradores de código y comandos; **David ejecutó las suites de prueba y los scripts de verificación, tomó las decisiones de diseño y alcance, probó la aplicación y firmó los entregables.**
- **Numeración:** UT-01 a UT-11 + R4-27/R5-13 según `specs/PLAN.md` y CONTRATOS.

### Aportes humanos (ejecutados y decididos por David)

- **Ejecución de la verificación completa.** Corrió `pytest` (suite total 100 pruebas) y `ruff check` sobre `src`, `tests`, `experimentos` y `verificacion`; ejecutó los siete scripts de verificación independiente (`r1_componente`, `r1_asociacion`, `r1_radios`, `r2_matriz`, `r3_envolvente`, `dijkstra_contra_bellmanford`, `tsp_oraculo_itertools`) y confirmó los resultados impresos (`R1-01/R1-04 OK`, `R2-06 OK`, `R3-05 OK`, `R4-06 OK`).
- **Prueba manual de la aplicación.** Abrió la app en el navegador y validó las pantallas de inicio, ruta, envolvente, resultados e itinerario, comprobando que los valores mostrados coincidieran con los archivos de `resultados/`.
- **Decisiones de alcance y diseño.** Fijó el catálogo canónico de 40 lugares (DA-06), la descarga única (DA-07), la proyección UTM 18N (DA-10), **la decisión de conservar y reportar A12-Acaime en lugar de sumarle la caminata** (DA-11, contra la alternativa que proponía la IA), los pares de muestreo (DA-14), el protocolo de medición (DA-16), el uso local sin publicación (DA-20/DA-24) y el entorno de pruebas (DA-25).
- **Firmas y responsabilidad de los entregables.** Firmó el documento técnico, la sustentación y el itinerario (R4-27, 2026-11-04), asumiendo la responsabilidad del contenido entregado, y revisó que las cifras del documento coincidieran con `resultados/`.

### Tareas asistidas por IA

| Tarea | Pedido a la IA | Qué produjo la IA | Decisión humana | Verificación (ejecutada por David) |
|---|---|---|---|---|
| FASE-00/FASE-01 (UT-01) | Arnés de medición con protocolo EXP-01/EXP-14 | `src/quindio/medicion/arnes.py` (proceso hijo spawn, perf_counter_ns, GC off, mediana 5, tope 5min, huella máquina/entrada) + 16-19 pruebas + demo sintética | Aceptado | `pytest tests/medicion/` 18-19 passed + CSV demo 2 filas ok + `ruff` limpio |
| R1a red (UT-02) | Descarga y modelo de red vial | Descarga única DA-07 (depto 8819/20184, componente 8803/20163) + pesos media-por-tipo + 5 redes medidas | Aceptado, firma DA-07/DA-10 por David | `verificacion/r1_componente.py` crudo==metadato + `resultados/r1/t_componente.csv` 5 filas + R1-01/R1-04 OK |
| R1b asociación (UT-04) | Asociar 40 lugares a la red | Asociación UTM 18N (barrido, desempate menor id) + reporte >500m; A12-Acaime fuera de red (DA-11 conservar+reportar) + grafo procesado | Aceptado | `verificacion/r1_asociacion.py` KDTree+geodésica OK, 10 lejanos; R1-08/R1-09 OK |
| R2a Dijkstra (UT-05) | Dijkstra propio x2 | `dijkstra.py` lineal O(V²) y cola O((V+E)logV) con invariante y ruta por predecesores + 13 pruebas + verificación Bellman-Ford propia | Aceptado | `pytest tests/caminos/` 13 passed + `verificacion/dijkstra_contra_bellmanford.py` R2-06 OK |
| R2b medición+matriz (UT-06) | Medir y matriz 40x40 | Pares vecindad ≤15km + 30 corridas + matriz dirigida + anexo CSV + gráfica + cociente mediano | Aceptado | `resultados/r2/mediciones.csv` 70 filas + matriz == NetworkX (tol 1e-9) + cociente ~150x |
| R3a envolvente (UT-07) | QuickHull entero | `quickhull.py` + referencia SciPy separada + degenerados a mano + R3-13 giros/contención/CCW | Aceptado | `pytest tests/envolvente/` 5/5 (red real == SciPy == Shapely, 14v) |
| R3b experimento (UT-08) | Envolvente en red real y sintética | Tabla Anexo 4 filas (8803/14 + 1k/17 + 10k/22 + 50k/34), cocientes 7.73/4.59/9.39/11.04 | Aceptado | `resultados/r3/tabla_anexo_r3.csv` + vértices archivo == fila Nodos |
| R4a exactos (UT-09) | TSP exacto | `exactos.py` fuerza bruta + Held-Karp DP + oráculo itertools confinado a `verificacion/` | Aceptado | `pytest tests/recorrido/` 7 passed + `tsp_oraculo_itertools.py` R4-06 OK k=4..7 |
| R4b calidad+itinerario (UT-10) | Curva y heurística voraz | Curva k=5..12 (bruta hasta k=11, HK hasta 12) + brechas 4.30/7.13/16.98/10.01 + itinerario 6 atractivos 10.081h cabe=sí | Aceptado | `resultados/r4/curva_exactos.csv` + `calidad_brechas.csv` + `itinerario.json` |
| R5 app (UT-11) | App Flask local | `src/quindio/app/` (rutas al momento R2/R4, envolvente desde archivo, tablas desde `resultados/`) + 39 pruebas + README | Aceptado, Flask 3.1.2 autorizado por David 2026-10-27 | `pytest tests/app/` 39 passed; suite total 100 passed + `ruff` limpio; prueba manual de las cinco pantallas |
| Docs y cierre (R4-27, GLOB-21/22/23) | Pulir docs contra resultados + guía sustentación | `documento_tecnico.md`, `sustentacion.md`, `guia_sustentacion_detallada.md`, `uso_ia.md`, `manifiesto.txt`, README + fix R2-08 `cola`→`cola_prioridad` | Firmado por David 2026-11-04; guía auditada 2026-11-14 | `pytest` 100 passed + `ruff` limpio; `itinerario.json:firma_r4_27=firmado` |

**Errores de la IA detectados y corregidos por David:**

- Una versión de los resultados de R2 rotulaba la variante con cola como `cola` en vez de `cola_prioridad`; David lo detectó al revisar las tablas contra los CONTRATOS y ordenó el fix (R2-08), aplicado sin volver a medir.
- Borradores iniciales del documento usaban cifras redondeadas en las tablas; la revisión contra `resultados/` obligó a regenerarlas desde los archivos.

**Lo que no se delegó a la IA:** la decisión sobre A12-Acaime (DA-11), la elección del catálogo canónico, las firmas humanas R4-27/R1-22-23/R2-23/R3-22-23/R4-26-28/GLOB-21-23, la corrida en limpio R5-13, la prueba manual de la aplicación y la revisión final de la sustentación.

## Juan Diego García — correcciones, segunda máquina y documento (2026-11-14 y 2026-11-15)

- **Herramienta:** Claude (Anthropic), en claude.ai, modelo Opus 5.5.
- **Modo de uso:** conversación. La IA no tuvo acceso al computador ni al
  repositorio con permisos de escritura; leyó una copia pública del repositorio
  y un zip del proyecto, propuso pasos, comandos, código y texto, y Juan Diego los
  ejecutó, revisó y subió con sus propios commits en la rama `correcciones-Diego`.
- **Numeración:** las tareas siguen la lista de 21 tareas acordada al inicio.

| Tarea | Pedido a la IA | Qué produjo la IA | Decisión humana | Verificación |
|---|---|---|---|---|
| 1 | Revisar el repositorio y probarlo a fondo | Lista de faltantes del repositorio (código de R1 y R3, scripts, pruebas, README); verificación independiente con NetworkX y SciPy en una copia | Aceptado; se pidió a David el proyecto completo | 6 scripts de `verificacion/` y `pytest` en Windows (línea base: 88 pasan, 12 fallan por `os.sysconf`) |
| 1 | Revisar lugares a más de 500 m | Detectó que A03 y A12 comparten nodo (0 s en la matriz) | Las coordenadas correctas de A13, F01 y F03 las buscó y verificó Diego en Google Maps; A15 y F07 se confirmaron como correctas | Recalculo de asociaciones: A13 589 m, F03 443 m, F01 273 m |
| 2–5 | Guardar resultados de Linux, subir el zip, unificar dependencias, README para Windows | Pasos de Git, `manifiesto.txt`, `requirements-dev.txt`, secciones del README | Aceptado | `pip install -r requirements-dev.txt`; `pytest` en `tests/app` |
| 3b | Fallo de pruebas en Windows | Diagnóstico (`os.sysconf` no existe en Windows) y función `_ram_mb` | Aceptado | 100 pruebas pasan; RAM leída: 16 149 MB |
| 8 | Qué hacer con Acaime (A12) | Tres opciones; **recomendó** sumar la caminata a la duración (opción A) | **Rechazada la recomendación:** el grupo eligió documentar la limitación (opción C) | Texto revisado en el catálogo y en R1.4 |
| 9–12 | Regenerar R1–R4 en Windows | Orden de ejecución, valores esperados y revisión de cada salida antes del commit | Aceptado; las mediciones las ejecutó Diego en su máquina | `verificacion/` completo, 100 pruebas, `instancias.csv` y `pares.csv` idénticos a Linux |
| 11a, 11c, 12a | Problemas de portabilidad encontrados al regenerar | Ficha de SciPy con `.pyd`, `.gitattributes`, JSON de R4 con `newline="\n"` | Aceptado | `ruff`; `entradas_r3.json` sin cambios tras normalizar |
| 13 | Prueba completa de la app | Lista de 10 casos con valores esperados | Aceptado; la prueba manual la hizo Diego | `docs/entorno/prueba_windows.md` |
| 14 | Explicar los «radios» de R1.3 | Análisis de los GraphML crudos, `verificacion/r1_radios.py` y texto | Aceptado | Script ejecutado en Windows: 8 403 + 383 nodos |
| 15–18 | Redactar R1.4, máquinas, comparación y actualizar cifras | Texto de las secciones 1.3, 2 (R1.4), 7.1 y cifras de R1–R4; `experimentos/comparar_maquinas.py` | Aceptado con correcciones: datos de la máquina Linux aportados por David; rango de R2 corregido (1,41 → 1,42) según el script | Script probado Linux contra Linux (razón 1,00) y ejecutado con los datos reales |
| 19 | Este registro | Borrador de este archivo | Revisado y completado por Diego | — |

**Errores de la IA detectados durante el trabajo:**

- Propuso un comando de verificación con un patrón mal formado (`"7,73 |"`)
  que coincidía con todas las líneas; se reemplazó por una búsqueda literal.
- Al proponer reemplazos de texto, uno dejó cortada una línea de R1; se detectó
  revisando la salida y se corrigió antes del commit.
- Algunas cifras de la comparación se calcularon primero con valores
  redondeados; el script generado desde los archivos corrigió una (rango de R2).

**Lo que no se delegó a la IA:** la verificación de coordenadas en el mapa, la
decisión sobre Acaime, la decisión de medir en una segunda máquina, la ejecución
de todas las mediciones y la revisión final del documento.