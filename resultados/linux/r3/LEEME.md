# Resultados R3b — envolvente convexa: experimento y archivo para R5

Spec: `specs/R3.md` (UT-08: R3-07, R3-08, R3-10, R3-11). Feature:
`odd/tasks/r3b-experimento.md`. Todos los archivos se generan con los scripts de
`experimentos/r3/`; ninguno se edita a mano (GLOB-08).

## Archivos

| Archivo | Qué es | Requisito |
|---|---|---|
| `mediciones.csv` | mediciones crudas del arnés UT-01: 5 tiempos por fila, mediana, semilla, máquina, versiones, huella de entrada (EXP-03/06/11/14), reanudable (EXP-16) | R3-07 |
| `entradas_r3.json` | testigo de cada conjunto: `n` tras dedup, `generados` antes, semilla, lado del cuadrado, bbox UTM, huella de la entrada y vértices | R3-07, R3-16 |
| `tabla_anexo_r3.csv` | tabla del Anexo con las columnas exigidas + `generados`: filas «Nodos de la red», «Cuadrado, 1 000 puntos», «Cuadrado, 10 000 puntos», «Cuadrado, 50 000 puntos» | R3-08 |
| `tabla_anexo_r3.md` | la misma tabla renderizada desde el CSV, para el documento técnico | R3-08 |
| `scipy_info_r3.json` / `.md` | qué algoritmo, lenguaje y versión usa SciPy, con las fuentes leídas en la instalación | R3-10 |
| `vertices_red.csv` | vértices de la envolvente de la red: enteros UTM + lon/lat + `nodo_id`; **R5 lo lee sin recalcular** | R3-11 |

## Convenciones (DA-17, DA-18, DA-10)

- Coordenadas de la red en UTM 18N (EPSG:32618), redondeo **half-up**
  (`quindio.envolvente.quickhull.redondear_half_up`) y deduplicación.
- `n` de la tabla = puntos **tras** deduplicar; `generados` = antes.
- Cuadrados: puntos **enteros** uniformes, semilla derivada `42 + (500 + i)` →
  542, 543, 544; lado = mayor dimensión del bbox UTM (56 536 m), anclado en
  `(xmin, ymin) = (401796, 464304)`.
- Tiempos en **ms**: mediana de 5 repeticiones del arnés UT-01 (EXP-03); solo
  se mide la envolvente (EXP-02); la conversión, el redondeo, la deduplicación
  y el formato de entrada quedan fuera de la región medida (R3-07).
- `Cociente` = tiempo propio ÷ tiempo SciPy (DA-18), calculado con los dos
  valores mostrados (3 decimales), por lo que se recalcula de la tabla.

## Cómo lo lee R5

`resultados/r3/vertices_red.csv` tiene una fila por vértice (14, igual a la
fila «Nodos de la red» de `tabla_anexo_r3.csv`):

```
orden,x_utm,y_utm,lon,lat,nodo_id
```

`lon`/`lat` (EPSG:4326, 7 decimales) sirven directo para dibujar el polígono en
el mapa; `nodo_id` permite rastrear el nodo de la componente que originó cada
vértice. No hace falta recalcular la envolvente.

## Regenerar

```
.venv/bin/python experimentos/r3/scipy_info_r3.py
.venv/bin/python experimentos/r3/medir_r3.py     # reanudable: omite lo ya medido
.venv/bin/python experimentos/r3/tablas_r3.py
```
