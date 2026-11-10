# PLAN — Rutas del Paisaje Cultural Cafetero

Destino previsto: `specs/PLAN.md`. Fija las decisiones de implementación. Los requisitos académicos y los valores evaluables siguen en `Proyecto_final_2026-2.md` y `Anexo_proyecto.md`; este plan los referencia y no los sustituye.

**Convenciones.** `[ENUNCIADO]` exigencia del enunciado o del anexo. `[PLAN]` decisión de ingeniería de este plan. `[PROPUESTA]` recomendación no vinculante hasta resolver su `DA-xx`. `[REC]` recomendación técnica a investigar; no es criterio de aceptación. `[HUMANA]` tarea que solo una persona puede completar; el agente no la declara cumplida. PROPUESTO: comando, herramienta o biblioteca no citada literalmente en el enunciado; su existencia y versión no se comprobaron en el entorno. `EV-xx` (evidencia) y `UT-xx` (unidad de trabajo) son IDs auxiliares. Citas: `archivo §sección, ítem`; material de clase: `archivo, Parte n, diapositiva m`. Los `.md` del proyecto no tienen paginación: se cita sección e ítem. Formato de las reglas: `**ID:** Orden. Verificación: método.`

## 0. Evidencia previa (Fase 1)

### 0.1 Documentos de autoridad

| Orden | Archivo | Autoridad | Lectura |
|---|---|---|---|
| 1 | `Proyecto_final_2026-2.md` | Fuente de verdad de requisitos y valores evaluables | Completo (§1–§8) |
| 2 | `Anexo_proyecto.md` | Complementa el enunciado: formato de tablas, archivos y gráficas | Completo |
| 3 | `Analisis_de_Algoritmos_03-06.md` | Convenciones y protocolos de clase; no sustituye al enunciado | Cuatro partes identificadas; contenido leído en las diapositivas citadas |

Partes del consolidado (cada una conserva su numeración de diapositivas):

| Parte | Título | Fuente declarada | Diapositivas | Contenido usado en este plan |
|---|---|---|---|---|
| 1 | Tiempo de ejecución de los algoritmos | `03 - Tiempo de ejecución.pdf` | 60 | Benchmarking y análisis (d.9–10); operaciones elementales (d.11–15); costo de métodos llamados (d.48–51) |
| 2 | Complejidad computacional y notación asintótica | `04 - Complejidad Computacional y notación asintótica.pdf` | 47 | Definición y convenciones de Big-O (d.10–13); regla de la suma y del límite (d.15–17); factorial y TSP (d.34); Θ y Ω (d.39) |
| 3 | Tiempo de ejecución de algoritmos recursivos | `05 - Analisis Algoritmos Recursivos.pdf` | 50 | Recurrencias por inducción y expansión (d.26–44); método maestro (d.45–48); sustitución y método iterativo (d.49) |
| 4 | Algoritmos de ordenamiento y búsqueda | `06 - Algoritmos de Ordenamiento y búsqueda.pdf` | 27 | Tabla de ordenamientos con Timsort (d.14); desbordamiento de `int` (d.23); única actividad de medición del material (d.25) |

Límites del consolidado: la Parte 3 no trata la recurrencia de valor de la programación dinámica (Held-Karp). La Parte 4 no contiene más protocolo experimental que la d.25. Ninguna parte define cómo medir en Python.

### 0.2 Inventario de los 8 complementarios

Los 8 archivos están cargados y se reconocen por nombre exacto; ninguno falta. Sus cabeceras indican que proceden de `A_FundaAn.pdf` (capítulos de libro), no de las presentaciones (DA-01).

- `01-conceptos-basicos.md | aporta contexto de calidad: §1.4 (documentar el código, control de versiones, estándar de programación) y §1.6 (verificabilidad, exactitud)`
- `02-analisis-de-algoritmos.md | aporta §2.4 (las optimizaciones pueden introducir errores; aplicarlas con cuidado) y §2.3.3 (anchos de tipo: int de 32 bits, double de 64 bits)`
- `03-tiempo-de-ejecucion.md | libro cap. 3; prevalece sobre la Parte 1 si hay divergencia (DA-02): §3.1 solo peor caso, §3.2 benchmarking, §3.3 operaciones elementales`
- `04-complejidad-computacional.md | libro cap. 4; prevalece sobre la Parte 2 (DA-02): §4.3.1 notación asintótica, §4.3.2 regla del límite`
- `05-recursividad.md | libro cap. 5; prevalece sobre la Parte 3 (DA-02): §5.4 análisis recursivo, §5.6 sustitución, §5.7 y Cuadro 5.2 recurrencias comunes; no trae el método maestro`
- `06-ordenamiento.md | libro cap. 6; prevalece sobre la Parte 4 (DA-02): §6.7 MergeSort y §6.8 QuickSort (recurrencias), §6.11 Cuadro 6.1; no trae protocolo de medición ni Timsort`
- `07-algoritmos-de-busqueda.md | DESCARTADO`
- `08-estructuras-de-datos.md | aporta §8.4: el orden de complejidad de cada operación depende de cómo se construye la estructura; no cubre colas de prioridad`

### 0.3 Tabla de valores críticos

Las secciones 1 a 6 usan únicamente valores de esta tabla. Los valores propuestos figuran como `NO ENCONTRADO`.

| ID | Valor literal | Archivo | Sección | R afectado | Estado |
|---|---|---|---|---|---|
| EV-01 | «al menos 40 lugares del departamento» | `Proyecto_final_2026-2.md` | §4, Catálogo de lugares | R1, R2, R4, R5 | Confirmado como mínimo; formulación distinta de «40 lugares» (DA-05) |
| EV-02 | Mínimos por categoría: 12 (Cabeceras municipales), 15 (Atractivos turísticos), 8 (Fincas cafeteras u hoteles rurales), 5 (Centros de acopio o trilladoras de café) | `Proyecto_final_2026-2.md` | §4, tabla de categorías | R1 | Confirmado |
| EV-03 | «Sus 12 municipios» | `Proyecto_final_2026-2.md` | §1 | R2 (municipios vecinos) | Confirmado |
| EV-04 | «a más de 500 m» | `Proyecto_final_2026-2.md` | §5, R1.4 | R1 | Confirmado |
| EV-05 | «UTM zona 18N» | `Proyecto_final_2026-2.md` | §5, R1.4 y R3 «Coordenadas» | R1, R3 | Confirmado |
| EV-06 | «con radios de 2, 5, 10 y 20 km» | `Proyecto_final_2026-2.md` | §5, R1.3 | R1 | Confirmado |
| EV-07 | «al menos 20 pares origen-destino del catálogo»; «la versión lineal con 10 de esos pares» | `Proyecto_final_2026-2.md` | §5, R2.1, viñeta 2 | R2 | Confirmado |
| EV-08 | «O(V²)»; «O((V + E) log V)» | `Proyecto_final_2026-2.md` | §5, R2.1 | R2 | Confirmado |
| EV-09 | «(al menos 40 × 40)» | `Proyecto_final_2026-2.md` | §5, R2.1, viñeta 4 | R2, R4 | Confirmado |
| EV-10 | «(1 000, 10 000 y 50 000 puntos, con semilla fija)» | `Proyecto_final_2026-2.md` | §5, R3.2 | R3 | Confirmado |
| EV-11 | «utilizar enteros de 64 bits para evitar desbordamientos» | `Proyecto_final_2026-2.md` | §5, R3 «Coordenadas» | R3 | Confirmado |
| EV-12 | «aumentar k desde 5 hasta 12, o hasta que una ejecución pase el límite de tiempo de la sección 6 si eso ocurre antes» | `Proyecto_final_2026-2.md` | §5, R4.1 | R4 | Formulación distinta de «k de 5 a 12» (DA-05) |
| EV-13 | Filas k = 5, 6, …, 12 | `Anexo_proyecto.md` | «Requerimiento 4», tabla de soluciones exactas | R4 | Confirmado |
| EV-14 | «Para k = 5, 8, 10 y 12, con al menos 5 instancias por cada k» | `Proyecto_final_2026-2.md` | §5, R4.3 | R4 | Confirmado |
| EV-15 | «entre 6 y 8 atractivos» | `Proyecto_final_2026-2.md` | §5, R4.4 y R5.1 | R4, R5 | Confirmado |
| EV-16 | «cabe en una jornada de 11 h» | `Proyecto_final_2026-2.md` | §5, R4.4 | R4 | Confirmado; borde en DA-22 |
| EV-17 | «la de Armenia (plaza de Bolívar) es el punto de salida y llegada por defecto del requerimiento 4» | `Proyecto_final_2026-2.md` | §4 | R4, R5 | Confirmado |
| EV-18 | «Cada medición se repite 5 veces y se reporta la mediana. Las ejecuciones de más de un minuto se miden una sola vez.» | `Proyecto_final_2026-2.md` | §6, ítem 3 | R1–R4 | Confirmado; conflicto con EV-30 (DA-03) |
| EV-19 | «si una ejecución pasa de 5 minutos, se detiene y se reporta como no completada» | `Proyecto_final_2026-2.md` | §6, ítem 7 | R1–R4 | Confirmado; conflicto con EV-31 (DA-04) |
| EV-20 | «Los tiempos se guardan en una misma unidad (milisegundos o nanosegundos).»; columna `tiempo_ms`; «Tiempo (ms)» | `Proyecto_final_2026-2.md`; `Anexo_proyecto.md` | §6, ítem 4; «Requerimiento 2», 3 y 4 | R1–R4 | Confirmado; el Anexo fija ms |
| EV-21 | «Los datos aleatorios se generan con una semilla fija, que se documenta.» | `Proyecto_final_2026-2.md` | §6, ítem 5 | R2, R3, R4 | Confirmado |
| EV-22 | «Las mediciones de un mismo requerimiento se hacen en la misma máquina.»; «Solo se mide el algoritmo» | `Proyecto_final_2026-2.md` | §6, ítems 1 y 2 | R1–R4 | Confirmado |
| EV-23 | `ox.truncate.largest_component(G, strongly=True)` | `Proyecto_final_2026-2.md` | §5, R1.3 | R1 | Confirmado |
| EV-24 | `scipy.spatial.ConvexHull` | `Proyecto_final_2026-2.md` | §5, R3.1 | R3 | Confirmado |
| EV-25 | Columnas `origen`, `destino`, `version`, `tiempo_viaje_s`, `nodos_explorados`, `tiempo_ms`; valores de `version`: «lineal / cola_prioridad» | `Anexo_proyecto.md` | «Requerimiento 2» | R2 | Confirmado |
| EV-26 | «en los 10 pares medidos con ambas» | `Anexo_proyecto.md` | «Requerimiento 2» | R2 | Confirmado |
| EV-27 | «una ejecución que pase el límite se marca como «no completada»» | `Anexo_proyecto.md` | «Requerimiento 4» | R4 | Confirmado |
| EV-28 | Pesos: R1 15 %, R2 20 %, R3 20 %, R4 25 %, R5 5 %, documento técnico 15 %. «40 % implementación correcta y verificada, 30 % análisis teórico […] y 30 % análisis experimental» | `Proyecto_final_2026-2.md` | §8 | R1–R4 | Confirmado |
| EV-29 | «Debe poder ejecutarse localmente siguiendo el README.» | `Proyecto_final_2026-2.md` | §5, R5.1 | R5 | Confirmado |
| EV-30 | «Repita cada medición 5 veces y reporte el promedio.» | `Analisis_de_Algoritmos_03-06.md` | Parte 4, diapositiva 25, ítem 3 | R1–R4 | Conflicto con EV-18 (DA-03) |
| EV-31 | «deberá calcular o deducir el resultado sin ejecutar el algoritmo» | `Analisis_de_Algoritmos_03-06.md` | Parte 4, diapositiva 25, nota final | R2, R4 | Conflicto con EV-19 (DA-04) |
| EV-32 | «se recomienda que los algoritmos se ejecuten bajo condiciones computacionales similares» | `Analisis_de_Algoritmos_03-06.md` | Parte 1, diapositiva 10 | R1–R4 | Convención de clase |
| EV-33 | Fila «Timsort»: mejor O(n), promedio O(n log n), peor O(n log n), memoria extra O(n) | `Analisis_de_Algoritmos_03-06.md` | Parte 4, diapositiva 14 | R3 | Convención de clase |
| EV-34 | «si la suma supera 2³¹ − 1»; «son necesarios 32 bits» (int) y «64 bits» (double) | `Analisis_de_Algoritmos_03-06.md`; `02-analisis-de-algoritmos.md` | Parte 4, diapositiva 23; §2.3.3 | R3 | Contexto |
| EV-35 | Quick sort, peor caso «O(n²)» frente a QuickSort «O(n log(n))» «considerando su peor caso» | `Analisis_de_Algoritmos_03-06.md`; `06-ordenamiento.md` | Parte 4, diapositiva 14; §6.11, Cuadro 6.1 | R3 | Divergencia (DA-02) |
| EV-36 | «T(n) = a T(n / b) + f(n)»; «T(n) = O(n^{log_b a} log n)» si f(n) es igual | `Analisis_de_Algoritmos_03-06.md` | Parte 3, diapositivas 45–46 | R3 | Convención de clase |
| EV-37 | «existe un entero n₀ y una constante c > 0 tales que, para todo entero n ≥ n₀: T(n) ≤ c · f(n)» | `Analisis_de_Algoritmos_03-06.md` | Parte 2, diapositiva 10 | R1–R4 | Convención de clase |
| EV-38 | Valor de la semilla maestra | — | — | R2, R3, R4 | NO ENCONTRADO (DA-17) |
| EV-39 | Tolerancia relativa propuesta: 10⁻⁹ | — | — | R2, R4 | NO ENCONTRADO; propuesta (DA-15) |
| EV-40 | Código EPSG propuesto para «UTM zona 18N»: 32618 | — | — | R1, R3 | NO ENCONTRADO; propuesta (DA-10) |
| EV-41 | Lado del cuadrado de R3.2; fórmula de la brecha de R4.3 | — | — | R3, R4 | NO ENCONTRADO (DA-18) |

## 1. Reglas globales

**GLOB-01:** Implementar todo el proyecto en Python: algoritmos, experimentos, verificaciones y aplicación [instrucción del usuario; `Proyecto_final_2026-2.md §3, «Lenguaje»` deja libre el lenguaje y exige uno solo para todos los algoritmos]. Verificación: búsqueda estática de archivos de código con extensión distinta de `.py`, excluyendo datos, documentación y activos de la interfaz; el resultado debe ser vacío.

**GLOB-02:** No usar funciones de biblioteca que resuelvan los algoritmos de implementación propia: Dijkstra (dos versiones), envolvente convexa por divide y vencerás, fuerza bruta, Held-Karp y heurística voraz [ENUNCIADO `§3, «Implementación propia»`; `§5, R2.1, R3.1, R4.1, R4.2`]. Verificación: búsqueda estática de importaciones y llamadas prohibidas (listas por requerimiento en la sección 3) sobre los módulos evaluables; falla si aparece alguna.

**GLOB-03:** Importar NetworkX, SciPy y Shapely solo desde scripts de verificación independientes y nunca desde módulos evaluables. Única excepción: `scipy.spatial.ConvexHull` en el módulo de referencia de R3, que el enunciado exige para comparar y medir [ENUNCIADO `§3, «Librerías»`; `§5, R3.1–R3.2`]. Verificación: búsqueda estática de `import` en todo el árbol; los scripts de verificación están en un directorio propio y ningún módulo evaluable los importa.

**GLOB-04:** Usar librerías solo para estructuras de apoyo y ordenamiento; investigar el costo de cada una, citar la fuente y sumarlo al análisis del algoritmo que la usa [ENUNCIADO `§3, «Implementación propia»`; método de suma de costos: `Analisis_de_Algoritmos_03-06.md`, Parte 1, diapositivas 48–51; contexto: `08-estructuras-de-datos.md §8.4`]. Verificación: la sección del documento técnico de cada R lista cada estructura u ordenamiento de biblioteca importado (lista generada por búsqueda estática) con costo y fuente; inspección de evidencias contra esa lista.

**GLOB-05:** Citar cada complejidad y cada dato del catálogo con autor y título o enlace en el mismo texto [ENUNCIADO `§3, «Fuentes»`; `§5` introducción]. No inventar fuentes: toda cita se abre y se lee; si no se pudo, marcarla `PENDIENTE-VERIFICACIÓN-HUMANA`. Verificación: inspección de que cada cita tiene autor y título o URL accesible; búsqueda del marcador `PENDIENTE-VERIFICACIÓN-HUMANA` en el texto final, que debe devolver cero coincidencias antes de la entrega.

**GLOB-06:** Verificar cada algoritmo antes de medirlo y antes de usar sus resultados [ENUNCIADO `§6, ítem 6`]. Verificación: el ejecutor de experimentos corre primero la verificación del algoritmo y aborta si falla; prueba (a crear) que introduce un fallo deliberado en un doble de prueba y comprueba el aborto.

**GLOB-07:** Generar los datos aleatorios con semilla fija y documentada, sin fuentes de aleatoriedad sin semilla [ENUNCIADO `§6, ítem 5`; EV-21]. Verificación: búsqueda estática de generadores aleatorios sin semilla explícita; prueba (a crear): dos ejecuciones con la misma semilla producen datos idénticos byte a byte.

**GLOB-08:** Guardar los resultados en CSV o JSON y generar toda tabla y gráfica solo desde esos archivos, con la unidad de tiempo indicada [ENUNCIADO `§6, ítem 8`]. Verificación: el script de generación lee solo archivos de resultados; prueba: borrar tablas y gráficas, regenerarlas y comprobar que las cifras coinciden con las de los archivos.

**GLOB-09:** Respetar los nombres de columna, filas y estructura que fija el anexo; las columnas pueden ampliarse, no reducirse [ENUNCIADO `Anexo_proyecto.md`, introducción]. Verificación: prueba de esquema por archivo y por tabla: columnas exigidas ⊆ columnas presentes, con nombres exactos.

**GLOB-10:** Acompañar cada tabla y gráfica con un párrafo que indique la unidad de tiempo y explique si lo medido coincide con lo esperado y, si no, por qué [ENUNCIADO `§6, ítem 8`]. Verificación: inspección con lista de comprobación por cada figura y tabla del Anexo, en el documento técnico y en la aplicación.

**GLOB-11:** Priorizar claridad, mantenibilidad y correctitud; no optimizar sin una medición que lo justifique; no añadir abstracciones, dependencias ni complejidad innecesarias [PLAN; `02-analisis-de-algoritmos.md §2.4`]. Verificación: revisión del diff: cada dependencia nueva consta en el manifiesto aprobado (REPO-08) y cada optimización cita en el registro del feature la medición anterior y posterior.

**GLOB-12:** Escribir el código para que cualquier integrante pueda explicarlo, modificarlo y verificarlo: docstring de módulo en español que enlace su `specs/R#.md`, nombres descriptivos, sin construcciones ofuscadas [ENUNCIADO `§3, «Inteligencia artificial»`; contexto: `01-conceptos-basicos.md §1.4`]. Verificación: búsqueda estática de que cada módulo evaluable tiene docstring de módulo con ese enlace; la comprobación humana ocurre en GLOB-24.

**GLOB-13:** Leer archivos e inspeccionar el repositorio sin consultar: listar, leer y buscar, y consultas de solo lectura del historial de control de versiones (PROPUESTO). Verificación: el registro de acciones de la sesión (conservado por el orquestador) contiene en esta categoría solo operaciones de lectura.

**GLOB-14:** Ejecutar sin consultar únicamente las verificaciones no destructivas que el usuario haya autorizado por escrito en el documento de feature: suite de pruebas, scripts de verificación y análisis estático, con comandos exactos fijados allí (DA-23). Ninguna verificación puede descargar, borrar ni regenerar datos. Verificación: los comandos ejecutados figuran en la lista autorizada; búsqueda estática de operaciones de red, borrado o escritura en `data/` dentro de los scripts de verificación.

**GLOB-15:** Consultar antes de acceder a la red: descargas con OSMnx, geocodificación, consulta web de documentación o fuentes y teselas del mapa. Indicar qué se solicitará, a qué servicio y dónde se guardará. Verificación: cada acceso a red del registro está precedido por una autorización registrada; búsqueda estática de que las llamadas de descarga existen solo en el módulo de preparación de datos designado.

**GLOB-16:** Consultar antes de instalar dependencias con pip (PROPUESTO): presentar la lista exacta con versiones y el requerimiento que las necesita, y usar un entorno aislado. Verificación: el manifiesto de dependencias (REPO-08) coincide con lo aprobado; búsqueda estática: ninguna importación de un paquete ausente del manifiesto.

**GLOB-17:** Consultar antes de borrar o regenerar datos existentes (`data/`, `resultados/`, cachés). No sobrescribir el grafo descargado ni su metadato de fecha. Verificación: suma de verificación de `data/crudo/` idéntica antes y después de cada sesión salvo autorización registrada; prueba (a crear): el escritor de datos crudos falla si el destino ya existe.

**GLOB-18:** Crear y modificar archivos sin consultar solo dentro del alcance de este plan: código, pruebas, especificaciones, resultados nuevos y documentación. No modificar `Proyecto_final_2026-2.md`, `Anexo_proyecto.md`, el material de clase ni el catálogo verificado por personas sin decisión humana registrada. Verificación: revisión del diff: ningún cambio en esos archivos.

**GLOB-19:** No crear commits ni ejecutar push sin autorización explícita del usuario para cada operación. Es una política deliberada del proyecto: ningún paso del flujo ODD ni modo de permisos de Gentle Shell la sustituye. Si un paso obligatorio del flujo exige commit o push, detenerse, señalar el conflicto y pedir autorización antes de ejecutarlo (DA-20). Verificación: inspección del historial: cada commit del agente, si existe, referencia una autorización registrada; sin autorización registrada no hay commits ni push del agente.

**GLOB-20:** No asumir que las confirmaciones destructivas están desactivadas; ante duda, pedir confirmación. Todo permiso no listado en GLOB-13 a GLOB-19 requiere decisión previa (DA-23); el silencio no autoriza. Verificación: inspección del registro de la sesión: ninguna acción fuera de las categorías autorizadas.

**GLOB-21 [HUMANA]:** Verificar las coordenadas del catálogo sobre un mapa [ENUNCIADO `§4`: «Las coordenadas se verifican en un mapa»]. El agente prepara por cada lugar una evidencia (enlace o imagen de mapa y coordenadas a revisar) y no marca ninguna coordenada como verificada. Verificación: cada fila del catálogo tiene los campos `verificada`, `verificada_por` y fecha, vacíos hasta que una persona los complete; el registro del agente no contiene escrituras en esos campos.

**GLOB-22 [HUMANA]:** Justificar la duración de visita de cada atractivo con una fuente o con un criterio definido por el grupo [ENUNCIADO `§4`]; preferir fuente citada (DA-19). El agente puede proponer fuentes candidatas y no fija duraciones. Verificación: cada atractivo tiene duración en minutos y un campo `justificacion_duracion` con fuente (autor y título o enlace) o criterio escrito; inspección de evidencias.

**GLOB-23 [HUMANA]:** Verificar que cada fuente citada existe y respalda lo afirmado (GLOB-05). Verificación: lista de comprobación firmada por una persona, con una fila por cita.

**GLOB-24 [HUMANA]:** Preparar y realizar la sustentación: cada integrante responde sobre cualquier parte del proyecto [ENUNCIADO `§7, «Sustentación»`; `§8, «Nota individual»`]. El agente puede preparar un resumen de evidencias por R y no certifica preparación alguna. Verificación: inspección: guion de sustentación por R con responsable humano; ninguna casilla de «preparada» marcada por el agente.

**GLOB-25:** Conservar el registro del uso de IA del agente para el anexo del documento técnico [ENUNCIADO `§3, «Inteligencia artificial»`; `§7`, documento técnico, ítem 4]: por tarea, herramienta y modelo, fecha, ID del plan, qué se pidió, qué se aceptó o rechazó y cómo se verificó. Verificación: el archivo del registro (REPO-07) existe y cada ID de tarea del documento de feature tiene una entrada con todos los campos (prueba de esquema).

**GLOB-26:** No declarar completada ninguna tarea [HUMANA]; mantener su estado `PENDIENTE` hasta que una persona lo registre. Verificación: la lista de tareas [HUMANA] (GLOB-21 a GLOB-24, R1-21 a R1-23, R2-23, R3-22, R3-23, R4-26 a R4-28, R5-13, R5-14) tiene estado y autor; el registro del agente no contiene cambios de estado.

**GLOB-27:** Mantener separados requisitos, decisiones del plan y recomendaciones: una `[PROPUESTA]` o `[REC]` no se convierte en criterio de aceptación sin autorización del usuario. Ante conflicto entre una convención de clase y el enunciado, prevalece el enunciado (DA-03, DA-04). Verificación: inspección del documento de feature: cada criterio cita un ID `[ENUNCIADO]` o `[PLAN]` y ninguno cita una `[PROPUESTA]` o `[REC]` no aprobada.

## 2. Orden de trabajo

### 2.1 Dependencias y unidades de trabajo

Flujo de datos: catálogo (UT-03) y red (UT-02) → asociación y grafo procesado (UT-04) → Dijkstra y matriz (UT-06) → R4 (UT-10) → aplicación (UT-11). R3 usa los nodos de la componente (UT-04). Toda medición usa el arnés UT-01.

| UT | Contenido | Depende de | Funcionalmente independiente de | Entrega |
|---|---|---|---|---|
| UT-00 | Contratos de datos (`specs/CONTRATOS.md`), estructura del repositorio, manifiesto de dependencias y `specs/R#.md` | DA-25 (modo de pruebas); DA-06 solo para el esquema del catálogo | Todo lo demás | Contratos congelados antes de lanzar escritores paralelos |
| UT-01 | Arnés de medición (EXP-01 a EXP-16) | UT-00 (esquema de resultados); DA-16 | Algoritmos de R2, R3 y R4 (se prueba con funciones de duración conocida) | Módulo de medición usado por R1.3, R2, R3.2 y R4.1 |
| UT-02 | R1a: descarga, pesos, componente, redes por radio, estimación de memoria | UT-00; GLOB-15; DA-07, DA-08, DA-09; medir exige UT-01 | Algoritmos de R2–R4 | Grafo crudo, componente, pesos y metadato |
| UT-03 | Catálogo del grupo [HUMANA] | DA-06 | — | Catálogo con coordenadas verificadas y duraciones justificadas |
| UT-04 | R1b: asociación lugar → nodo, reporte de más de 500 m, grafo procesado | UT-02, UT-03; DA-10, DA-11 | Algoritmos de R2–R4 | Grafo procesado, índices y asociaciones |
| UT-05 | R2a: Dijkstra en dos versiones y verificaciones con grafos sintéticos | UT-00 | Datos reales, R1, R3, R4 | Módulos y pruebas |
| UT-06 | R2b: mediciones, gráfica, cociente y matriz | UT-01, UT-04, UT-05; DA-14 | R3 | Archivo de mediciones y matriz |
| UT-07 | R3a: preparación de coordenadas enteras, envolvente propia, referencia SciPy y pruebas con puntos sintéticos | UT-00; DA-12 | R1, R2, R4 | Módulos y pruebas |
| UT-08 | R3b: experimento y archivo de envolvente | UT-01, UT-04, UT-07 | R2, R4 | Tabla y archivo para R5 |
| UT-09 | R4a: fuerza bruta, Held-Karp y heurística con matrices sintéticas asimétricas | UT-00; DA-13, DA-21 | Datos reales, R1–R3 | Módulos y pruebas |
| UT-10 | R4b: experimentos, calidad de la heurística e itinerario | UT-01, UT-06, UT-09; GLOB-22; DA-17, DA-22 | R3 | Tablas, gráfica e itinerario |
| UT-11 | R5: aplicación | UT-04, UT-05, UT-08, UT-09 y resultados de R1–R4; DA-24 | — | Aplicación y README |
| UT-12 | Documento técnico, README, anexo de IA y sustentación [HUMANA con borradores del agente] | Todas | — | Entregables de `§7` |

### 2.2 Clasificación ODD: insumos para el orquestador

Son propuestas. El orquestador decide la clasificación, el uso de explorador, escritores paralelos o verificador y las delegaciones. Ninguna se justifica por tamaño ni por número de archivos.

- Clasificación: cada R y UT-01 contiene más de un paso de implementación significativo (ver UT-00 a UT-12); candidatos a trabajo sustancial con documento de feature.
- Explorador de solo lectura: propuesto para R1, R3 y UT-01 porque dependen del comportamiento de versiones y de mecanismos del entorno que el plan no puede asumir; para R4, solo para investigación bibliográfica; para R5, para inspeccionar los artefactos reales de R1–R4.
- Escritores paralelos candidatos tras congelar UT-00: UT-01, UT-05, UT-07 y UT-09. Condición: unidades funcionalmente independientes (datos sintéticos y contratos congelados) con superficies disjuntas (REPO-10). No son paralelizables entre sí UT-06, UT-08 y UT-10 (necesitan UT-01 y datos de UT-04) ni UT-11 (necesita todas).
- Verificación independiente: propuesta para los cuatro ítems de alto riesgo nombrados de la tabla siguiente.
- Recuperabilidad: las series de mediciones largas escriben resultados de forma incremental y son reanudables (EXP-16).

| Ítem de alto riesgo nombrado | Reglas | Riesgo concreto (impacto según `§8`) | Verificación independiente sugerida |
|---|---|---|---|
| Correctitud de Held-Karp | R4-04, R4-06, R4-17 | Recorrido u óptimo erróneos sin fallo visible; R4 pesa 25 % y alimenta el itinerario y R5 | Oráculo propio con enumeración de la biblioteca estándar en `verificacion/`; matrices asimétricas aleatorias con semilla; casos resueltos a mano; no reutilizar las pruebas del implementador |
| Aritmética entera de la envolvente | R3-01, R3-02, R3-13 | Vértices incorrectos por desbordamiento, flotantes o signo del producto cruzado, sin error visible; R3 pesa 20 % | Coordenadas extremas, alineadas y duplicadas; comparar contra SciPy y contra Shapely; comprobar giro y contención con aritmética entera |
| Protocolo de medición | EXP-01 a EXP-16; DA-16 | Mediciones incomparables o irreproducibles invalidan el 30 % experimental de cada R1–R4 | Revisar el arnés con funciones de duración conocida: mediana, regla de un minuto, límite de 5 minutos, exclusión de E/S y huella de entrada |
| Asociación lugar → nodo | R1-06, R1-07, R1-12 | Un CRS mezclado o un nodo ajeno a la componente propaga el error a R2, R4 y R5 | Segundo método de vecino más cercano en `verificacion/`, comparación completa por lugar y contraste en mapa por una persona |

## 3. Plan por requerimiento

### 3.1 R1 — Modelo de la red vial

**Objetivo.** `Proyecto_final_2026-2.md §5, R1.1 a R1.5`; datos en `§4`; formato de resultados en `Anexo_proyecto.md, «Requerimiento 1»`; peso en `§8` (EV-28).

**Fragmentos literales para el documento de feature de ODD.** `§4` («Red vial» y «Catálogo de lugares», con su tabla y el párrafo de campos); `§5, R1.1` a `R1.5` completos; `§6`, ítems 1 a 8; `Anexo_proyecto.md`, bloque «Requerimiento 1».

**Protocolo que aplica.** Mediana de 5 repeticiones; una sola medición si dura más de un minuto; «no completada» si pasa de 5 minutos (EXP-03, EXP-04, EXP-08).

**Políticas y criterios de aceptación.**

**R1-01:** Descargar la red del departamento con OSMnx (el enunciado da como ejemplo `ox.graph_from_place("Quindío, Colombia", network_type="drive")`), guardarla cruda sin modificar y registrar en un metadato: fecha de descarga, versión de Python, de OSMnx y de NetworkX, parámetros de descarga y origen (descarga o GraphML entregado por el docente) [ENUNCIADO `§4, «Red vial»`]. Requiere consulta previa (GLOB-15; DA-07, DA-08). Verificación: prueba de esquema del metadato (campos presentes y no vacíos); prueba de comparación: el grafo crudo recargado tiene el número de nodos y aristas registrado en el metadato.

**R1-02:** Estimar los megabytes de la matriz de adyacencia y de las listas de adyacencia con V y E leídos del metadato del grafo, no escritos a mano. Declarar por escrito los supuestos: bytes por celda y por entrada, tratamiento de aristas paralelas y lazos (conteos del multigrafo y del grafo simple) y convención de megabyte. Reportar la estimación para la red descargada y para la componente, elegir una representación con esos números y justificarla [ENUNCIADO R1.1; PLAN: supuestos]. Verificación: prueba unitaria (a crear) del cálculo con V y E pequeños resueltos a mano; el reporte muestra V, E y supuestos en una tabla; inspección de importaciones: R2 a R4 usan la representación elegida.

**R1-03:** Guardar en cada arista su distancia (m) y su tiempo de viaje (s), calculado como la distancia dividida por la velocidad expresada en m/s. Documentar de dónde sale la velocidad de cada tramo, cómo se trataron los tramos sin velocidad (DA-09) y que el tiempo es una estimación del modelo, no el tiempo real [ENUNCIADO R1.2]. Verificación: prueba de integración sobre el grafo procesado: toda arista tiene ambos atributos, finitos y no negativos; prueba unitaria: en aristas de muestra con distancia positiva, distancia dividida por tiempo es igual a la velocidad en m/s dentro de la tolerancia de DA-15; inspección del texto: contiene la salvedad de estimación.

**R1-04:** Obtener la componente fuertemente conexa más grande invocando literalmente `ox.truncate.largest_component(G, strongly=True)` [ENUNCIADO R1.3; EV-23]. Verificación: búsqueda estática de la llamada literal en el módulo de R1; prueba con script independiente (puede usar NetworkX): el resultado es fuertemente conexo y su número de nodos es igual al de la mayor componente fuertemente conexa del grafo de entrada, calculada de forma independiente.

**R1-05:** Medir solo la llamada de R1-04 sobre un grafo ya cargado en memoria, para las redes descargadas con `ox.graph_from_point` con radios de 2, 5, 10 y 20 km alrededor de la plaza de Bolívar de Armenia (coordenadas del catálogo verificado, GLOB-21) y para la red completa del departamento [ENUNCIADO R1.3; EV-06]. Reportar por red V, E, V + E y tiempo (ms), con V y E de la red de entrada. Verificación: prueba del arnés (UT-01): descarga, lectura y escritura quedan fuera de la región medida; prueba de esquema: cinco filas con las etiquetas del Anexo («Radio de 2 km», «Radio de 5 km», «Radio de 10 km», «Radio de 20 km», «Departamento completo») y V + E igual a la suma de V y E en cada fila.

**R1-06:** Asociar cada lugar del catálogo al nodo de la componente más cercano por distancia euclidiana en metros en UTM zona 18N, transformando lugares y nodos con el mismo CRS (DA-10); desempatar por menor identificador de nodo; guardar por lugar el nodo y la distancia (m) [ENUNCIADO R1.4; EV-05]. Implementar la búsqueda recorriendo todos los nodos de la componente, sin árbol espacial [PLAN: es la opción más simple de explicar y verificar]. Verificación: (i) prueba unitaria con nodos sintéticos donde el más cercano en metros UTM difiere del más cercano en grados; (ii) script independiente con otro método (árbol espacial de biblioteca, solo verificación) que reproduce el mismo nodo para todos los lugares, con los empates documentados; (iii) prueba: todo nodo asignado pertenece a la componente.

**R1-07:** Reportar los lugares cuya distancia al nodo asignado sea estrictamente mayor que 500 m, con su distancia y el tratamiento decidido por personas (DA-11); no eliminar ni modificar lugares sin decisión registrada [ENUNCIADO R1.4; EV-04]. Verificación: prueba unitaria: una distancia de exactamente 500 m no se reporta y una mayor sí; prueba de integración: el conjunto de identificadores del catálogo antes y después de la asociación es idéntico salvo decisión registrada.

**R1-08:** Guardar la componente, sus pesos y las asociaciones, junto con el metadato de V y E antes y después del filtro, para reutilizarlos sin descargar la red [ENUNCIADO R1.5]. Verificación: prueba de ida y vuelta: la carga desde disco no invoca funciones de descarga (búsqueda estática del módulo de carga) y reproduce nodos, aristas, pesos con tipos numéricos y asociaciones del grafo en memoria; la tabla de tamaños (columnas Red, Nodos, Aristas; filas «Red descargada» y «Componente fuertemente conexa») se genera desde el metadato.

**R1-09:** Asignar a los nodos un índice entero contiguo persistido y entregar a R2–R4 estructuras planas de Python; los módulos de algoritmos no dependen de OSMnx ni de NetworkX [PLAN; GLOB-03]. Verificación: prueba: la correspondencia identificador↔índice es biyectiva tras recargar; búsqueda estática: los módulos de R2, R3 y R4 no importan OSMnx ni NetworkX.

**R1-10:** Comprobar la propiedad que justifica trabajar solo con la componente: desde cualquier nodo se alcanza a todos los demás respetando el sentido de las vías [ENUNCIADO R1.3]. Verificación: script independiente: una búsqueda desde un nodo cualquiera en el grafo y otra en el grafo invertido alcanzan todos los nodos; la matriz de R2 no tiene entradas infinitas (R2-11).

**R1-11:** Respetar la tabla de bibliotecas de R1. Verificación: búsqueda estática de importaciones por módulo contra la tabla.

**Bibliotecas de R1.**

| Categoría | Permitidas | Prohibidas |
|---|---|---|
| Implementación evaluable | OSMnx para descargar, proyectar y llamar `largest_component`; biblioteca estándar; NumPy (PROPUESTO) para la búsqueda del nodo más cercano | Sustituir `ox.truncate.largest_component(G, strongly=True)` por otra implementación en la medición; usar `strongly=False`; descargar fuera del módulo de preparación de datos |
| Scripts de verificación | NetworkX, SciPy (árbol espacial), pyproj y GeoPandas (PROPUESTO) para contraste | Importarlas desde módulos evaluables (GLOB-03) |
| Herramientas de análisis | Matplotlib; pandas (PROPUESTO) | — |
| Preparación y procesamiento de datos | OSMnx y GeoPandas (`§3`); pyproj (PROPUESTO) | Escribir en `data/crudo/` una vez creado (GLOB-17) |

**Riesgos y mitigaciones.**

**R1-12 [alto riesgo nombrado: asociación lugar → nodo]:** Riesgo: mezclar grados con metros, invertir el orden latitud/longitud, asociar a un nodo del grafo sin filtrar o proyectar en otra zona; el error se propaga a R2, R4 y R5. Mitigación: fijar explícitamente el orden de ejes y la zona en la transformación y aplicar R1-06. Verificación: prueba con dos lugares de coordenadas conocidas cuya distancia geodésica se calcula con una herramienta independiente: la distancia euclidiana en UTM coincide dentro de una tolerancia declarada por el verificador y justificada por la distorsión de escala de la proyección; cada lugar cae dentro del cuadro envolvente de la red.

**R1-13:** Riesgo: la descarga no es reproducible porque OSM cambia. Mitigación: grafo crudo con fecha (R1-01) y GLOB-17. Verificación: las de R1-01 y GLOB-17.

**R1-14:** Riesgo: cambios de API entre versiones de OSMnx (funciones que cambian de módulo o de nombre). Mitigación: fijar versión exacta en el manifiesto y registrarla en cada archivo de resultados (EXP-14). Verificación: el metadato de cada resultado contiene la versión de OSMnx y el manifiesto la fija.

**R1-15:** Riesgo: en redes pequeñas el tiempo se acerca a la resolución del temporizador. Mitigación: mediana de 5 repeticiones y conservación de los 5 tiempos crudos (EXP-03). Verificación: el archivo de resultados contiene los cinco tiempos crudos por medición.

**Recomendaciones técnicas a investigar.**

**R1-16 [REC]:** Algoritmo interno de `largest_component`. Hipótesis de partida, no confirmada: delega en el cálculo de componentes fuertemente conexas de NetworkX (variante de Tarjan con modificaciones de Nuutila, no recursiva; tiempo lineal esperado en V + E). Confirmar leyendo documentación y código de las versiones instaladas y citar con autor y título o enlace.

**R1-17 [REC]:** Averiguar en el código de la versión instalada si la función retorna sin trabajo adicional cuando el grafo ya es fuertemente conexo y qué copias y estructuras auxiliares crea (memoria); registrar por red si la entrada ya lo era.

**R1-18 [REC]:** Averiguar cómo la versión instalada interpreta `maxspeed` (unidades, listas, valores no numéricos) y qué imputación ofrece; usarlo para resolver DA-09.

**R1-19 [REC]:** Averiguar la semántica del parámetro de distancia de `graph_from_point` (cuadro envolvente o distancia sobre la red) para interpretar «radio» (DA-08).

**R1-20 [REC]:** Contrastar la estimación de memoria con la memoria real del grafo cargado, con una herramienta de medición de memoria de la biblioteca estándar (PROPUESTO).

**Intervenciones humanas y dependencias.**

**R1-21 [HUMANA]:** Elaborar el catálogo y verificar sus coordenadas sobre un mapa (GLOB-21; DA-06). Verificación: la de GLOB-21.

**R1-22 [HUMANA]:** Decidir y documentar el tratamiento de cada lugar a más de 500 m (DA-11). Verificación: cada lugar reportado en R1-07 tiene decisión, autor y fecha humanos registrados.

**R1-23 [HUMANA]:** Redactar la justificación de la representación elegida (R1.1) y de por qué la componente conviene a los requerimientos siguientes (R1.3), con las cifras y el análisis que prepare el agente. Verificación: inspección: ambos textos existen y citan las cifras de R1-02 y la propiedad de R1-10.

**Insumos ODD (decide el orquestador).**
- Dependencias bloqueantes: permiso de red (GLOB-15, DA-07) para R1-01 y R1-05; DA-08 y DA-09 para R1-03 y R1-05; catálogo verificado (UT-03) y DA-10 para R1-06; arnés UT-01 para R1-05.
- Superficies de edición disjuntas candidatas: `src/<paquete>/red/`, `tests/red/`, `specs/R1.md`, `experimentos/r1/`, `resultados/r1/`.
- Exploración de solo lectura: sí; hay que leer documentación y código de las versiones instaladas de OSMnx y NetworkX (algoritmo, parseo de velocidades, semántica de la distancia), cuyo comportamiento el plan no puede asumir.
- Riesgo concreto: asociación lugar → nodo (R1-12). Verificación independiente: sugerida.

### 3.2 R2 — Caminos mínimos

**Objetivo.** `Proyecto_final_2026-2.md §5, R2.1` (texto y cinco viñetas); formato de resultados en `Anexo_proyecto.md, «Requerimiento 2»`. Se trabaja sobre la componente de R1 con el tiempo de viaje como peso.

**Fragmentos literales para el documento de feature de ODD.** `§5, R2.1` completo con sus cinco viñetas; `§4` («Catálogo de lugares»); `§6`, ítems 1 a 8; `Anexo_proyecto.md`, bloque «Requerimiento 2».

**Protocolo que aplica.** EXP-03, EXP-04 y EXP-08 (mediana de 5 repeticiones; una sola medición si pasa de un minuto; «no completada» si pasa de 5 minutos) y semilla fija (EXP-06).

**Políticas y criterios de aceptación.**

**R2-01:** Implementar las dos versiones de Dijkstra sin bibliotecas de grafos: recorrido lineal O(V²) y cola de prioridad O((V + E) log V) [ENUNCIADO R2.1; EV-08]. La cola puede ser una estructura de apoyo de la biblioteca estándar (`heapq`, PROPUESTO) con su costo investigado y sumado (GLOB-04). Verificación: búsqueda estática: los módulos de Dijkstra no importan NetworkX, SciPy, OSMnx ni igraph.

**R2-02:** Detener ambas versiones al sacar el nodo destino y devolver el tiempo y la ruta (secuencia de nodos) reconstruida a partir del predecesor de cada nodo [ENUNCIADO R2.1]. Verificación: prueba unitaria (a crear) sobre grafos sintéticos con semilla fija: la ruta empieza en el origen, termina en el destino, cada par consecutivo es una arista del grafo y la suma de las aristas de menor peso entre paralelas es igual al tiempo devuelto (igualdad exacta); caso origen = destino: tiempo cero, ruta de un nodo y un nodo explorado.

**R2-03:** Contar cada nodo como explorado una sola vez, la primera vez que sale de la cola (el destino cuenta al salir); en la versión con cola de prioridad, ignorar sin contar las entradas obsoletas [ENUNCIADO R2.1]. Verificación: prueba unitaria con un grafo donde un nodo entra varias veces a la cola: el contador aumenta una sola vez; en todas las pruebas, nodos explorados ≤ V.

**R2-04:** Aplicar a ambas versiones el mismo orden de adyacencia, la misma regla de desempate por menor índice de nodo y la relajación solo ante mejora estricta; conservar la arista de menor tiempo entre aristas paralelas e ignorar los lazos [PLAN: hace comparables los nodos explorados]. Verificación: en los pares medidos con ambas versiones y en grafos sintéticos, `nodos_explorados` y la ruta coinciden entre versiones; toda diferencia se registra como hallazgo.

**R2-05:** Validar al cargar que todos los pesos son finitos y no negativos y fallar con error explícito en caso contrario [ENUNCIADO R2.1, viñeta 1: condición sobre los pesos]. Verificación: prueba unitaria: un grafo con un peso negativo provoca el error; el grafo procesado de R1 pasa la validación.

**R2-06:** Verificar antes de medir [ENUNCIADO R2.1, viñeta «Verificación»; `§6, ítem 6`]: (a) las dos versiones dan los mismos tiempos en todos los pares medidos con ambas; (b) en grafos sintéticos con semilla fija, la versión lineal desde un origen hacia cada nodo coincide con el vector de la versión con cola; (c) un script independiente con NetworkX compara los tiempos de todos los pares medidos y de todas las filas de la matriz. Verificación: pruebas (a crear) con esas tres comparaciones; igualdad exacta entre las dos versiones propias y la tolerancia de DA-15 frente a NetworkX.

**R2-07:** Elegir al menos 20 pares origen-destino del catálogo para la versión con cola y 10 de esos pares para la versión lineal, estos últimos entre lugares cercanos (mismo municipio o municipios vecinos), y guardar la lista como archivo de entrada del experimento [ENUNCIADO R2.1, viñeta 2; EV-07; DA-14]. Verificación: prueba sobre el archivo de pares: al menos 20 pares distintos; los 10 pares lineales están incluidos entre ellos; cada uno cumple el criterio de cercanía según la tabla de municipios vecinos aprobada (DA-14).

**R2-08:** Registrar por consulta y por versión el tiempo de viaje, los nodos explorados y el tiempo (ms) en un archivo con las columnas exactas `origen`, `destino`, `version`, `tiempo_viaje_s`, `nodos_explorados` y `tiempo_ms`, con `version` igual a `lineal` o `cola_prioridad` [ENUNCIADO Anexo, «Requerimiento 2»; EV-25]. Verificación: prueba de esquema (GLOB-09); recuento: al menos 20 filas `cola_prioridad` y 10 filas `lineal`; `tiempo_viaje_s` igual entre versiones por par.

**R2-09:** Presentar la gráfica con nodos explorados en el eje horizontal, tiempo (ms) en el vertical y las dos versiones en la misma figura con color o símbolo distinto [ENUNCIADO R2.1, viñeta 3; Anexo]. Verificación: prueba sobre el objeto de figura (a crear): dos series, etiquetas de ejes con «nodos explorados» y «ms», y puntos iguales a los del archivo de R2-08.

**R2-10:** Calcular, por cada uno de los 10 pares medidos con ambas versiones, el cociente tiempo de la versión lineal ÷ tiempo de la versión con cola, y reportar mediana, mínimo y máximo [ENUNCIADO R2.1, viñeta 3; Anexo; EV-26]. Verificación: recálculo independiente desde el CSV de R2-08: coincide con la tabla.

**R2-11:** Calcular y guardar la matriz de tiempos entre todos los lugares del catálogo ejecutando la versión con cola una vez desde cada lugar, sin destino, y sin simetrizarla; formato: CSV con primera fila y primera columna iguales a los identificadores de los lugares y celda (i, j) igual a los segundos de ir de i a j [ENUNCIADO R2.1, viñeta «Matriz de tiempos»; Anexo; EV-09]. Verificación: pruebas: el encabezado de fila es igual al de columna y a los identificadores del catálogo en el mismo orden; al menos 40 filas y 40 columnas; diagonal cero; todas las entradas finitas y no negativas; desigualdad triangular entre lugares con la tolerancia de DA-15; un script independiente con NetworkX reproduce cada fila; búsqueda estática: ningún código promedia ni iguala la matriz con su traspuesta.

**R2-12:** Medir con el arnés (UT-01) según EXP-03, EXP-04 y EXP-08; una consulta que pase de 5 minutos se registra «no completada» en una columna adicional `estado` y no se sustituye por un valor deducido [ENUNCIADO `§6, ítems 3 y 7`; DA-04]. Verificación: prueba del arnés con límite reducido y una función lenta: estado `no_completada` y sin tiempo.

**R2-13:** Implementar ambas versiones en Python puro sobre las mismas estructuras de datos, sin NumPy ni vectorización [PLAN: conserva la comparabilidad; DA-21]. Verificación: búsqueda estática: sin importaciones de NumPy en los módulos de Dijkstra.

**R2-14:** Documentar el invariante de Dijkstra, por qué permite detenerse al sacar el destino, la condición que deben cumplir los pesos y la complejidad en tiempo y memoria con fuente, incluido el costo de la cola de la biblioteca [ENUNCIADO R2.1, viñeta 1; EV-08; GLOB-04]. Verificación: inspección de evidencias con lista de comprobación: invariante enunciado, justificación de la parada, condición de pesos, fuente citada y costo de la cola incluido.

**R2-15:** Respetar la tabla de bibliotecas de R2 y no extender a R2 permisos de R1 ni de R3. Verificación: búsqueda estática de importaciones por módulo contra la tabla.

**Bibliotecas de R2.**

| Categoría | Permitidas | Prohibidas |
|---|---|---|
| Implementación evaluable | Biblioteca estándar: estructura de cola de prioridad (`heapq`, PROPUESTO), listas y diccionarios | NetworkX, SciPy (`csgraph`), OSMnx (`ox.routing`, caminos mínimos), igraph, graph-tool; NumPy y pandas dentro del algoritmo medido |
| Scripts de verificación | NetworkX y SciPy, solo para comprobar resultados | Importarlos desde módulos evaluables |
| Herramientas de análisis | pandas (PROPUESTO), Matplotlib, `statistics` (PROPUESTO) | — |
| Preparación y procesamiento de datos | Cargador del grafo procesado (puede usar OSMnx); entrega estructuras planas (R1-09) | OSMnx o NetworkX dentro de los módulos de Dijkstra |

**Riesgos y mitigaciones.**

**R2-16:** Riesgo: comparaciones de punto flotante falsas por empates y por orden de suma. Mitigación: orden determinista (R2-04) y tolerancia explícita (DA-15). Verificación: las de R2-04 y R2-06.

**R2-17:** Riesgo: la versión lineal tarda demasiado en pares lejanos. Mitigación: pares cercanos (R2-07) y límite de 5 minutos (R2-12). Verificación: la de R2-12.

**R2-18:** Riesgo: el cociente refleja la diferencia de implementación entre la estructura de cola de la biblioteca y el recorrido lineal propio, además de la complejidad. Mitigación: no corregirlo artificialmente y explicarlo en la discusión del cociente (GLOB-10). Verificación: inspección: el párrafo de la tabla del cociente menciona esa diferencia, con la fuente investigada (R2-21).

**R2-19:** Riesgo: lugares distintos asociados al mismo nodo producen filas idénticas y tiempos cero entre ellos. Mitigación: tratarlos como lugares distintos por identificador de catálogo; no deduplicar por nodo. Verificación: prueba: la matriz tiene una fila por lugar del catálogo aunque haya nodos repetidos.

**Recomendaciones técnicas a investigar.**

**R2-20 [REC]:** Costo de la cola con entradas obsoletas: su tamaño puede llegar a la cantidad de aristas; confirmar con fuente que la cota O((V + E) log V) del enunciado se mantiene y citarla.

**R2-21 [REC]:** Averiguar si la estructura de cola de la biblioteca estándar está implementada en código compilado y cómo eso afecta el cociente.

**R2-22 [REC]:** Añadir la verificación de un grafo pequeño resuelto a mano, que `§6, ítem 6` admite como método.

**Intervenciones humanas y dependencias.**

**R2-23 [HUMANA]:** Aprobar la tabla de municipios vecinos y la lista de pares (DA-14). Verificación: la tabla y la lista llevan autor y fecha humanos; R2-07 usa solo esas versiones.

**Insumos ODD (decide el orquestador).**
- Dependencias bloqueantes: R2a (UT-05) solo necesita los contratos de UT-00; R2b (UT-06) necesita grafo procesado e índices (UT-04), arnés (UT-01), pares aprobados (DA-14) y pesos finales (DA-09).
- Superficies de edición disjuntas candidatas: `src/<paquete>/caminos/`, `tests/caminos/`, `specs/R2.md`, `experimentos/r2/`, `resultados/r2/`.
- Exploración de solo lectura: no para los algoritmos, que el enunciado especifica; opcional para la fuente del costo de la cola (R2-20, R2-21).
- Riesgo concreto: desempates y comparabilidad (R2-16, R2-18). Verificación independiente adicional: no sugerida; R2-06 ya incluye un script independiente con NetworkX. R2a es independiente de datos reales; R2b no lo es.

### 3.3 R3 — Envolvente convexa de la red vial

**Objetivo.** `Proyecto_final_2026-2.md §5, R3` (introducción, «Coordenadas», R3.1 y R3.2); formato de resultados en `Anexo_proyecto.md, «Requerimiento 3»`. Se calcula sobre los nodos de la componente de R1.

**Fragmentos literales para el documento de feature de ODD.** `§5, R3` completo; `§6`, ítems 1 a 8; `Anexo_proyecto.md`, bloque «Requerimiento 3».

**Protocolo que aplica.** EXP-03, EXP-04 y EXP-08 (mediana de 5 repeticiones; una sola medición si pasa de un minuto; «no completada» si pasa de 5 minutos) y semilla fija (EXP-06).

**Políticas y criterios de aceptación.**

**R3-01:** Preparar los puntos: convertir las coordenadas de los nodos de la componente a metros en UTM zona 18N (DA-10), aproximar cada coordenada al entero más cercano y eliminar los puntos repetidos [ENUNCIADO R3 «Coordenadas»; EV-05]. Fijar y documentar la regla de empate de los valores terminados en .5 (DA-18). Verificación: pruebas unitarias: los valores terminados en .5 siguen la regla documentada; el conjunto resultante no tiene duplicados (tamaño del conjunto igual a la longitud de la lista); todas las coordenadas son enteros.

**R3-02:** Calcular giros y alineaciones solo con aritmética entera exacta: sin flotantes, divisiones, raíces ni trigonometría en los predicados; enteros nativos de Python o, si se usa NumPy, `int64` explícito [ENUNCIADO R3 «Coordenadas»; EV-11; contexto: Parte 4, diapositiva 23, y `02-analisis-de-algoritmos.md §2.3.3`, EV-34]. Verificación: (i) búsqueda estática en el módulo de la envolvente: sin `float`, `/`, `sqrt`, funciones trigonométricas ni dtype flotante en los predicados; (ii) pruebas unitarias con coordenadas cuyos productos cruzados exceden el rango de 32 bits y, en una variante de prueba, la precisión del flotante de doble precisión: resultados exactos; (iii) si hay arreglos NumPy, prueba de que su dtype es entero de 64 bits.

**R3-03:** No contar como vértices los puntos alineados sobre los lados del polígono [ENUNCIADO R3 «Coordenadas»]. Verificación: pruebas unitarias: un cuadrado con puntos intermedios en sus lados devuelve solo las esquinas; un conjunto con todos los puntos alineados cumple el comportamiento fijado en DA-18.

**R3-04:** Elegir e implementar un algoritmo propio de envolvente convexa de divide y vencerás y justificar la elección según la distribución de los puntos de la red [ENUNCIADO R3.1; DA-12]. Registrar elección, justificación y recurrencia en `specs/R3.md` antes de programar. Verificación: inspección del historial o del documento de feature: la elección y la recurrencia anteceden al primer cambio del módulo de la envolvente; la justificación cita una medición de la distribución (vértices frente a puntos) obtenida con la referencia de R3-05.

**R3-05:** Calcular también con `scipy.spatial.ConvexHull` en un módulo de referencia separado y verificar que ambos devuelvan los mismos vértices en todas las pruebas, comparando conjuntos de coordenadas y no índices, sin depender del vértice inicial ni del sentido [ENUNCIADO R3.1; EV-24]. Verificación: prueba de comparación automática sobre los nodos de la red, los tres cuadrados, conjuntos pequeños con semilla fija y casos construidos; falla si la diferencia simétrica de los conjuntos no es vacía.

**R3-06:** Definir el comportamiento ante conjuntos que no forman polígono (pocos puntos distintos, todos alineados) y verificarlo con casos resueltos a mano, porque SciPy no sirve de referencia en ellos (DA-18). Verificación: pruebas unitarias con resultados esperados fijados a mano (R3-23).

**R3-07:** Medir las dos versiones con los nodos de la componente y con puntos al azar en un cuadrado de 1 000, 10 000 y 50 000 puntos con semilla fija [ENUNCIADO R3.2; EV-10]. Ambas reciben el mismo conjunto entero ya preparado, en el formato que cada una necesita; solo se mide el cálculo de la envolvente [ENUNCIADO `§6, ítem 2`; DA-18]. Verificación: prueba del arnés: las funciones de conversión, redondeo, deduplicación y formato quedan fuera de la región medida; la `n` de cada fila es el tamaño del conjunto tras deduplicar.

**R3-08:** Presentar la tabla con las columnas del Anexo (Conjunto de puntos, n, Vértices de la envolvente, Tiempo propio (ms), Tiempo SciPy (ms), Cociente) y las filas «Nodos de la red», «Cuadrado, 1 000 puntos», «Cuadrado, 10 000 puntos» y «Cuadrado, 50 000 puntos» [ENUNCIADO Anexo, «Requerimiento 3»]. Verificación: prueba de esquema y de filas; los vértices coinciden entre la versión propia y SciPy en cada fila; el cociente se recalcula desde las dos columnas de tiempo con la dirección fijada en DA-18.

**R3-09:** Plantear la recurrencia del algoritmo elegido, resolverla con una técnica de la Parte 3 (diapositivas 26–49) o con fuente, y documentar la complejidad en tiempo y memoria con fuente, sumando el costo del ordenamiento de biblioteca si se usa [ENUNCIADO `§5` introducción; GLOB-04; EV-33, EV-36]. Verificación: inspección con lista de comprobación: recurrencia planteada, solución, costo del ordenamiento si aplica y fuente citada.

**R3-10:** Explicar la diferencia de tiempos investigando qué algoritmo y qué lenguaje usa SciPy internamente en la versión instalada, y registrar esa versión [ENUNCIADO R3.2]. Verificación: inspección: el texto nombra algoritmo, lenguaje, versión y fuente.

**R3-11:** Guardar los vértices de la envolvente de la red (coordenadas enteras UTM y posición geográfica para mostrarlos) en un archivo que R5 lea sin recalcular [PLAN]. Verificación: prueba: el número de vértices del archivo es igual al de la fila «Nodos de la red» de R3-08 y R5 lo carga.

**R3-12:** Respetar la tabla de bibliotecas de R3. Verificación: búsqueda estática de importaciones por módulo contra la tabla.

**Bibliotecas de R3.**

| Categoría | Permitidas | Prohibidas |
|---|---|---|
| Implementación evaluable (envolvente propia) | Biblioteca estándar; ordenamiento de biblioteca con su costo incluido (GLOB-04); enteros nativos | `scipy.spatial` (`ConvexHull`, `Delaunay`, `HalfspaceIntersection`), `convex_hull` de Shapely o GeoPandas, funciones de envolvente de scikit-image u OpenCV (PROPUESTO), cualquier función que devuelva una envolvente |
| Scripts de verificación y módulo de referencia | `scipy.spatial.ConvexHull` (única función de SciPy que el enunciado exige para comparar y medir); Shapely como segundo contraste (PROPUESTO) | Importarlos desde la implementación evaluable (GLOB-03) |
| Herramientas de análisis | Matplotlib; pandas (PROPUESTO) | — |
| Preparación y procesamiento de datos | OSMnx, GeoPandas y pyproj (PROPUESTO) para la conversión a UTM | Realizar la conversión dentro de la región medida |

**Riesgos y mitigaciones.**

**R3-13 [alto riesgo nombrado: aritmética entera de la envolvente]:** Riesgo: desbordamiento o pérdida de precisión por el tipo (NumPy con entero por defecto de 32 bits en algunas plataformas), flotantes en los predicados o signo equivocado del producto cruzado; produce vértices erróneos sin error visible. Mitigación: R3-02 más una propiedad de salida: cada giro entre vértices consecutivos es estrictamente a la izquierda y todo punto de entrada está dentro o sobre el polígono, comprobado con aritmética entera. Verificación: prueba de propiedad (a crear) con semilla fija sobre conjuntos aleatorios y adversarios (casi alineados, todos los puntos en posición convexa, duplicados antes de deduplicar): ambas condiciones se cumplen.

**R3-14:** Riesgo: profundidad de recursión excesiva con particiones desbalanceadas y error de recursión de Python. Mitigación: probar entradas adversarias; no elevar el límite global sin una medición que lo justifique. Verificación: prueba con entradas adversarias: sin error y con resultado igual al de la referencia.

**R3-15:** Riesgo: discrepancia con SciPy por puntos alineados sobre el borde. Mitigación: no ajustar el algoritmo propio para coincidir; documentar el caso; si SciPy devuelve puntos alineados, normalizar ambos resultados con el predicado entero exacto y registrarlo. Verificación: el reporte de comparación lista toda normalización y su cuenta (cero si no hubo).

**R3-16:** Riesgo: el redondeo y la deduplicación cambian el conjunto; la envolvente es la de los puntos redondeados [ENUNCIADO R3 «Coordenadas»]. Mitigación: documentarlo y reportar el número de puntos antes y después. Verificación: el archivo de resultados contiene ambos conteos.

**R3-17:** Riesgo: tiempos incomparables por el formato de entrada y por la diferencia de lenguaje de implementación (código propio en Python frente a una biblioteca compilada). Mitigación: EXP-11 y explicación en R3-10. Verificación: inspección: la discusión de la tabla menciona ambas diferencias.

**Recomendaciones técnicas a investigar.**

**R3-18 [REC]:** Algoritmo de SciPy. Hipótesis de partida, no confirmada: biblioteca Qhull escrita en C con el algoritmo Quickhull. Confirmar en la documentación de la versión instalada.

**R3-19 [REC]:** Costo del ordenamiento de Python. Hipótesis de partida, no confirmada: Timsort, coherente con la fila «Timsort» de la Parte 4, diapositiva 14. Confirmar en la documentación oficial.

**R3-20 [REC]:** Comparar candidatos: QuickHull (descarta pronto los puntos interiores cuando los vértices son pocos frente a n; en el peor caso las particiones quedan desbalanceadas) y fusión por tangentes (recursión balanceada en el peor caso). Decidir con la relación vértices/puntos medida (DA-12). Obtener las complejidades de una fuente; no inferirlas de `06-ordenamiento.md §6.11` ni de la Parte 4, diapositiva 14 (DA-02).

**R3-21 [REC]:** Para la solución de la recurrencia, consultar la Parte 3: método maestro (diapositivas 45–48) y sustitución o método iterativo (diapositiva 49).

**Intervenciones humanas y dependencias.**

**R3-22 [HUMANA]:** Elegir el algoritmo y redactar su justificación (DA-12). Verificación: `specs/R3.md` contiene la decisión con autor y fecha humanos.

**R3-23 [HUMANA]:** Fijar a mano los resultados esperados de los casos degenerados de R3-06. Verificación: cada caso lleva el resultado esperado con autor humano.

**Insumos ODD (decide el orquestador).**
- Dependencias bloqueantes: R3a (UT-07) necesita los contratos de UT-00 y DA-12; R3b (UT-08) necesita la componente y los índices (UT-04), el arnés (UT-01) y el módulo de R3a.
- Superficies de edición disjuntas candidatas: `src/<paquete>/envolvente/`, `tests/envolvente/`, `specs/R3.md`, `experimentos/r3/`, `resultados/r3/`.
- Exploración de solo lectura: sí; leer la documentación de la versión instalada de SciPy (R3-10) y medir la distribución de puntos de la red antes de elegir algoritmo (DA-12).
- Riesgo concreto: aritmética entera (R3-13). Verificación independiente: sugerida. R3a es independiente de datos reales; R3b no lo es.

### 3.4 R4 — Ruta óptima de recorrido

**Objetivo.** `Proyecto_final_2026-2.md §5, R4` (introducción y R4.1 a R4.5); formato de resultados en `Anexo_proyecto.md, «Requerimiento 4»`. Usa la matriz de R2.

**Fragmentos literales para el documento de feature de ODD.** `§5, R4` completo; `§4`, último párrafo (campos del catálogo, duración de visita y Armenia); `§6`, ítems 1 a 8; `Anexo_proyecto.md`, bloque «Requerimiento 4».

**Protocolo que aplica.** EXP-03, EXP-04 y EXP-08 (mediana de 5 repeticiones; una sola medición si pasa de un minuto; «no completada» si pasa de 5 minutos) y semilla fija (EXP-06).

**Políticas y criterios de aceptación.**

**R4-01:** Modelar el problema como viajante asimétrico sobre la matriz de R2: salida desde el lugar de partida, visita de los k lugares elegidos y regreso; costo igual a la suma de las celdas dirigidas del recorrido, en segundos; no suponer simetría [ENUNCIADO R4, introducción]. Verificación: prueba unitaria con una matriz asimétrica pequeña cuyo óptimo y recorrido se calculan a mano: ambos métodos exactos lo devuelven y el recorrido inverso tiene costo distinto.

**R4-02:** Implementar con código propio la fuerza bruta (todas las permutaciones, con la enumeración incluida en el código propio) y Held-Karp (programación dinámica sobre subconjuntos de lugares) [ENUNCIADO R4.1; DA-21]. Verificación: búsqueda estática: los módulos de R4 no importan funciones de enumeración combinatoria de la biblioteca estándar ni bibliotecas de optimización o de TSP; pruebas de R4-06.

**R4-03:** Antes de implementar Held-Karp, justificar la subestructura óptima y plantear la recurrencia en `specs/R4.md` [ENUNCIADO R4.1; `§5` introducción]. Verificación: inspección del historial o del documento de feature: el documento con ambas partes antecede al primer cambio del módulo de Held-Karp.

**R4-04:** Hacer que Held-Karp devuelva el recorrido (orden de visita) y su tiempo total [ENUNCIADO R4.1]. Verificación: pruebas: el recorrido es una permutación de los k lugares, empieza y termina en el lugar de partida, y su costo recalculado desde la matriz coincide con el reportado dentro de la tolerancia de DA-15.

**R4-05:** Estimar la memoria de Held-Karp según el tamaño de su tabla (número de entradas por bytes por entrada, con los supuestos declarados) para cada k medido [ENUNCIADO R4.1]. Verificación: prueba unitaria del cálculo para valores pequeños de k comprobados a mano; el reporte lista k, entradas, supuestos de bytes y megabytes.

**R4-06:** Verificar que la fuerza bruta y Held-Karp dan el mismo tiempo total óptimo en todos los k que la fuerza bruta resuelva [ENUNCIADO R4.1] y, además, contra un oráculo independiente. Verificación: prueba de comparación (costos iguales con la tolerancia de DA-15) sobre las instancias del experimento y sobre matrices asimétricas aleatorias con semilla fija; un script independiente enumera con la biblioteca estándar (solo verificación) y coincide.

**R4-07:** Ejecutar el experimento de soluciones exactas con Armenia como partida y k lugares al azar del catálogo, sin repetir, sin incluir la partida y de cualquier categoría, con semilla fija [ENUNCIADO R4, introducción y R4.1], para k = 5, 6, …, 12 (EV-13) o hasta que una ejecución pase de 5 minutos (EV-12), con la misma instancia por k para ambos métodos (DA-17). Verificación: archivo de instancias guardado; prueba: cada instancia tiene k lugares distintos y sin Armenia, ambos métodos usan el mismo conjunto, y cada serie termina en 12 o en el primer k «no completada» de su método.

**R4-08:** Detener toda ejecución que pase de 5 minutos, marcarla «no completada», no aumentar k para ese método y reportar el mayor k resuelto de cada método [ENUNCIADO R4.1; `§6, ítem 7`; Anexo; EV-27]. Verificación: prueba del arnés con límite reducido; en la tabla, el mayor k resuelto de cada método es el último k con estado completado (comprobación automática).

**R4-09:** Presentar la gráfica de tiempo (ms) frente a k, con una curva por solución y sin trazar los puntos «no completada» como valores [ENUNCIADO R4.1; Anexo]. Verificación: prueba sobre el objeto de figura (a crear): dos series, ejes con «k» y «ms», sin puntos para los k no completados.

**R4-10:** Implementar con código propio la heurística voraz elegida por el grupo (DA-13): constructiva, parte del lugar de partida y regresa a él, respeta la dirección de la matriz, sin mejoras posteriores no voraces y con desempate determinista documentado [ENUNCIADO R4.2]. Verificación: pruebas unitarias en una matriz asimétrica pequeña con resultado resuelto a mano: recorrido válido y costo correcto; inspección: la justificación de la elección está en `specs/R4.md`.

**R4-11:** Medir la calidad de la heurística para k = 5, 8, 10 y 12 con al menos 5 instancias distintas por k: brecha = (costo de la heurística − costo de Held-Karp) ÷ costo de Held-Karp × 100; reportar promedio y máximo [ENUNCIADO R4.3; EV-14; fórmula en DA-18]. Verificación: recálculo independiente desde el CSV por instancia; ninguna brecha negativa más allá de la tolerancia de DA-15 (si aparece, hay un fallo en Held-Karp o en la heurística); los conjuntos de lugares de las instancias de un mismo k son distintos.

**R4-12:** Calcular el itinerario de un día: lugar de partida del catálogo (por defecto Armenia) y entre 6 y 8 atractivos, ordenados con Held-Karp, con duración igual a visitas más desplazamientos incluido el regreso; comprobar si cabe en 11 h; si no cabe, quitar atractivos con justificación humana (R4-27), recalcular y reportar la duración final [ENUNCIADO R4.4; EV-15, EV-16, EV-17; DA-22]. Verificación: prueba unitaria con matriz y duraciones pequeñas resueltas a mano; la tabla del Anexo tiene las columnas Orden, Lugar, Desplazamiento desde el anterior (min), Visita (min) y Tiempo acumulado (h), la fila «Regreso» y los tres totales (visitas, desplazamientos, duración de la jornada); comprobación automática: total = suma de visitas + suma de desplazamientos, acumulado no decreciente y el indicador «cabe» corresponde a la comparación con 11 h.

**R4-13:** Calcular internamente en segundos y convertir a minutos y horas solo al presentar, sin redondear los valores almacenados [ENUNCIADO: no redondear ni convertir valores sin autorización; Anexo: formato]. Verificación: prueba: el archivo de resultados conserva segundos; la tabla redondea solo al presentar, con el número de decimales documentado.

**R4-14:** Mostrar con un ejemplo reproducible por qué la heurística no siempre encuentra el mejor recorrido y comparar con Dijkstra, que también es voraz [ENUNCIADO R4.5]. Verificación: prueba: la instancia del ejemplo (de R4-11 con brecha positiva o una matriz asimétrica pequeña construida) da un costo de la heurística estrictamente mayor que el de Held-Karp; inspección: el texto explica por qué la elección voraz garantiza el óptimo en Dijkstra y aquí no.

**R4-15:** Documentar la complejidad en tiempo y memoria de la fuerza bruta, de Held-Karp y de la heurística, con fuente y con recurrencia donde corresponda [ENUNCIADO `§5` introducción]. Verificación: inspección con lista de comprobación: complejidad, memoria, fuente y recurrencia por algoritmo.

**R4-16:** Respetar la tabla de bibliotecas de R4. Verificación: búsqueda estática de importaciones por módulo contra la tabla.

**Bibliotecas de R4.**

| Categoría | Permitidas | Prohibidas |
|---|---|---|
| Implementación evaluable | Biblioteca estándar sin enumeración combinatoria ni memoización automática; Python puro sin NumPy en el algoritmo medido (DA-21) | `itertools` (permutaciones, combinaciones), `functools` (`cache`, `lru_cache`), NetworkX (TSP), SciPy (`optimize`), OR-Tools y paquetes de TSP (PROPUESTO) |
| Scripts de verificación | `itertools` para el oráculo independiente | Importarlo desde módulos evaluables |
| Herramientas de análisis | `tracemalloc` (PROPUESTO) para la memoria real; pandas; Matplotlib | — |
| Preparación y procesamiento de datos | Lectura del CSV de la matriz con la biblioteca estándar o pandas | — |

**Riesgos y mitigaciones.**

**R4-17 [alto riesgo nombrado: correctitud de Held-Karp]:** Riesgo: error de asimetría (usar la celda de ida por la de vuelta), desfase entre k y k + 1 nodos, incluir la partida en los subconjuntos, reconstrucción incorrecta del recorrido o igualdad de flotantes mal comparada. Mitigación: R4-01, R4-04 y R4-06 más propiedades: el costo de Held-Karp no supera el de ninguna permutación aleatoria y no cambia al permutar el orden de los lugares de entrada. Verificación: pruebas de propiedad (a crear) con semilla fija sobre matrices asimétricas.

**R4-18:** Riesgo: lugares que comparten nodo (costo cero entre ellos) producen empates. Mitigación: desempate determinista y comparar costos, no recorridos. Verificación: R4-06 compara costos; prueba con una matriz con ceros fuera de la diagonal.

**R4-19:** Riesgo: la fuerza bruta alcanza un k menor que 12 en Python; es esperable y se reporta, no se oculta con atajos. Mitigación: sin poda ni memoización (R4-08). Verificación: prueba: para un k pequeño, el número de permutaciones evaluadas por la fuerza bruta es igual al total de permutaciones (contador de prueba).

**R4-20:** Riesgo: instancias repetidas o sesgadas. Mitigación: sorteo sin reemplazo con semilla derivada y verificación de distinción (R4-07, R4-11). Verificación: las de R4-07 y R4-11.

**Recomendaciones técnicas a investigar.**

**R4-21 [REC]:** Fuentes de Held-Karp, su recurrencia y sus complejidades de tiempo y memoria. El material de clase solo menciona el viajante como caso factorial (Parte 2, diapositiva 34) y no trata recurrencias de programación dinámica (Parte 3).

**R4-22 [REC]:** Representar los subconjuntos como máscara de bits y la tabla indexada por subconjunto y último lugar, para que su tamaño sea explícito (R4-05).

**R4-23 [REC]:** Contrastar la memoria estimada con la memoria real medida (R4-05).

**R4-24 [REC]:** Candidatos para la heurística voraz: vecino más cercano dirigido e inserción más barata; decidir con DA-13.

**R4-25 [REC]:** Los tiempos de los dos métodos exactos no dependen del contenido de la matriz; comprobarlo con una segunda instancia en un k pequeño antes de aceptar una sola instancia por k (DA-17).

**Intervenciones humanas y dependencias.**

**R4-26 [HUMANA]:** Elegir la heurística y redactar su justificación (DA-13). Verificación: `specs/R4.md` contiene la decisión con autor y fecha humanos.

**R4-27 [HUMANA]:** Elegir la partida y los atractivos del itinerario y decidir y justificar cuáles se quitan si no cabe (DA-22). El agente puede calcular el ahorro de tiempo por atractivo como evidencia. Verificación: la decisión y su justificación llevan autor y fecha humanos.

**R4-28 [HUMANA]:** Justificar las duraciones de visita (GLOB-22). Verificación: la de GLOB-22.

**Insumos ODD (decide el orquestador).**
- Dependencias bloqueantes: R4a (UT-09) necesita UT-00, DA-13 y DA-21; R4b (UT-10) necesita la matriz (UT-06), el arnés (UT-01), las duraciones (GLOB-22) y DA-17 y DA-22.
- Superficies de edición disjuntas candidatas: `src/<paquete>/recorrido/`, `tests/recorrido/`, `specs/R4.md`, `experimentos/r4/`, `resultados/r4/`.
- Exploración de solo lectura: solo investigación bibliográfica de Held-Karp (R4-21); no se necesita explorar código.
- Riesgo concreto: correctitud de Held-Karp (R4-17). Verificación independiente: sugerida. R4a es independiente de datos reales; R4b no lo es.

### 3.5 R5 — Aplicación

**Objetivo.** `Proyecto_final_2026-2.md §5, R5` (introducción y R5.1); entregable en `§7`. El Anexo no fija formato para R5; la aplicación muestra las tablas y gráficas de los bloques R1–R4 del Anexo.

**Fragmentos literales para el documento de feature de ODD.** `§5, R5` completo; `§7` (tabla de entregables); `Anexo_proyecto.md`, bloques «Requerimiento 1» a «Requerimiento 4» (qué tablas y gráficas se muestran).

**Políticas y criterios de aceptación.**

**R5-01:** Entregar una aplicación (web o de escritorio, DA-24) que se ejecute localmente siguiendo el README [ENUNCIADO R5.1; EV-29]. Verificación: prueba de humo (a crear) que arranca la aplicación y obtiene la pantalla principal sin error; la ejecución de los pasos del README en un entorno limpio es [HUMANA] (R5-13).

**R5-02:** Permitir elegir origen y destino del catálogo y mostrar la ruta en un mapa con su tiempo de viaje, calculados en el momento con la versión con cola de prioridad de R2 [ENUNCIADO R5, introducción y R5.1]. Verificación: prueba de integración: para un par del archivo de R2-08, la ruta y el tiempo de la aplicación son iguales a los del módulo de R2 y al `tiempo_viaje_s` del CSV.

**R5-03:** Mostrar la envolvente convexa sobre el mapa del departamento usando el archivo de R3-11, cuyo precálculo el enunciado permite [ENUNCIADO R5, introducción y R5.1]. Verificación: prueba: el número de vértices dibujados es igual al de la fila «Nodos de la red» de R3-08.

**R5-04:** Permitir elegir la partida del itinerario (por defecto Armenia) y entre 6 y 8 atractivos, rechazar selecciones fuera de ese rango y mostrar el recorrido de Held-Karp y el de la heurística voraz propios, calculados en el momento, con el tiempo total de cada uno y la diferencia entre ellos [ENUNCIADO R5.1; EV-15, EV-17]. Verificación: prueba de integración: para una selección fija, recorridos y totales son idénticos a los de R4; la diferencia (heurística menos Held-Karp) no es negativa; una cantidad inferior y una superior al rango se rechazan.

**R5-05:** Mostrar las gráficas y tablas de R1–R4 (pueden ser las mismas imágenes del documento técnico) [ENUNCIADO R5.1]. Verificación: prueba: cada tabla y gráfica de los bloques R1–R4 del Anexo (R1: dos tablas; R2: gráfica y tabla del cociente; R3: tabla; R4: gráfica, dos tablas e itinerario) es accesible desde la aplicación y proviene de `resultados/` (GLOB-08).

**R5-06:** No descargar la red ni recalcular experimentos en la aplicación: cargar el grafo procesado y los resultados guardados [PLAN]. Verificación: búsqueda estática: la aplicación no importa el módulo de descarga; prueba con las funciones de descarga sustituidas por un doble que falla: la aplicación arranca y responde.

**R5-07:** Entregar un README con instrucciones para ejecutar la aplicación y reproducir los experimentos, versiones fijadas y ubicación de los datos [ENUNCIADO `§7`, «Repositorio en GitHub»]. Verificación: lista de comprobación del README contra `§7`; una persona ejecuta cada comando documentado.

**R5-08:** Calcular rutas y recorridos solo con los módulos propios de R2 y R4; respetar la tabla de bibliotecas de R5 [ENUNCIADO R5, introducción; GLOB-02]. Verificación: búsqueda estática de importaciones en el paquete de la aplicación contra la tabla.

**Bibliotecas de R5.**

| Categoría | Permitidas | Prohibidas |
|---|---|---|
| Implementación evaluable | Módulos propios de R2 (cola de prioridad), R3 (archivo de envolvente) y R4 (Held-Karp y heurística); marco de interfaz y de mapas (`§3`: Folium, Leaflet, Plotly, Matplotlib; PROPUESTO: Streamlit, Dash o Flask, DA-24) | NetworkX, enrutamiento de OSMnx y SciPy para calcular rutas o recorridos |
| Scripts de verificación | Pruebas de integración; NetworkX solo en scripts independientes | Importarlo desde la aplicación |
| Herramientas de análisis | Matplotlib, Plotly | — |
| Preparación y procesamiento de datos | Lectura del grafo procesado y de los archivos de resultados | Descargar la red (R5-06) |

**Riesgos y mitigaciones.**

**R5-09:** Riesgo: las teselas del mapa requieren red al ejecutar. Mitigación: documentarlo en el README y consultar el acceso (GLOB-15; DA-23). Verificación: el README menciona la dependencia.

**R5-10:** Riesgo: tiempo de carga del grafo y de cada consulta. Mitigación: medir antes de añadir cachés (GLOB-11). Verificación: ninguna caché añadida sin una medición registrada.

**Recomendaciones técnicas a investigar.**

**R5-11 [REC]:** Elegir el marco de interfaz después de DA-24 y de la aprobación de dependencias (GLOB-16).

**R5-12 [REC]:** Mostrar tiempo de desplazamiento, duración de visitas y total, además de la diferencia (DA-24).

**Intervenciones humanas y dependencias.**

**R5-13 [HUMANA]:** Ejecutar los pasos del README en un entorno limpio. Verificación: registro humano con fecha, sistema y resultado.

**R5-14 [HUMANA]:** Decidir tipo de aplicación y marco (DA-24). Verificación: la decisión consta en `specs/R5.md` con autor y fecha humanos.

**Insumos ODD (decide el orquestador).**
- Dependencias bloqueantes: UT-04 (grafo procesado), UT-05 (Dijkstra), UT-08 (archivo de envolvente), UT-09 (Held-Karp y heurística), resultados de R1–R4 y DA-24; no es paralelizable con ellas.
- Superficies de edición disjuntas candidatas: `src/<paquete>/app/`, `tests/app/`, `specs/R5.md`; `README.md` es superficie compartida (REPO-10).
- Exploración de solo lectura: sí, para inspeccionar los formatos reales de los artefactos de R1–R4 y las dependencias de la interfaz elegida, que dependen de decisiones aún abiertas.
- Riesgo concreto: divergencia entre lo mostrado y los resultados de R2–R4. Verificación independiente: no sugerida; R5-02 a R5-04 comparan contra los módulos.

## 4. Protocolo experimental

Se aplica a R1 (R1.3), R2, R3 (R3.2) y R4 (R4.1). `Proyecto_final_2026-2.md §6` es el protocolo vinculante. La única convención de medición del material de clase es `Analisis_de_Algoritmos_03-06.md`, Parte 4, diapositiva 25; donde contradice al enunciado prevalece el enunciado.

| EXP | Parámetro | Valor confirmado y referencia | Estado | Pendiente |
|---|---|---|---|---|
| EXP-01 | Máquina | Misma máquina por requerimiento; reportar procesador, RAM, sistema operativo y versión del lenguaje (`§6, ítem 1`) | Confirmado | — |
| EXP-02 | Región medida | Solo el algoritmo; sin leer archivos, generar datos ni imprimir (`§6, ítem 2`) | Confirmado | — |
| EXP-03 | Repeticiones y estadístico | 5 repeticiones; mediana (`§6, ítem 3`). Clase: 5 repeticiones y promedio (Parte 4, d.25) | Confirmado; conflicto de clase | DA-03 |
| EXP-04 | Ejecuciones largas | Más de un minuto: una sola medición (`§6, ítem 3`) | Confirmado | DA-16 (cómo aplicarlo) |
| EXP-05 | Unidad | Una sola unidad, milisegundos o nanosegundos (`§6, ítem 4`); el Anexo usa ms | Confirmado; ms por Anexo | DA-16 (temporizador) |
| EXP-06 | Semilla | Fija y documentada (`§6, ítem 5`) | Confirmado | DA-17 (valor y derivación) |
| EXP-07 | Verificación previa | Antes de medir, con otra implementación propia, un caso a mano o una biblioteca (`§6, ítem 6`) | Confirmado | — |
| EXP-08 | Límite de tiempo | Más de 5 minutos: se detiene y se reporta «no completada» (`§6, ítem 7`; Anexo, R4). Clase: deducir el resultado sin ejecutar (Parte 4, d.25) | Confirmado; conflicto de clase | DA-04; DA-16 (mecanismo) |
| EXP-09 | Tablas y gráficas | Desde CSV o JSON, con unidad y párrafo (`§6, ítem 8`) | Confirmado | — |
| EXP-10 | Muestra por requerimiento | R1: cuatro radios y departamento; R2: al menos 20 pares con cola y 10 con lineal; R3: nodos de la red y 1 000, 10 000 y 50 000 puntos; R4: k = 5, 6, …, 12 y k = 5, 8, 10 y 12 con al menos 5 instancias | Confirmado | DA-14, DA-17, DA-18 |
| EXP-11 | Comparabilidad | Mismo conjunto de entrada y condiciones similares (Parte 1, d.10); copia de la misma entrada por algoritmo (Parte 4, d.25, ítem 2) | Convención de clase adoptada por el plan | — |
| EXP-12 | Variantes de entrada ordenada o inversa | Parte 4, d.25, ítem 4 | NO ADOPTADO: el enunciado no lo exige | — |
| EXP-13 | Estado limpio por repetición | Decisión del plan | `[PLAN]` | — |
| EXP-14 | Metadatos y tiempos crudos | Decisión del plan | `[PLAN]` | — |
| EXP-15 | Reproducibilidad | Decisión del plan | `[PLAN]` | — |
| EXP-16 | Reanudación de series | Decisión del plan | `[PLAN]` | — |

**EXP-01:** Ejecutar todas las mediciones de un mismo requerimiento en la misma máquina y registrar procesador, RAM, sistema operativo y versión de Python en cada archivo de resultados [ENUNCIADO `§6, ítem 1`; EV-22]. Verificación: prueba de esquema: cada archivo de resultados trae esos metadatos; el arnés rechaza fusionar resultados con metadatos distintos dentro de un mismo requerimiento (prueba con dos huellas de máquina distintas).

**EXP-02:** Medir solo la ejecución del algoritmo; excluir lectura de archivos, generación de datos, conversión de formatos de entrada, impresión y escritura de resultados [ENUNCIADO `§6, ítem 2`]. Verificación: prueba del arnés con una función de prueba que espera fuera y dentro de la región medida: el tiempo reportado incluye solo la espera interna.

**EXP-03:** Repetir cada medición 5 veces, contar las 5 repeticiones sin descartar la primera, reportar la mediana y guardar además los 5 tiempos crudos [ENUNCIADO `§6, ítem 3`; EV-18; DA-03]. Verificación: prueba del arnés con tiempos simulados: la mediana es el tercer valor ordenado; los cinco valores crudos aparecen en el archivo.

**EXP-04:** Medir una sola vez las ejecuciones de más de un minuto [ENUNCIADO `§6, ítem 3`]. Operación [PLAN]: tras la primera repetición, si dura más de un minuto no se repite y se reporta ese valor; si no, se completan las 5 repeticiones aunque una posterior supere el minuto (DA-16). Verificación: prueba del arnés con una función simulada que supera el umbral (configurable en la prueba; la constante real del código es un minuto): se registra una sola medición.

**EXP-05:** Guardar todos los tiempos en milisegundos [ENUNCIADO `§6, ítem 4`; Anexo; EV-20] con un temporizador monotónico de alta resolución (PROPUESTO: `time.perf_counter_ns`, equivalente de `System.nanoTime()` de la Parte 4, diapositiva 25; DA-16) e indicar la unidad en cada tabla y gráfica. Verificación: búsqueda estática de un único punto de conversión a ms; prueba: una función de duración conocida produce el valor esperado con una tolerancia declarada.

**EXP-06:** Fijar una semilla maestra documentada y derivar de ella, de forma determinista, la semilla de cada conjunto o instancia; registrar la semilla efectiva en cada archivo de resultados [ENUNCIADO `§6, ítem 5`; EV-21; DA-17]. Verificación: la de GLOB-07 más una prueba: la semilla efectiva consta en el archivo y regenera el mismo conjunto.

**EXP-07:** Verificar cada algoritmo antes de medirlo (GLOB-06) con otra implementación propia, un caso pequeño resuelto a mano o una biblioteca, y registrar el método usado [ENUNCIADO `§6, ítem 6`]. Verificación: el archivo de resultados referencia el método de verificación; inspección de que el documento técnico explica cómo se verificó cada algoritmo.

**EXP-08:** Detener toda ejecución que pase de 5 minutos y registrarla «no completada», sin tiempo ni valor deducido [ENUNCIADO `§6, ítem 7`; EV-19, EV-27; DA-04]. El mecanismo de corte se decide en DA-16. Verificación: prueba del arnés con límite reducido y una función lenta: estado `no_completada`, ejecución terminada y sin tiempo; búsqueda estática de que la constante del límite real es 5 minutos.

**EXP-09:** Generar tablas y gráficas solo desde archivos CSV o JSON, con unidad y párrafo [ENUNCIADO `§6, ítem 8`]. Verificación: la de GLOB-08 y GLOB-10.

**EXP-10:** Usar en cada requerimiento exactamente las muestras de la tabla (EV-06, EV-07, EV-10, EV-12, EV-13, EV-14) y guardar las listas de entradas (pares, instancias, conjuntos) como archivos de entrada del experimento [ENUNCIADO R1.3, R2.1, R3.2, R4.1, R4.3]. Verificación: prueba: el número de filas de cada archivo de resultados coincide con la muestra exigida; el archivo de entradas existe y se reutiliza al repetir.

**EXP-11:** Comparar algoritmos solo sobre la misma entrada, en la misma máquina, con las mismas estructuras de datos y en el mismo lenguaje; cada algoritmo comparado recibe una copia idéntica de la entrada [ENUNCIADO `§3, «Lenguaje»`, `§6, ítem 1`; EV-32]. Verificación: prueba: el arnés calcula una huella de la entrada entregada a cada algoritmo comparado y las huellas coinciden.

**EXP-12:** No añadir variantes de entrada ordenada ni en orden inverso (Parte 4, diapositiva 25, ítem 4) porque el enunciado no las exige [PLAN; GLOB-27]. Verificación: inspección: los archivos de entradas contienen solo las muestras de EXP-10.

**EXP-13:** Iniciar cada repetición en estado limpio: sin memoización ni cachés compartidos entre repeticiones ni entre algoritmos, y sin mutar la entrada [PLAN: evita mediciones incomparables]. Verificación: búsqueda estática de decoradores de caché en los módulos medidos; prueba: la huella de la entrada es idéntica antes y después de cada repetición.

**EXP-14:** Guardar con cada resultado la versión de Python y de las bibliotecas usadas, la semilla efectiva, la fecha, la máquina y los 5 tiempos crudos [PLAN]. Verificación: prueba de esquema de metadatos.

**EXP-15:** Comprobar la reproducibilidad: dos ejecuciones completas con la misma semilla deben producir idénticas las columnas deterministas (nodos explorados, vértices, costos, rutas, instancias) y tiempos del mismo orden; los tiempos no se exigen idénticos [PLAN]. Verificación: script de comparación: columnas deterministas iguales byte a byte; para los tiempos, reporta mínimo, mediana y máximo de las repeticiones sin criterio numérico de aprobación.

**EXP-16:** Escribir los resultados de forma incremental y permitir reanudar una serie interrumpida sin repetir mediciones completadas y sin mezclar máquinas (EXP-01) [PLAN: recuperabilidad]. Verificación: prueba (a crear): interrumpir una serie simulada y reanudarla produce el mismo archivo final, en las columnas deterministas, que una serie ininterrumpida.

## 5. Repositorio y flujo ODD

**REPO-01:** Organizar el repositorio con la estructura siguiente [PROPUESTA; solo `specs/` aparece en `Proyecto_final_2026-2.md §3` como ejemplo]. Verificación: inspección del árbol contra esta estructura; toda desviación consta como decisión registrada; los directorios de módulos evaluables no contienen scripts de verificación.

```
README.md
specs/            PLAN.md, CONTRATOS.md, R1.md … R5.md
data/             catalogo/, crudo/ (grafo descargado y metadato con fecha), procesado/
src/<paquete>/    comun/, medicion/, red/, caminos/, envolvente/, recorrido/, app/
tests/            espejo de src/<paquete>/
verificacion/     scripts independientes (NetworkX, SciPy, Shapely, oráculos)
experimentos/     ejecutores por requerimiento
resultados/       CSV/JSON, tablas y gráficas
docs/             documento_tecnico.md, uso_ia.md
```

**REPO-02:** Escribir antes de programar cada requerimiento una especificación breve en `specs/R#.md` con su comportamiento esperado y casos de prueba [ENUNCIADO `§3, «Desarrollo guiado por especificaciones»`]. `specs/PLAN.md` conserva las decisiones; `specs/CONTRATOS.md` conserva los esquemas compartidos (catálogo, grafo procesado, asociaciones, matriz, resultados). Cada `R#.md` lista los IDs del plan que cubre y un caso de prueba por criterio de aceptación. Verificación: para cada R, `specs/R#.md` existe antes del primer cambio del código de ese R (historial o documento de feature) y todo criterio `R#-xx` de aceptación figura en su lista de casos de prueba.

**REPO-03:** Nombrar con el ID de la regla las pruebas que la verifican (un caso que verifica R2-03 incluye `R2_03` en su nombre), nombrar los archivos de resultados `resultados/r#_<descripcion>.<ext>`, citar IDs en los mensajes de commit cuando se autoricen y escribir las referencias al enunciado con la forma `Proyecto_final_2026-2.md §5, R2.1` [PLAN]. Verificación: script de cobertura de IDs (a crear): cada ID de aceptación `R#-xx` aparece en al menos una prueba; nombres conformes por búsqueda estática.

**REPO-04:** Preservar los requisitos originales en el documento de feature de ODD con este procedimiento: (1) el orquestador copia literalmente, sin resumir, los fragmentos listados como «Fragmentos literales» de cada R, con archivo y sección; (2) incluye el bloque del Anexo del requerimiento; (3) cita las reglas del plan por ID sin reescribirlas; (4) toda delegación a un subagente remite al localizador del documento de feature, a los IDs aplicables y a las secciones originales; (5) todo subagente lee el documento de feature y los fragmentos originales antes de editar; (6) ante una ambigüedad devuelve una pregunta en lugar de decidir; (7) los escritores no modifican los fragmentos literales. Verificación: script de comparación (a crear) que busca cada fragmento, tomado del archivo fuente, como subcadena del documento de feature y no debe reportar faltantes; inspección de una delegación: cita el localizador y los IDs.

**REPO-05:** No crear ni mover manualmente el documento de feature ni su espejo: los define Gentle Shell (su documentación indica `odd/tasks/<feature-name>.md` y un espejo en memoria; no verificado en este repositorio). Verificación: inspección: no existe un documento de feature manual duplicado en `specs/`.

**REPO-06:** Usar ODD con las especificaciones breves de REPO-02; no activar el flujo SDD/OpenSpec de Gentle Shell sin decisión del usuario; declarar el modo TDD y el ejecutor de pruebas antes de implementar (DA-25); mantener GLOB-19 por encima de cualquier modo de permisos (el README de Gentle Shell indica que su modo YOLO concede permiso permanente para commits y push no forzados; no habilitarlo para este proyecto sin autorización expresa). Verificación: el documento de feature registra el modo de permisos y el modo TDD declarados por el usuario; la de GLOB-19.

**REPO-07:** Llevar el registro de uso de IA en `docs/uso_ia.md` (PROPUESTO) con entradas por tarea: fecha, herramienta y modelo, ID del plan, qué se pidió, qué se aceptó, rechazó o modificó y cómo se verificó. El agente lo mantiene; el anexo final del documento técnico lo redactan y firman personas [ENUNCIADO `§3`; `§7`]. Verificación: script de esquema; cada tarea del documento de feature tiene una entrada completa.

**REPO-08:** Mantener un único manifiesto de dependencias (PROPUESTO) con versiones exactas y el requerimiento que usa cada una; instalar solo lo aprobado (GLOB-16). Verificación: búsqueda estática: todo paquete importado figura en el manifiesto y el manifiesto no contiene paquetes sin uso.

**REPO-09:** Entregar en el repositorio código, datos procesados, resultados de los experimentos y README [ENUNCIADO `§7`, «Repositorio en GitHub»]. El grafo crudo puede excluirse del control de versiones si el procesado y el metadato bastan para reproducir; si un archivo supera el límite del servicio, comprimirlo o usar almacenamiento de archivos grandes solo tras decisión (DA-26). Verificación: inspección: `data/procesado/` y `resultados/` presentes y no excluidos; lista de archivos excluidos justificada.

**REPO-10:** Tratar como superficie propia cada paquete de `src/<paquete>/` con su `tests/`, su `specs/R#.md`, su `experimentos/` y su `resultados/r#`; tratar como superficies compartidas, editadas por una sola unidad a la vez, `src/<paquete>/comun/`, `specs/CONTRATOS.md`, el manifiesto, `README.md` y `docs/` [PLAN]. Verificación: revisión del diff por unidad: cada unidad modifica solo su superficie o las compartidas que se le asignaron.

**REPO-11:** Marcar `BORRADOR` los textos del documento técnico y del README que prepare el agente; el documento técnico sigue la estructura de `§7` (arquitectura con diagrama de componentes y flujo de datos, secciones por requerimiento, conclusiones, anexo de uso de IA) y lo revisan y firman personas [ENUNCIADO `§7`]. Verificación: inspección: existen las cuatro partes; la búsqueda del marcador `BORRADOR` en la versión final devuelve cero coincidencias.

**REPO-12:** Mantener la matriz de cobertura siguiente y comprobar que cada ítem del enunciado tiene al menos una regla [PLAN]. Verificación: script de comparación (a crear) entre la lista de ítems de la matriz y las secciones del enunciado; ningún ítem sin ID.

| Enunciado | Cobertura |
|---|---|
| `§3` Lenguaje; Implementación propia; Librerías | GLOB-01, GLOB-02, GLOB-03, GLOB-04; R1-11, R2-15, R3-12, R4-16, R5-08 |
| `§3` Fuentes; Inteligencia artificial; SDD; Repositorio | GLOB-05, GLOB-23; GLOB-12, GLOB-25, REPO-07; REPO-02; GLOB-19, REPO-01, DA-20 |
| `§4` Red vial; Catálogo | R1-01; GLOB-21, GLOB-22, R1-21, DA-06 |
| `§5` introducción (complejidad con fuente y recurrencia) | GLOB-04, GLOB-05, R2-14, R3-09, R4-03, R4-15 |
| R1.1; R1.2; R1.3 | R1-02, R1-23; R1-03; R1-04, R1-05, R1-10, R1-16 a R1-19, R1-23 |
| R1.4; R1.5 | R1-06, R1-07, R1-12, R1-22; R1-08, R1-09 |
| R2.1 texto; viñeta 1; viñeta 2 | R2-01 a R2-04; R2-05, R2-14; R2-07, R2-08, R2-12 |
| R2.1 viñetas 3, 4 y 5 | R2-09, R2-10; R2-11; R2-06 |
| R3 «Coordenadas»; R3.1; R3.2 | R3-01 a R3-03; R3-04 a R3-06, R3-09; R3-07, R3-08, R3-10 |
| R4 introducción; R4.1; R4.2; R4.3 | R4-01, R4-07; R4-02 a R4-09; R4-10; R4-11 |
| R4.4; R4.5 | R4-12, R4-13; R4-14 |
| R5.1 (cuatro funciones y README) | R5-02, R5-03, R5-04, R5-05; R5-01, R5-07 |
| `§6` ítems 1 a 8 | EXP-01 a EXP-16; GLOB-06 a GLOB-10 |
| `§7`; `§8` | REPO-09, REPO-11, R5-07; sección 2.2 |

## 6. Decisiones abiertas

Ninguna decisión de esta sección es criterio de aceptación. Las recomendaciones son `[PROPUESTA]`.

**DA-01 — Origen de los archivos 03 a 06 individuales y precedencia.**
- Pregunta: ¿se aplica «los individuales prevalecen sobre el consolidado» aunque sean documentos distintos?
- Motivo: el prompt los describe como originales de las presentaciones; sus cabeceras indican `A_FundaAn.pdf` (capítulos de un libro) y el consolidado declara PDF de diapositivas (`03 - Tiempo de ejecución.pdf` … `06 - Algoritmos de Ordenamiento y búsqueda.pdf`). Además `06-ordenamiento.md` solo trata ordenamiento; la búsqueda está en `07-algoritmos-de-busqueda.md`.
- Consecuencia: define qué fuente de clase se cita ante una divergencia.
- Recomendación: aplicar la precedencia solo a las divergencias de DA-02 y, en lo demás, citar la fuente específica (parte y diapositiva, o archivo y sección). Evita atribuir a una fuente contenido de la otra.
- Bloquea: no. Responsable: usuario.

**DA-02 — Divergencias entre `Analisis_de_Algoritmos_03-06.md` y los individuales 03 a 06.**

| # | Tema | Consolidado | Individual | Tratamiento |
|---|---|---|---|---|
| 1 | Regla del límite | Parte 2, d.17 usa o minúscula | `04 §4.3.2` usa O mayúscula | Prevalece 04; la definición de Big-O de la Parte 2, d.10 es idéntica a `04 §4.3.1` |
| 2 | Peor caso de QuickSort | Parte 4, d.14: O(n²) | `06 §6.11`, Cuadro 6.1, «peor caso»: O(n log(n)) | Por regla prevalece 06, pero el enunciado exige citar la complejidad de una fuente (`§5`): el plan no usa ninguna de las dos para QuickHull (R3-20) |
| 3 | Condiciones del benchmarking | Parte 1, d.10: «se recomienda» condiciones similares | `03 §3.2`: «es necesario» hardware con las mismas características | Ambas son compatibles con `§6, ítem 1` (misma máquina), que prevalece |
| 4 | Técnicas de estimación | Parte 1, d.9: benchmarking y análisis | `03 §3.2`: añade profiling | Sin efecto: el proyecto usa benchmarking y análisis |
| 5 | Operaciones elementales | Parte 1, d.12: lista ampliada (condicionales, `new`, incrementos, acumuladores) | `03 §3.3`: lista más corta | Sin efecto: el enunciado pide complejidades de fuente, no conteo de instrucciones |
| 6 | Casos analizados | Parte 1, d.4: mejor y peor caso | `03 §3.1`: solo peor caso | `[PLAN]` reportar el peor caso y, cuando la fuente lo dé, el caso esperado |
| 7 | Método maestro | Parte 3, d.45–48 | `05 §5.7` no lo trae; su Cuadro 5.2 tiene mal transcrita la entrada del caso c > dᵏ («O(n log(n)c)») | Usar Parte 3, d.45–48; el caso de igualdad coincide en ambas fuentes |

- Consecuencia: evita citar una cifra o una regla divergente como si fuera única.
- Recomendación: registrar en el documento técnico solo las divergencias del tema que se cite.
- Bloquea: no. Responsable: usuario (confirmar el tratamiento).

**DA-03 — Estadístico y repeticiones: Parte 4, diapositiva 25 frente a `§6, ítem 3`.**
- Pregunta: ¿mediana o promedio?
- Motivo: la Parte 4, d.25 dice «Repita cada medición 5 veces y reporte el promedio» sin excepción para ejecuciones largas; `§6, ítem 3` dice mediana y una sola medición si pasa de un minuto.
- Consecuencia: define cada celda de tiempo de todas las tablas.
- Recomendación: mediana, porque prevalece el enunciado (resuelta por jerarquía); los 5 tiempos crudos (EXP-03) permiten calcular el promedio sin reportarlo, para evitar ambigüedad.
- Bloquea: no. Responsable: usuario (confirmar).

**DA-04 — Ejecuciones que no terminan: Parte 4, diapositiva 25 frente a `§6, ítem 7`.**
- Pregunta: ¿se deduce el resultado o se reporta «no completada»?
- Motivo: la nota final de la Parte 4, d.25 dice «deberá calcular o deducir el resultado sin ejecutar el algoritmo»; `§6, ítem 7`, `§5, R4.1` y el Anexo dicen «no completada».
- Consecuencia: afecta la versión lineal de R2 y la fuerza bruta de R4, y determina el mayor k resuelto.
- Recomendación: «no completada», porque prevalece el enunciado (resuelta por jerarquía); una extrapolación puede añadirse a la discusión solo si se rotula como estimación y nunca en la celda de la tabla.
- Bloquea: no. Responsable: usuario (confirmar).

**DA-05 — Formulación literal de los valores críticos.**
- Pregunta: ¿se confirman estas interpretaciones? (a) «k de 5 a 12» se lee en `§5, R4.1` como «desde 5 hasta 12, o hasta que una ejecución pase el límite de tiempo de la sección 6 si eso ocurre antes», y el Anexo lista k = 5, 6, …, 12. (b) «40 lugares» se lee en `§4` como «al menos 40 lugares»; los mínimos por categoría suman el mismo total (EV-02). (c) 500 m, 11 h y 5 minutos se confirmaron con la misma formulación; sus bordes se interpretan «a más de 500 m» como estricto, «cabe en una jornada de 11 h» como duración total no superior a 11 h y «pasa de 5 minutos» como más de 5 minutos por ejecución.
- Motivo: el prompt resume los valores y el enunciado añade condiciones o mínimos sin definir bordes.
- Consecuencia: define el número de ejecuciones de k, el tamaño mínimo del catálogo y los bordes de tres umbrales.
- Recomendación: paso 1 en k con corte por límite; catálogo de al menos 40 con los mínimos por categoría; bordes `> 500 m`, `≤ 11 h` y `> 5 minutos`. Es la lectura literal del enunciado y del Anexo.
- Bloquea: no. Responsable: grupo (consultar al docente si hay duda).

**DA-06 — Catálogo.**
- Pregunta: ¿quién elabora el catálogo, con qué fuentes y cómo se registra su verificación?
- Motivo: `§4` dice que «cada grupo arma» el catálogo y exige verificar las coordenadas en un mapa, pero no asigna responsables ni formato de registro.
- Consecuencia: sin catálogo no hay R1.4, matriz de tiempos ni R4.
- Recomendación: el grupo elabora y firma el catálogo (identificador, nombre, municipio, categoría, latitud, longitud y, para atractivos, duración en minutos); el agente solo valida esquema y mínimos por categoría y puede proponer candidatos marcados `NO VERIFICADO`. GLOB-21 y GLOB-22 son tareas humanas.
- Bloquea: sí, R1-06 en adelante. Responsable: grupo.

**DA-07 — Fuente de la red.**
- Pregunta: ¿se autoriza la descarga con OSMnx y cuándo se usa el GraphML del docente?
- Motivo: `§4` prevé el GraphML del docente solo si la descarga falla; GLOB-15 exige consulta previa.
- Consecuencia: define origen y fecha de los datos de todo el proyecto.
- Recomendación: autorizar una descarga única del departamento y de las redes por radio, guardarlas crudas con fecha (R1-01) y no volver a descargar sin nueva autorización; si falla, pedir el GraphML al docente y registrar su origen.
- Bloquea: sí, R1-01. Responsable: usuario.

**DA-08 — Parámetros de descarga y definición de «radio».**
- Pregunta: ¿qué parámetros de `graph_from_place` y `graph_from_point` se usan (tipo de red, tipo de distancia, simplificación, conservación de componentes)?
- Motivo: `§4` y `R1.3` solo dan `network_type="drive"` como ejemplo y «radios de 2, 5, 10 y 20 km».
- Consecuencia: cambia V y E de las cinco redes y el significado de «radio».
- Recomendación: tipo de red `drive` en todas, valores por defecto de la biblioteca para el resto, todos registrados en el metadato y el mismo tipo de distancia en los cuatro radios (R1-19).
- Bloquea: no el código; sí la medición de R1-05. Responsable: grupo.

**DA-09 — Velocidad de los tramos y tramos sin velocidad (R1.2).**
- Pregunta: ¿de dónde sale la velocidad y qué se hace cuando falta?
- Motivo: `R1.2` exige explicarlo pero no fija la política.
- Consecuencia: cambia todos los pesos y, con ellos, los resultados de R2 a R5.
- Recomendación: usar la imputación por tipo de vía que ofrezca la versión instalada de la biblioteca de descarga (R1-18), documentando el valor de respaldo y el tratamiento de unidades y valores no numéricos; no inventar tablas propias sin fuente.
- Bloquea: los resultados de R2 en adelante, no la implementación. Responsable: grupo.

**DA-10 — Sistema de referencia de «UTM zona 18N».**
- Pregunta: ¿qué datum y código EPSG se usan?
- Motivo: `R1.4` y `R3` dicen «UTM zona 18N» sin datum.
- Consecuencia: define las distancias de R1.4 y las coordenadas enteras de R3.
- Recomendación: WGS 84 / UTM 18N con el código EPSG 32618 (valor propuesto, NO ENCONTRADO en el enunciado; EV-40), verificado contra la documentación de la biblioteca de proyecciones. OSM usa WGS 84.
- Bloquea: sí, R1-06 y R3-01 (decisión breve). Responsable: grupo.

**DA-11 — Lugares a más de 500 m.**
- Pregunta: ¿cómo se tratan?
- Motivo: `R1.4` pide reportarlos y explicar el tratamiento sin fijarlo.
- Consecuencia: puede cambiar el catálogo y la matriz.
- Recomendación: primero verificar la coordenada en un mapa (GLOB-21); si persiste, conservar el lugar con su distancia reportada y documentar que sus tiempos excluyen el tramo fuera de la red; reemplazar el lugar solo si su coordenada es incorrecta o inadecuada; nunca eliminarlo en silencio.
- Bloquea: el cierre de R1-08 y de R2-11. Responsable: grupo.

**DA-12 — Algoritmo de envolvente por divide y vencerás (R3.1).**
- Pregunta: ¿cuál se implementa y con qué justificación según la distribución de los puntos de la red?
- Motivo: `R3.1` dice «elegir» y «justificar».
- Consecuencia: define la recurrencia, el riesgo de profundidad de recursión y la comparación con SciPy.
- Recomendación: decidir con la relación vértices/puntos medida con la referencia; si los vértices son pocos frente a n (esperable en una red concentrada), QuickHull es coherente con el criterio y simple de explicar con aritmética entera; si se prioriza una cota de peor caso balanceada, fusión por tangentes (R3-20).
- Bloquea: sí, la implementación de R3. Responsable: grupo.

**DA-13 — Heurística voraz (R4.2).**
- Pregunta: ¿cuál se implementa?
- Motivo: `R4.2` dice «elegida por el grupo».
- Consecuencia: define R4-10, R4-11 y R4-14.
- Recomendación: vecino más cercano dirigido (ir siempre al lugar no visitado de menor tiempo desde el actual y regresar a la partida): constructivo, explicable en una frase, respeta la asimetría y contrasta con Dijkstra (R4.5). Alternativa voraz: inserción más barata.
- Bloquea: sí, R4-10. Responsable: grupo.

**DA-14 — Municipios vecinos y selección de pares (R2).**
- Pregunta: ¿qué municipios son vecinos y cómo se eligen los pares?
- Motivo: `R2.1` pide «mismo municipio o municipios vecinos» y al menos 20 pares sin fijar el método.
- Consecuencia: define el rango de nodos explorados y la validez del cociente.
- Recomendación: tabla de vecindad de los 12 municipios verificada por una persona con mapa o fuente; los 10 pares lineales sorteados con semilla entre pares cercanos; el resto de los pares con cola cubre cercanos y lejanos para ampliar el rango de nodos explorados.
- Bloquea: sí, R2-07. Responsable: grupo.

**DA-15 — Tolerancia numérica.**
- Pregunta: ¿qué tolerancia se usa al comparar tiempos en punto flotante?
- Motivo: `§6, ítem 6` exige que coincidan sin definir tolerancia.
- Consecuencia: define cuándo una verificación pasa o falla.
- Recomendación: igualdad exacta entre las dos versiones propias de Dijkstra (R2-04) y tolerancia relativa propuesta de 10⁻⁹ (EV-39) frente a bibliotecas y entre fuerza bruta y Held-Karp; registrarla en `specs/CONTRATOS.md`.
- Bloquea: no. Responsable: grupo con el verificador.

**DA-16 — Mecánica de medición no fijada por el enunciado.**
- Pregunta: ¿qué temporizador, política de recolección de basura, aislamiento de proceso y mecanismo de corte a 5 minutos se usan, y cómo se aplica «más de un minuto»?
- Motivo: `§6` fija reglas, no mecanismos; la Parte 4, d.25 usa `System.nanoTime()` (Java).
- Consecuencia: validez de todas las mediciones.
- Recomendación: temporizador monotónico de alta resolución (`time.perf_counter_ns`, PROPUESTO); recolección de basura desactivada solo durante la región medida y registrada; cada ejecución medida en un proceso hijo cuyo tope de 5 minutos de reloj de pared termina el proceso padre, y el hijo mide su propio tiempo tras cargar las entradas; descartar comprobaciones cooperativas dentro del algoritmo porque alterarían lo medido (un hilo de Python no puede terminarse desde fuera); para «más de un minuto», decidir tras la primera repetición (EXP-04).
- Bloquea: los experimentos, no el código. Responsable: grupo con verificador independiente.

**DA-17 — Semilla, instancias y su derivación.**
- Pregunta: ¿cuál es la semilla maestra, cómo se derivan las semillas de conjuntos e instancias, cuántas instancias por k se usan para la curva de R4.1 y se reutilizan en R4.3?
- Motivo: `§6, ítem 5` exige semilla fija y documentada sin valor (EV-38); `R4.1` no fija instancias por k para la curva.
- Consecuencia: reproducibilidad de R2, R3 y R4.
- Recomendación: una semilla maestra entera elegida por el grupo antes de la primera medición; semillas derivadas de forma determinista (semilla maestra más un índice estable por conjunto); una instancia por k para la curva (R4-25 verifica que los tiempos exactos no dependen del contenido de la matriz), reutilizada como instancia 1 de R4.3 para k = 5, 8, 10 y 12.
- Bloquea: los experimentos. Responsable: grupo.

**DA-18 — Definiciones operativas no fijadas en R3 y R4.**
- Pregunta: ¿qué regla de empate en .5 se usa al redondear; qué devuelve la envolvente de conjuntos que no forman polígono; qué lado tiene el cuadrado de R3.2, cómo se generan sus puntos, qué `n` se reporta y cómo se define «Cociente»; cuál es la fórmula de la brecha de R4.3?
- Motivo: `R3` y `R4.3` no lo definen; el Anexo nombra columnas sin definirlas (EV-41).
- Consecuencia: define los valores de las tablas de R3 y R4.
- Recomendación: regla de la función de redondeo usada, documentada; para conjuntos degenerados, devolver los puntos extremos distintos; lado igual a la mayor dimensión del rectángulo envolvente de los nodos en UTM; coordenadas enteras uniformes generadas directamente; `n` igual a los puntos tras deduplicar, con una columna adicional para los generados; cada versión recibe su formato natural preparado fuera de la región medida; Cociente = tiempo propio ÷ tiempo SciPy, indicado en el encabezado; brecha = (costo de la heurística − costo de Held-Karp) ÷ costo de Held-Karp × 100, con promedio y máximo por k.
- Bloquea: no. Responsable: grupo.

**DA-19 — Duración de visita: fuente o criterio.**
- Pregunta: ¿se exige fuente?
- Motivo: el prompt pide justificar «con fuentes»; `§4` admite «una fuente o un criterio definido por el grupo».
- Consecuencia: define GLOB-22.
- Recomendación: prevalece el enunciado; preferir fuente citada y usar criterio escrito solo si no existe.
- Bloquea: el cierre de R4-12. Responsable: grupo.

**DA-20 — Commits, push y autoría.**
- Pregunta: ¿cómo se autorizan commits y push y quién figura como autor?
- Motivo: GLOB-19 es política deliberada; `§3, «Repositorio»` usa el historial como evidencia del trabajo de cada integrante; el flujo ODD puede incluir un cierre con commit y el modo YOLO de Gentle Shell concede permiso permanente (según su README, no verificado aquí).
- Consecuencia: evita atribuir a una persona trabajo del agente y evita commits no autorizados.
- Recomendación: no habilitar el modo YOLO; commits hechos por la persona integrante tras revisar el diff, con una línea de coautoría que declare la asistencia de IA; el agente propone el mensaje y cada operación se autoriza por separado.
- Bloquea: sí, antes del primer commit. Responsable: usuario y grupo (consultar al docente si la coautoría afecta la evaluación individual).

**DA-21 — Bibliotecas estándar y NumPy en algoritmos propios.**
- Pregunta: ¿se permiten funciones de enumeración (`itertools`), memoización automática o NumPy dentro de los algoritmos propios y medidos?
- Motivo: `§3` permite librerías para «estructuras de apoyo y las operaciones de ordenamiento», prohíbe las que «resuelvan» el algoritmo y exige mediciones comparables, pero no clasifica estas funciones.
- Consecuencia: define R2-13, R4-02 y las tablas de bibliotecas.
- Recomendación: no en los algoritmos evaluables y medidos (R2, R3 propia, R4); sí en scripts de verificación. La enumeración es parte de la fuerza bruta, la memoización oculta el tamaño de la tabla de Held-Karp (R4.1) y mezclar NumPy con Python puro distorsiona la comparación. Si el grupo quiere permitir alguna, consultar al docente.
- Bloquea: no; se aplica el valor por defecto. Responsable: grupo.

**DA-22 — Reglas de borde del itinerario (R4.4).**
- Pregunta: ¿se admite una cantidad de atractivos menor que el mínimo tras quitar; el límite de 11 h es inclusivo; se visita el lugar de partida; con qué criterio se quitan atractivos?
- Motivo: `R4.4` no lo define.
- Consecuencia: define R4-12 y R4-27.
- Recomendación: admitir menos atractivos tras quitar registrando la cantidad final; «cabe» si la duración no supera 11 h; la partida no se visita, no suma tiempo de visita y no cuenta entre los atractivos; criterio escrito por el grupo antes de calcular.
- Bloquea: R4-12. Responsable: grupo.

**DA-23 — Permisos adicionales.**
- Pregunta: ¿qué comandos de verificación quedan autorizados y se autoriza la consulta web de documentación y fuentes y el acceso a las teselas del mapa?
- Motivo: el plan lista categorías de permisos, no comandos; el silencio no autoriza.
- Consecuencia: define lo que el agente puede hacer sin consultar.
- Recomendación: autorizar por escrito (a) la suite de pruebas y los scripts de verificación, con comandos exactos fijados al crear el documento de feature; (b) consulta web de solo lectura para documentación y fuentes de complejidad; (c) teselas en R5 solo en ejecución local. Todo lo demás, por consulta.
- Bloquea: sí, antes de ejecutar verificaciones y de investigar fuentes. Responsable: usuario.

**DA-24 — Aplicación (R5).**
- Pregunta: ¿web o escritorio, qué marco, en qué unidad se muestra el tiempo, se muestra el desglose y se muestra la comprobación de 11 h?
- Motivo: `R5.1` solo dice «web o de escritorio» y «tiempo total de cada uno».
- Consecuencia: define las dependencias de R5.
- Recomendación: aplicación web local con un marco de Python de interfaz sencilla (PROPUESTO, tras GLOB-16); mostrar tiempo de desplazamiento, duración de visitas y total, y la diferencia entre la heurística y Held-Karp; la comprobación de 11 h no es requisito de R5 y no se añade sin autorización.
- Bloquea: la elección de dependencias de R5. Responsable: grupo.

**DA-25 — Modo TDD, ejecutor de pruebas y flujo SDD de Gentle Shell.**
- Pregunta: ¿TDD activado o no, con qué ejecutor de pruebas, y se usa el SDD/OpenSpec de Gentle Shell o solo ODD con `specs/`?
- Motivo: el entorno no está verificado y ODD toma estas decisiones de la configuración o del usuario (según su documentación); no deben inventarse.
- Consecuencia: define cómo se implementa y verifica cada tarea.
- Recomendación: ODD con las especificaciones breves de REPO-02, que cumplen `§3`, sin SDD/OpenSpec; TDD activado para los módulos de algoritmos de R2, R3 y R4 porque cada criterio ya define su prueba; ejecutor a elegir por el usuario (PROPUESTO: pytest).
- Bloquea: sí, antes de la primera tarea de implementación. Responsable: usuario.

**DA-26 — Tamaño de los datos procesados.**
- Pregunta: ¿cómo versionar archivos que superen el límite del servicio de alojamiento?
- Motivo: `§7` exige datos procesados en el repositorio y su tamaño se conoce solo después de R1.
- Consecuencia: define REPO-09.
- Recomendación: medir tamaños tras R1-08; comprimir o usar almacenamiento de archivos grandes solo con autorización (GLOB-16, DA-23); excluir el grafo crudo si el metadato y el procesado bastan.
- Bloquea: no. Responsable: grupo.
