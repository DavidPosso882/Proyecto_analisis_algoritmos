# Registro de uso de inteligencia artificial

Anexo del documento técnico (sección 8). Cada integrante registra las tareas en
las que usó IA. La responsabilidad sobre el contenido entregado es de las
personas del grupo: todo lo propuesto por la IA se revisó, se ejecutó y se
verificó antes de incluirlo.

## David Posso

> PENDIENTE: registrar herramienta, modelo, fechas y tareas (plan, R1–R5,
> documento) con el mismo formato de la tabla de abajo.

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