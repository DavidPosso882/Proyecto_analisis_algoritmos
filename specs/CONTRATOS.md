# CONTRATOS.md — Esquemas compartidos (CONGELADO 2026-10-20)

> Estado: `CONGELADO`. Base fija para writers paralelos. Cambios solo por decisión registrada.
> Fuente: `PLAN.md §2.1 UT-00`, `REPO-02`, `REPO-10`. No inventar campos exigidos por el Anexo.

## Reglas

- Nombres de columna, filas y estructura del Anexo se respetan; columnas pueden ampliarse, no reducirse (GLOB-09).
- Tiempos en ms en una sola unidad (EXP-05, EV-20). Semilla efectiva + máquina + versiones en cada archivo de resultados (EXP-06, EXP-14).
- Tolerancia numérica (DA-15) y EPSG (DA-10) fijados abajo. Sin `PENDIENTE-DA`.
- Cada `R#.md` lista los IDs que cubre y un caso de prueba por criterio (REPO-02).

## Esquemas a congelar en UT-00

### 1. Catálogo (`data/catalogo/`) — requiere DA-06

Campos mínimos propuestos (grupo firma): `id, nombre, municipio, categoria, latitud, longitud, duracion_min (solo atractivos), justificacion_duracion, verificada, verificada_por, fecha_verificacion`.
Mínimos: al menos 40 lugares (EV-01); 12 cabeceras, 15 atractivos, 8 fincas/hoteles rurales, 5 acopios/trilladoras (EV-02). Coordenadas se verifican en mapa por persona (GLOB-21). Duraciones con fuente o criterio del grupo (GLOB-22).

### 2. Grafo procesado (UT-04, R1-08, R1-09)

`data/procesado/`: componente + pesos (`distancia_m`, `tiempo_viaje_s`) + asociaciones lugar→nodo (`nodo_id, distancia_m`) + índices contiguos + metadato (V/E antes/después, fecha descarga, versiones OSMnx/NetworkX/Python, parámetros, origen). Carga sin descargar (R1-08). Módulos R2-R4 no importan OSMnx ni NetworkX (R1-09, GLOB-03).

### 3. Asociaciones (R1-06, R1-07)

Vecino más cercano euclidiano en UTM 18N, mismo CRS (DA-10), desempate por menor id de nodo, sin árbol espacial. Reporte `> 500 m` estricto (EV-04, DA-11). Sin eliminar lugares sin decisión registrada.

### 4. Matriz R2 (R2-11)

CSV con primera fila y primera columna = ids de lugares en el mismo orden; celda (i,j) = segundos de i a j, dirigida, sin simetrizar; diagonal cero; al menos 40×40 (EV-09). Columnas de mediciones: `origen, destino, version, tiempo_viaje_s, nodos_explorados, tiempo_ms` con `version ∈ {lineal, cola_prioridad}` (EV-25). Columna adicional `estado` para `no_completada` (R2-12).

### 5. Resultados de medición (EXP-14)

Por fila: medición + 5 tiempos crudos + mediana + semilla efectiva + máquina (CPU/RAM/SO/Python) + versiones + fecha + huella de entrada (EXP-11) + método de verificación (EXP-07). Misma máquina por requerimiento (EXP-01). Solo algoritmo en región medida (EXP-02).

### 6. Envolvente R3 (R3-11)

Archivo de vértices (enteros UTM + posición para mapa) con conteo igual a fila «Nodos de la red» de R3-08. Tabla con columnas del Anexo: `Conjunto, n, Vertices, Tiempo propio (ms), Tiempo SciPy (ms), Cociente` (R3-08). `n` = tras deduplicar (R3-07).

### 7. Recorrido R4 (R4-07, R4-11, R4-12)

Instancias guardadas (k lugares sin Armenia, sin repetir, semilla derivada, DA-17). Curva k=5..12 con corte en primer `no_completada` (R4-07, R4-08). Calidad k=5,8,10,12 con ≥5 instancias: `brecha = (heuristica − heldkarp) / heldkarp × 100`, promedio y máximo (R4-11, DA-18). Itinerario con columnas `Orden, Lugar, Desplazamiento (min), Visita (min), Acumulado (h)` + fila Regreso + 3 totales (R4-12). Cálculo interno en segundos (R4-13).

## Pendientes de congelar (ver FASE-00)

- [x] DA-10: WGS84 / UTM 18N, EPSG:32618. Firma: David Posso, 2026-10-20.
- [x] DA-15: igualdad exacta entre propios (Dijkstra×2, bruta vs HK); tolerancia relativa 1e-9 vs libs. Firma: David Posso, 2026-10-20.
- [x] DA-17: semilla maestra 42; derivadas `42 + índice estable`; 1 instancia por k para curva, reutilizada como instancia 1 de R4.3. Firma: David Posso, 2026-10-20.
- [x] DA-18: redondeo documentado de la función usada; degenerados a extremos distintos; lado = mayor dimensión bbox UTM; puntos uniformes enteros; `n` tras dedup + columna generados; Cociente = propio/SciPy; brecha = (H-HK)/HK×100 prom+máx. Firma: David Posso, 2026-10-20.
- [ ] Manifiesto único con versiones exactas (REPO-08).
