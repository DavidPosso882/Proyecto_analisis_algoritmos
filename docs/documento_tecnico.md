# Documento técnico — Red vial del Quindío, caminos mínimos, envolvente y ruta óptima

> **Firmado:** David Posso, 2026-11-04. Revisión humana realizada; R5-13 (ejecución en limpio) queda como único pendiente registrado en §8.

Proyecto final de Análisis de Algoritmos. Todos los algoritmos evaluables son de
implementación propia en Python puro; las bibliotecas externas solo se usan para
preparar datos, graficar o verificar de forma independiente (GLOB-02, GLOB-03).

## 1. Arquitectura de la solución

### 1.1 Diagrama de componentes

```text
                    ┌──────────────────────────────┐
   descarga única → │ red/        R1               │ → data/crudo/
   (OSMnx, DA-07)   │ descarga, pesos, componente, │
                    │ asociaciones, grafo procesado│ → data/procesado/
                    └──────────────┬───────────────┘
                                   │ componente.graphml, grafo_idx.json,
                                   │ indices.json, asociaciones.csv
             ┌─────────────────────┼──────────────────────┐
             ▼                     ▼                      ▼
   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐
   │ caminos/   R2    │  │ envolvente/  R3  │  │ recorrido/   R4    │
   │ Dijkstra lineal  │  │ QuickHull entero │  │ fuerza bruta,      │
   │ y con cola       │  │ + referencia     │  │ Held-Karp, voraz   │
   └────────┬─────────┘  └────────┬─────────┘  └─────────┬──────────┘
            │ matriz_tiempos.csv  │ vertices_red.csv     │ tablas y JSON
            ▼                     ▼                      ▼
                        ┌──────────────────────┐
   data/catalogo/  ───→ │ app/  R5 (Flask)     │ ←── resultados/r1..r4/
   catalogo.csv         │ lee y calcula al     │
                        │ momento, no descarga │
                        └──────────────────────┘
```

### 1.2 Flujo de datos entre requerimientos

1. **R1** descarga la red, calcula pesos (distancia y tiempo), se queda con la
   componente fuertemente conexa, asocia cada lugar del catálogo a un nodo y
   guarda el grafo procesado con índices contiguos. Ese grafo es la única
   entrada de R2, R3 y R4.
2. **R2** ejecuta Dijkstra sobre la componente y produce las mediciones, la
   matriz dirigida de tiempos 40 × 40 (`resultados/r2/matriz_tiempos.csv`) y la
   gráfica del cociente entre versiones. La matriz alimenta a R4 y a la
   aplicación.
3. **R3** toma las coordenadas UTM de los nodos de la componente, las redondea a
   enteros, elimina duplicados y calcula la envolvente con QuickHull propio;
   guarda los vértices en `resultados/r3/vertices_red.csv` para que la
   aplicación los dibuje sin recalcular.
4. **R4** usa la matriz de R2 para la curva de soluciones exactas, la calidad de
   la heurística y el itinerario de un día.
5. **R5** (aplicación) lee el grafo procesado, el catálogo, la matriz de R2 y los
   vértices de R3; calcula rutas e itinerarios al momento con los módulos de R2
   y R4 y muestra las tablas y gráficas guardadas en `resultados/`.

### 1.3 Protocolo experimental y máquinas de medición

Todas las mediciones pasan por el arnés propio (`src/quindio/medicion/arnes.py`),
que aplica el protocolo de la sección 6 del enunciado:

- Cada medición corre en un **proceso hijo** (`multiprocessing`, contexto
  `spawn`) que recibe la entrada ya preparada; solo se mide el algoritmo, con
  `time.perf_counter_ns` y el recolector de basura desactivado dentro de la
  región medida. Leer archivos, generar datos e imprimir quedan por fuera.
- **5 repeticiones y se reporta la mediana**. Si la primera repetición pasa de
  60 s, se mide una sola vez. Si una ejecución pasa de **5 minutos**, se detiene
  el proceso hijo y se registra como `no_completada`, sin tiempo.
- Tiempos guardados en **milisegundos**. Datos aleatorios con **semilla fija**:
  maestra 42 y derivadas `42 + índice`, documentadas en cada archivo de resultados.
- Antes de medir, cada algoritmo se **verifica** (contra otra implementación
  propia, un caso resuelto a mano o una biblioteca); si la verificación falla,
  no se mide.
- Cada fila de resultados guarda la **huella de la máquina**, los 5 tiempos
  crudos, la semilla y la huella de la entrada. Al fusionar resultados, el arnés
  rechaza filas de máquinas distintas.

**Máquinas.** El proyecto se midió completo en dos máquinas:

| | Máquina A (Linux) | Máquina B (Windows) |
|---|---|---|
| Procesador | AMD Ryzen 7 5800H (8 núcleos / 16 hilos, 3,2 GHz base) | Intel Core i5-1135G7 de 11.ª generación (4 núcleos / 8 hilos, 2,4 GHz base) |
| Memoria RAM | 16 GB DDR4-3200 (15 372 MB disponibles para el sistema) | 16 GB (16 149 MB disponibles para el sistema) |
| Sistema operativo | Fedora Linux 44, kernel 7.2.11-200.fc44.x86_64 | Windows 11 Home Single Language, compilación 26200 |
| Python | 3.14.8 | 3.14.0 |
| Bibliotecas | SciPy 1.18.1, NumPy 2.5.4, NetworkX 3.7, OSMnx 2.1.1 | las mismas versiones |
| Fechas de medición | 2026-10-27 a 2026-11-04 | 2026-11-14 |
| Resultados | `resultados/linux/` | `resultados/r1` a `resultados/r4` (vigentes) |

Se cumple la regla de que las mediciones de un mismo requerimiento se hacen en
la misma máquina: **cada requerimiento se midió completo en cada una**, y nunca
se mezclan filas de las dos en una misma tabla o gráfica. Los resultados
vigentes del documento son los de la máquina B, que además usan el catálogo con
las coordenadas corregidas de A13, F01 y F03. Los de la máquina A se conservan
sin cambios como referencia para la comparación de la sección 7.1.

Las dos máquinas difieren a la vez en **procesador y sistema operativo**, así
que la comparación de la sección 7.1 no aísla el efecto del sistema operativo:
muestra cuánto cambian los tiempos absolutos entre dos equipos reales y si se
mantienen las conclusiones del análisis (crecimiento con el tamaño de la
entrada, cocientes entre versiones y mayor k resuelto).

## 2. Requerimiento 1 — Modelo de la red vial

**Problema.** Representar la red vial del Quindío con pesos utilizables por los
algoritmos siguientes y quedarse solo con la parte donde existe camino dirigido
entre cualquier par de nodos.

**Representación.** Con V = 8 819 y E = 20 184 aristas (multigrafo) la matriz de
adyacencia ocuparía ~593 MB (celdas de 8 bytes) y las listas de adyacencia
~0,53 MB; se eligen listas de adyacencia (`cifras_r1a.json`). El detalle del
supuesto está en ese archivo y en la sección de resultados.

**Pesos.** Cada arista guarda distancia en metros y tiempo de viaje en segundos.
La velocidad de cada tramo se imputó con la media de `maxspeed` por tipo de vía
(la imputación de la versión instalada de OSMnx, 2.1.1); los tipos sin ningún
`maxspeed` usan la media global y el tiempo es
`travel_time = length / speed` (`src/quindio/red/pesos.py`). El tiempo es una
estimación del modelo, no un tiempo real de recorrido.

**Componente fuertemente conexa.** Se usa la llamada literal
`ox.truncate.largest_component(G, strongly=True)`, que internamente aplica el
algoritmo de Tarjan iterativo (`strongly_connected_components`, NetworkX 3.7)
con las mejoras de Tarjan y Zwick. Complejidad **O(V + E)** en tiempo y
**O(V)** en memoria (Tarjan, 1972, *Depth-first search and linear graph
algorithms*, SIAM J. Comput. 1(2)).

**Resultados.**

| Red | Nodos | Aristas |
|---|---|---|
| Red descargada | 8 819 | 20 184 |
| Componente fuertemente conexa | 8 803 | 20 163 |

| Red | V | E | V + E | Tiempo (ms) |
|---|---|---|---|---|
| Radio de 2 km | 1 639 | 3 639 | 5 278 | 30,527 |
| Radio de 5 km | 4 297 | 9 710 | 14 007 | 85,866 |
| Radio de 10 km | 5 929 | 13 376 | 19 305 | 123,022 |
| Radio de 20 km | 8 786 | 20 078 | 28 864 | 185,765 |
| Departamento completo | 8 819 | 20 184 | 29 003 | 186,274 |

*Unidad:* milisegundos, mediana de 5 ejecuciones (EXP-05); `V + E` es el tamaño
de entrada. *Lectura:* el tiempo crece con V + E y las dos redes más grandes
casi empatan, lo que coincide con el costo lineal esperado del algoritmo; no se
observan saltos que sugieran otra complejidad (GLOB-10). Fuente:
`resultados/r1/t_componente.csv`, `resultados/r1/cifras_r1a.json`.

**Qué cubre cada «radio».** Las redes de 2, 5, 10 y 20 km se descargaron con
`ox.graph_from_point(..., dist=r, dist_type="bbox")` (parámetros en
`data/crudo/*.meta.json`). Con `dist_type="bbox"`, OSMnx no descarga un
círculo sino un **cuadrado de lado 2·r** centrado en la plaza de Bolívar, y no
lo recorta al límite del departamento. La comparación de los ids de nodo con la
red del departamento (`verificacion/r1_radios.py`) muestra qué cubre cada una:

| Red | Cuadro | Nodos | Del Quindío | De otros departamentos | Nodos del Quindío cubiertos |
|---|---|---|---|---|---|
| Radio de 2 km | 4 × 4 km | 1 639 | 1 639 | 0 | 18,7 % |
| Radio de 5 km | 10 × 10 km | 4 297 | 4 297 | 0 | 48,8 % |
| Radio de 10 km | 20 × 20 km | 5 929 | 5 929 | 0 | 68,0 % |
| Radio de 20 km | 40 × 40 km | 8 786 | 8 403 | 383 | 95,3 % |

Las tres primeras redes son subconjuntos de la del departamento. La de 20 km
tiene casi el mismo tamaño que el departamento (8 786 frente a 8 819 nodos),
pero **no es la misma red**: Armenia está a 36,7 km del borde sur de la red del
departamento (Génova y Pijao) y a unos 20 km de los demás bordes, así que el
cuadro de 40 × 40 km deja fuera unos 400 nodos del sur y, a cambio, incluye 383
nodos de los departamentos vecinos. Por eso su tiempo es casi igual al del
departamento: el algoritmo es lineal en V + E y las dos redes tienen un tamaño
de entrada casi igual (28 864 frente a 29 003), no porque cubran la misma zona.

**Discusión.** Trabajar solo con la componente evita respuestas «sin camino» en
R2 y R4 y reduce el grafo en 16 nodos y 21 aristas.

**Ubicación de los lugares (R1.4).** Cada lugar del catálogo se asocia al nodo
de la componente más cercano en línea recta, con distancia euclidiana entre
coordenadas en metros (UTM 18N, EPSG:32618); la asociación se verifica contra un
árbol KD de SciPy y contra la distancia geodésica (`verificacion/r1_asociacion.py`).

En una primera versión del catálogo, 7 lugares quedaban a más de 500 m. Al
revisarlos en el mapa (2026-11-14) se encontró que tres coordenadas eran
aproximadas y se corrigieron: A13 (Barbas-Bremen) pasó de 994 m a 589 m de su
nodo, F03 (Hotel El Edén) de 877 m a 443 m y F01 (Café San Alberto) de 526 m a
273 m. Las otras coordenadas se confirmaron como correctas. Con el catálogo
corregido quedan **5 lugares a más de 500 m**:

| Id | Lugar | Distancia al nodo (m) | Por qué queda lejos de la red | Tratamiento |
|---|---|---|---|---|
| A12 | Reserva Natural Acaime | 3 522 | al final de un sendero peatonal, sin vía para carros | se conserva; limitación documentada (ver abajo) |
| A15 | Camino Nacional del Quindío | 1 115 | sendero histórico sin acceso vehicular directo | se conserva; coordenada verificada |
| A03 | Valle de Cocora | 1 062 | el punto del catálogo está dentro del valle, lejos del final de la vía | se conserva; coordenada verificada |
| A13 | Parque Natural Regional Barbas-Bremen | 589 | reserva forestal; el acceso es por un camino interno | se conserva; coordenada corregida |
| F07 | Finca Hotel La Bella Villa | 547 | finca con acceso por un carreteable interno que no está en la red | se conserva; coordenada verificada |

Ningún lugar se eliminó: el enunciado exige al menos 15 atractivos y el
catálogo tiene exactamente 15. El tratamiento común es conservar el lugar y
asociarlo a su nodo más cercano, que funciona como el **punto de acceso por
carretera**. La consecuencia para R2 y R4 es que el tiempo calculado llega hasta
ese punto de acceso y **no incluye el último tramo** (a pie o por un camino
privado). Para estos 5 lugares el tiempo del modelo subestima el tiempo real;
para los otros 35 la diferencia es menor de 500 m.

**Limitación de Acaime (A12).** Acaime y el Valle de Cocora (A03) quedan
asociados al **mismo nodo**: el nodo vial más cercano a Acaime es el final de
la vía del valle. En `data/procesado/asociaciones.csv` ambos lugares tienen el mismo `nodo_id`
(1543526033). Por eso la matriz de tiempos asigna **0 s** a A03 → A12 y a
A12 → A03, aunque en la realidad separa a los dos una caminata de varias horas.
El grupo decidió conservar el lugar y documentar la limitación, porque la red
modela solo vías para carros (`network_type="drive"`) y el enunciado aclara que
el tiempo es una estimación del modelo y no el tiempo real. Los algoritmos no se
ven afectados en su corrección, porque resuelven bien el problema sobre la
matriz que reciben. Esto influye en los resultados en tres lugares:

- R2: el par medido A12 → A09 sale desde el nodo de Cocora.
- R4: dos instancias contienen A03 y A12 a la vez (curva con k = 9 y la
  instancia 5 de calidad con k = 10). En ambas el tramo entre los dos cuesta
  0 s, así que el óptimo de Held-Karp los visita seguidos.
- Itinerario de un día: no se ve afectado, porque A12 es uno de los dos
  atractivos que se quitan para que la jornada quepa en 11 h y A03 no está en
  la selección.

## 3. Requerimiento 2 — Caminos mínimos

**Problema.** Calcular el camino de menor tiempo de viaje entre dos lugares del
catálogo con implementación propia.

**Algoritmo.** Dijkstra en dos versiones: mínimo por recorrido lineal y mínimo
con cola de prioridad (`heapq`). Ambas se detienen al extraer el destino y
reconstruyen la ruta por predecesores.

**Correctitud.** Invariante: al extraer un nodo, su distancia ya es óptima,
porque todo camino alternativo hacia él pasaría por un nodo no extraído de
distancia mayor o igual. Por eso es correcto detenerse al extraer el destino. La
condición es que los pesos sean finitos y no negativos, lo que se cumple porque
son tiempos de viaje.

**Complejidad.** Versión lineal **O(V²)** en tiempo y **O(V)** en memoria;
versión con cola **O((V + E) log V)** en tiempo y **O(V)** en memoria (Cormen,
Leiserson, Rivest y Stein, *Introduction to Algorithms*, 3.ª ed., §24.3; el
costo de `heapq` se incluye según GLOB-04).

**Resultados.** 20 pares medidos con la versión de cola y 10 de ellos también con
la lineal (`resultados/r2/mediciones_anexo.csv`). La gráfica
`resultados/r2/grafica_nodos_ms.png` tiene nodos explorados en el eje horizontal
y tiempo en milisegundos en el vertical, con una serie por versión.

| Cociente lineal / cola | Valor |
|---|---|
| Mediana | 149,84 |
| Mínimo | 5,99 |
| Máximo | 189,60 |

*Unidad:* el cociente es adimensional (tiempos en ms). *Lectura:* la versión
lineal tarda ~150 veces más en mediana, coherente con O(V²) frente a O((V + E) log V) en
una red de 8 803 nodos; el mínimo (6x, par F05→A09) corresponde a un par cercano
con pocos nodos explorados y el máximo (190x, A01→A02) a un par largo; la diferencia también incluye el costo de las
estructuras de cada implementación propia. Fuente:
`resultados/r2/cociente.json`.

**Matriz de tiempos.** `resultados/r2/matriz_tiempos.csv` es dirigida y no
simétrica (40 × 40, diagonal cero, segundos); se obtuvo con la versión de cola
ejecutada una vez por origen sin detenerse en un destino. Es la entrada de R4 y
del itinerario de la aplicación.

**Verificación.** Las dos versiones coinciden en los 10 pares medidos con ambas
(`verificacion/dijkstra_contra_bellmanford.py` con Bellman-Ford propio y
`verificacion/r2_matriz.py` con NetworkX fuera de los módulos medidos).

## 4. Requerimiento 3 — Envolvente convexa de la red vial

**Problema.** Aproximar la extensión de la red con el menor polígono convexo que
contiene sus nodos.

**Preparación.** Coordenadas UTM 18N (EPSG:32618) redondeadas al entero más
cercano con regla .5 hacia arriba y deduplicadas; los puntos alineados sobre los
lados no son vértices. Los predicados usan solo aritmética entera exacta.

**Algoritmo.** QuickHull (elegido por ser dividir y vencerás y por la
distribución concentrada de la red: razón vértices/puntos medida = 0,0016).
Fuente: Barber, Dobkin y Huhdanpaa, *The Quickhull algorithm for convex hulls*,
ACM TOMS 22(4), 1996.

**Recurrencia y complejidad.** Con m puntos a la izquierda de un segmento
dirigido, se elige el más lejano (búsqueda lineal) y se recurre en los dos
subconjuntos:

```text
T(m) = T(m1) + T(m2) + O(m),  con m1 + m2 ≤ m
```

Peor caso **O(n²)** en tiempo (puntos en círculo); caso esperado **O(n log n)**
en nubes concentradas. Memoria **O(n)**. Se suma el costo del ordenamiento de
biblioteca usado para extremos y particiones (Timsort de Python, O(n log n)).

**Resultados.** `resultados/r3/tabla_anexo_r3.csv`:

| Conjunto de puntos | n | Vértices | Tiempo propio (ms) | Tiempo SciPy (ms) | Cociente |
|---|---|---|---|---|---|
| Nodos de la red | 8 803 | 14 | 9,719 | 1,258 | 7,73 |
| Cuadrado, 1 000 puntos | 1 000 | 17 | 1,975 | 0,430 | 4,59 |
| Cuadrado, 10 000 puntos | 10 000 | 22 | 13,760 | 1,466 | 9,39 |
| Cuadrado, 50 000 puntos | 50 000 | 34 | 73,127 | 6,622 | 11,04 |

*Unidad:* milisegundos; `n` es tras deduplicar. *Lectura:* el tiempo propio
crece de forma aproximadamente lineal-logarítmica y el cociente frente a SciPy
se mantiene entre 4,6 y 11,0, con tendencia a crecer con n porque la referencia
está compilada (Qhull en C) mientras la implementación propia es Python puro;
los vértices coinciden con SciPy en las cuatro filas. Fuente:
`resultados/r3/mediciones.csv`, `resultados/r3/scipy_info_r3.md`.

**Uso en R5.** Los 14 vértices se guardan en
`resultados/r3/vertices_red.csv` (coordenadas enteras UTM y lon/lat) y la
aplicación los dibuja sin recalcular (R3-11, R5-03).

## 5. Requerimiento 4 — Ruta óptima de recorrido

**Problema.** Salir de un lugar del catálogo, visitar k lugares y regresar
minimizando el tiempo total, con la matriz dirigida de R2 (TSP asimétrico).

### 5.1 Soluciones exactas

**Subestructura óptima.** Si al tour óptimo que sale de 0 le quito el último
tramo j → 0, lo que queda es un camino óptimo que sale de 0, visita un
subconjunto y termina en j; si existiera otro más barato, empalmándolo con
j → 0 se obtendría un tour mejor, contradicción.

**Recurrencia (Held-Karp).** Con C(S, j) el costo mínimo de salir de 0, visitar
exactamente S y terminar en j:

```text
C({j}, j) = c[0][j]
C(S, j)   = mín { C(S∖{j}, i) + c[i][j] }  para i ∈ S, i ≠ j
óptimo    = mín { C(V∖{0}, j) + c[j][0] }  para j ≠ 0
```

**Complejidad.** Fuerza bruta **O(k!)** en tiempo y **O(k)** en memoria;
Held-Karp **O(k²·2^k)** en tiempo y **O(k·2^k)** en memoria (Bellman, 1962,
JACM 9(1); Held y Karp, 1962, J. SIAM 10(1)). La tabla usa k·2^k entradas de 8
bytes (R4-05).

**Resultados.** `resultados/r4/tabla_exactos.csv` y la gráfica
`resultados/r4/grafica_k_ms.png`:

| k | Fuerza bruta (ms) | Held-Karp (ms) |
|---|---|---|
| 5 | 0,189 | 0,095 |
| 6 | 0,951 | 0,205 |
| 7 | 7,058 | 0,464 |
| 8 | 60,983 | 1,043 |
| 9 | 588,557 | 2,456 |
| 10 | 6 451,338 | 5,953 |
| 11 | 73 175,226 | 14,344 |
| 12 | no completada | 33,794 |

*Unidad:* milisegundos, mediana de 5 ejecuciones. *Lectura:* la fuerza bruta
se multiplica por 4 a 12 en cada paso de k (crecimiento factorial) y se corta en
k = 12 por límite de tiempo, mientras Held-Karp crece como k²·2^k; el mayor k
resuelto por ambos métodos es 11 y, en k = 5 a 11, los dos devuelven el mismo
costo óptimo (`resultados/r4/curva_exactos.csv`, verificación R4-06), lo que
coincide con las complejidades declaradas. Fuente:
`resultados/r4/tabla_exactos.csv`, `resultados/r4/curva_exactos.csv`.

### 5.2 Heurística voraz y su calidad

Se eligió **vecino más cercano dirigido**: desde la partida se va siempre al
lugar no visitado de menor tiempo y al final se regresa; desempate por menor
índice. Es constructiva pura, sin mejoras no voraces, y su costo es
**O(k²)** en tiempo y **O(k)** en memoria.

| k | Instancias | Brecha promedio (%) | Brecha máxima (%) | Brecha mínima (%) |
|---|---|---|---|---|
| 5 | 5 | 3,3158 | 5,0487 | 2,2453 |
| 8 | 5 | 4,8725 | 11,3227 | 0,0090 |
| 10 | 5 | 10,0750 | 16,7878 | 3,1285 |
| 12 | 5 | 11,7232 | 22,0549 | 5,7446 |

*Unidad:* brecha en porcentaje, (heurística − Held-Karp) / Held-Karp × 100.
*Lectura:* la brecha es no negativa porque Held-Karp es óptimo y crece con k como
se espera de una heurística constructiva. Fuente:
`resultados/r4/tabla_calidad.csv`, `resultados/r4/calidad_brechas.csv`.

**Por qué el voraz falla aquí y no en Dijkstra.** En Dijkstra la elección voraz
es segura porque, con pesos no negativos, la distancia mínima ya fijada no puede
mejorarse después (subestructura óptima del camino mínimo). En el TSP la mejor
arista inmediata puede dejar el tour atrapado en una secuencia cara: la solución
se arma con una decisión local que no considera el resto del ciclo, como muestran
las brechas de la tabla.

### 5.3 Itinerario de un día

Partida Armenia (C01, no se visita ni cuenta), selección inicial de 8 atractivos
por sorteo con semilla derivada 42 + 900 y quitas sucesivas mientras la jornada
supere 11 h, con el criterio escrito antes de calcular (DA-22). Resultado final:
6 atractivos, 420 min de visitas, 184,88 min de desplazamientos y 10,081 h de
jornada (`resultados/r4/tabla_itinerario.csv`).

*Unidad:* desplazamientos y visitas en minutos, acumulado y jornada en horas.
*Lectura:* el itinerario cabe en la jornada de 11 h tras quitar dos atractivos
(A12 y A13), que son los que más tiempo total ahorran.

**Firma humana R4-27.** David Posso, 2026-11-04: se confirman la selección inicial de 8 atractivos (A07, A04, A12, A13, A14, A10, A05, A08) y las quitas A12 y A13 por mayor ahorro de tiempo total según criterio DA-22 registrado en `resultados/r4/itinerario_criterio_previo.json`. Jornada final 10,081 h, cabe en 11 h.

## 6. Requerimiento 5 — Aplicación

**Alcance.** Aplicación web local (Flask 3.1.2, DA-24) que se ejecuta con
`PYTHONPATH=src .venv/bin/python -m quindio.app` y escucha en
`http://127.0.0.1:5000` (R5-01, R5-07).

| Pantalla | Contenido | Regla |
|---|---|---|
| `/ruta` | origen y destino del catálogo, ruta sobre el mapa y tiempo de viaje calculados al momento con Dijkstra de cola | R5-02 |
| `/envolvente` | polígono de la envolvente leído de `resultados/r3/vertices_red.csv` (14 vértices, igual a la fila «Nodos de la red») | R5-03 |
| `/itinerario` | partida (por defecto Armenia) y 6 a 8 atractivos; recorrido, totales y diferencia de Held-Karp y del voraz; rechazo fuera de rango | R5-04 |
| `/resultados` | tablas y gráficas de R1 a R4 leídas de `resultados/` con su unidad de tiempo y una lectura breve | R5-05, GLOB-08, GLOB-10 |

**Bibliotecas.** El cálculo usa solo los módulos propios de R2 y R4; el marco es
Flask y el mapa se dibuja con Leaflet sobre teselas de OpenStreetMap. La
aplicación no importa NetworkX, OSMnx, SciPy, ni el módulo de descarga, ni el
arnés de medición (R5-06, R5-08); una prueba estática recorre las importaciones
del paquete y otra sustituye la descarga por un doble que falla y comprueba que
la aplicación arranca y responde.

**Trazabilidad mostrado ↔ resultados.** Las pruebas de integración fijan la
coincidencia con los artefactos: los 20 pares de `mediciones_anexo.csv` y el
módulo `dijkstra_cola` (R5-02), el conteo de vértices de R3-08/R3-11 (R5-03) y
la selección final del itinerario de R4 con totales idénticos y diferencia no
negativa (R5-04).

**Riesgos.** R5-09: las teselas del mapa requieren red al usar la aplicación, lo
que está documentado en el README; sin conexión, el tiempo de viaje, los
vértices y las tablas siguen disponibles. R5-10: la carga de datos se midió antes
de decidir que fuera única (0,72 s al arrancar; consultas de ruta de 7 a 18 ms) y
no se añadió ninguna otra caché (GLOB-11).

## 7. Conclusiones

1. Las listas de adyacencia son la representación viable de una red de 8 803
   nodos: la matriz de adyacencia ocuparía cientos de megabytes.
2. La componente fuertemente conexa se obtiene en tiempo lineal en V + E y basta
   para que todo par de lugares tenga camino dirigido.
3. La cola de prioridad es decisiva en R2: la mediana del cociente frente a la
   versión lineal es 149,84 en la red completa (rango 5,99–189,60 según par).
4. QuickHull con enteros exactos reproduce los vértices de SciPy y mantiene la
   envolvente de la red en 14 vértices.
5. Held-Karp resuelve hasta k = 12 (fuerza bruta hasta k = 11), y la heurística
   voraz queda entre 0,009 % y 22,05 % por encima del óptimo según k (promedio 3,3 %–11,7 %).
6. La aplicación demuestra los resultados sin descargar ni re-medir: recalcula
   solo lo que el enunciado pide al momento y sus cifras coinciden con los
   archivos de resultados.

### 7.1 Comparación entre las dos máquinas

Todos los experimentos se midieron completos en la máquina A (Linux, AMD Ryzen 7
5800H) y en la máquina B (Windows 11, Intel Core i5-1135G7); ver la sección 1.3.
La comparación se genera desde los archivos con
`experimentos/comparar_maquinas.py` (`resultados/comparacion/`). Como las
máquinas difieren en procesador **y** sistema operativo, la comparación no
separa el efecto de cada uno; sirve para ver qué tanto cambian los tiempos
absolutos entre dos equipos reales y si las conclusiones del análisis se
mantienen.

Se compararon solo las mediciones con el mismo trabajo en ambas máquinas. En R2
se excluyen las 4 cuya entrada cambió con el catálogo corregido (T02 → F03 y las
filas de matriz de A13, F01 y F03). En R4 se conservan todas, porque fuerza
bruta, Held-Karp y el voraz hacen el mismo número de operaciones para un k dado,
sin importar los valores de la matriz.

**Razón Windows/Linux por requerimiento** (mediana en B ÷ mediana en A; mayor
que 1 significa que B fue más lenta):

| Requerimiento | Mediciones comparadas | Razón mediana | Rango       |
|---|---|---|-------------|
| R1 (componente) | 5 | 1,09 | 1,07 – 1,22 |
| R2 (Dijkstra y matriz) | 66 | 1,18 | 0,98 – 1,42 |
| R3 (envolvente) | 8 | 1,22 | 0,80 – 4,36 |
| R4 (exactos y voraz) | 55 | 1,06 | 0,97 – 1,53 |

**Mediciones representativas** (ms, mediana de 5):

| Medición | A (Linux) | B (Windows) | Razón |
|---|---|---|---|
| R1 · componente del departamento | 186,27 | 198,80 | 1,07 |
| R2 · C04 → C12, cola de prioridad | 6,40 | 7,80 | 1,22 |
| R2 · C04 → C12, versión lineal | 959,67 | 969,50 | 1,01 |
| R3 · red, versión propia | 9,72 | 11,72 | 1,21 |
| R3 · red, SciPy | 1,26 | 2,95 | 2,35 |
| R3 · cuadrado de 1 000 puntos, propia | 1,97 | 1,58 | 0,80 |
| R3 · cuadrado de 1 000 puntos, SciPy | 0,43 | 1,87 | 4,36 |
| R3 · cuadrado de 50 000 puntos, propia | 73,13 | 90,19 | 1,23 |
| R3 · cuadrado de 50 000 puntos, SciPy | 6,62 | 7,60 | 1,15 |
| R4 · fuerza bruta, k = 11 | 73 175 | 87 960 | 1,20 |
| R4 · Held-Karp, k = 12 | 33,79 | 40,21 | 1,19 |

**Lo que se mantiene igual en las dos máquinas.**

- Los resultados lógicos: V y E de las cinco redes de R1, los vértices de la
  envolvente en los cuatro conjuntos de R3 (14, 17, 22 y 34), los pares
  sorteados de R2, las instancias de R4 y el mayor k resuelto en el tope de
  5 minutos (11 con fuerza bruta y 12 con Held-Karp).
- El crecimiento con el tamaño de la entrada. Al pasar de k = 10 a k = 11, la
  fuerza bruta se multiplica por 11,3 en A y por 11,9 en B, cerca del factor 11
  que predice O(k!). Al pasar de k = 11 a k = 12, Held-Karp se multiplica por
  2,36 en A y por 2,47 en B, cerca del factor (12/11)²·2 ≈ 2,38 que predice
  O(k²·2^k). Cambiar de máquina cambia la constante, no la forma de la curva.
- El orden entre algoritmos: en ambas máquinas Dijkstra con cola es dos órdenes
  de magnitud más rápido que la versión lineal, y Held-Karp es miles de veces
  más rápido que la fuerza bruta desde k = 10.

**Lo que cambia, y por qué importa para el análisis.**

- **La máquina B es más lenta en general** (entre 6 % y 22 % según la mediana de
  cada requerimiento), lo esperable para un procesador de 4 núcleos frente a uno
  de 8. Cada medición usa un solo núcleo, así que pesan más la frecuencia, la
  caché y el sistema operativo que el número de núcleos.
- **La diferencia no es uniforme entre algoritmos.** La versión lineal de
  Dijkstra tarda casi lo mismo en ambas máquinas (razón 1,01), mientras que la
  versión con cola tarda 21 % más en B. Por eso el cociente lineal/cola baja de
  una mediana de 150× en A a 124× en B. Una explicación posible es que la
  versión con cola crea y descarta muchas tuplas en el montículo, y la gestión
  de memoria cuesta distinto en cada sistema. La conclusión práctica es que el
  cociente entre dos algoritmos **no es una constante del algoritmo**: depende
  de la máquina. La comparación asintótica (O(V²) frente a O((V + E) log V)) sí
  se mantiene.
- **SciPy tiene un costo fijo mayor en B.** En B, SciPy tarda entre 1,0 y 1,7 ms
  más que en A en todos los conjuntos, casi sin importar n. Ese costo fijo (la
  conversión a `double` y la preparación de Qhull) domina con pocos puntos: con
  1 000 puntos, la versión propia en Python **le gana a SciPy en B** (cociente
  0,85 frente a 4,59 en A). Con 50 000 puntos, el costo fijo se diluye y los
  cocientes vuelven a ser parecidos (11,9 en B y 11,0 en A). Es un ejemplo de
  por qué el análisis asintótico describe el comportamiento para n grande y no
  necesariamente para n pequeño, donde dominan las constantes.

**Portabilidad.** Medir en una segunda plataforma reveló cuatro supuestos de
Linux en el código, que se corrigieron sin cambiar ningún algoritmo:

1. El arnés obtenía la RAM con `os.sysconf`, que no existe en Windows.
2. La ficha de SciPy buscaba la extensión compilada como `.so` y usaba `ldd`; en
   Windows la extensión es `.pyd` y `ldd` no existe.
3. Python escribe los archivos de texto con saltos `\r\n` en Windows, así que
   cada JSON generado aparecía modificado por completo. Se resolvió con
   `.gitattributes` y escribiendo los JSON de R4 con `newline="\n"`, para que la
   huella del prerregistro del itinerario sea la misma en ambas plataformas.
4. El README solo traía comandos de Linux.

## 8. Anexo de uso de inteligencia artificial

El registro por tarea (herramienta y modelo, fecha, ID del plan, pedido, qué se
aceptó, rechazó o modificó y cómo se verificó) se mantiene en
[`docs/uso_ia.md`](uso_ia.md), conforme a REPO-07 y GLOB-25. Este anexo lo
redactan y firman personas; el agente no certifica el uso de IA.

Pendientes humanos restantes: ejecución del README en un entorno limpio (R5-13). Firmado R4-27 (David Posso, 2026-11-04), revisión y firma del documento (REPO-11) y registro del uso de IA de las tareas de cierre.
