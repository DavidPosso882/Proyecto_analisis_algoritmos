# 00-INDICE — Cómo usar este plan con gentle shell

**Fuente de verdad congelada:** `specs/PLAN.md` (copia exacta de `../PLAN.md`, sha256 `6b09a9810979c47aefdd7ef9e2f628979fb030ab1ca4127aa0f622e4054523b5`, 2026-10-20).
No reescribas reglas. Toda fase cita IDs (`GLOB-xx`, `R#-xx`, `EXP-xx`, `REPO-xx`, `DA-xx`, `EV-xx`, `UT-xx`). Ante conflicto entre clase y enunciado, prevalece el enunciado (GLOB-27).

**Autoridades académicas (no se modifican):** `../Proyecto_final_2026-2.md`, `../Anexo_proyecto.md`, `../Analisis_de_Algoritmos_03-06.md`.
Prohibido modificarlas sin decisión humana registrada (GLOB-18).

## Orden de fases (una a la vez, con puerta humana entre cada una)

| Paso | Archivo de fase | UT | Bloquea hasta firmar |
|---|---|---|---|
| 0 | `FASE-00-fundacion.md` | UT-00 | DA-20, DA-23, DA-25 + manifiesto + CONTRATOS esquema |
| 1 | `FASE-01-arnes.md` | UT-01 | DA-16, DA-17 (mecánica y semilla) |
| 2 | `R1.md` | UT-02, UT-03, UT-04 | DA-06, DA-07, DA-08, DA-09, DA-10, DA-11 |
| 3 | `R2.md` | UT-05, UT-06 | DA-14 (+ DA-09, DA-15, DA-17 ya fijados) |
| 4 | `R3.md` | UT-07, UT-08 | DA-12, DA-18 |
| 5 | `R4.md` | UT-09, UT-10 | DA-13, DA-22 (+ GLOB-22 duraciones) |
| 6 | `R5.md` | UT-11, UT-12 | DA-24, DA-26 + README en limpio (R5-13) |

Flujo de datos: catálogo (UT-03) + red (UT-02) → grafo procesado (UT-04) → Dijkstra y matriz (UT-06) → R4 (UT-10) → app (UT-11). R3 usa nodos de UT-04. Toda medición usa el arnés UT-01.

## Cómo lanzar cada fase en gentle shell (obligatorio)

1. El orquestador crea el feature doc con el flujo propio de gentle shell (`odd/tasks/<fase>.md` + espejo en memoria). **No lo crees a mano** (REPO-05).
2. El feature doc copia **literalmente, sin resumir**, los «Fragmentos literales» que lista la fase, más el bloque del Anexo correspondiente (REPO-04 pasos 1-2).
3. El feature doc cita reglas **por ID, sin reescribirlas** (REPO-04 paso 3).
4. Toda delegación remite al localizador del feature doc + IDs + secciones originales; el worker lee el feature doc y los fragmentos antes de editar (REPO-04 pasos 4-5).
5. Ante ambigüedad, el worker devuelve una pregunta, no decide (REPO-04 paso 6). Los writers no modifican fragmentos literales (REPO-04 paso 7).
6. Handoff por referencia: `Spec: specs/<FASE>.md, T#, S#`. Nunca por paráfrasis. Al volver, el worker dice qué `S#` cubrió.
7. Superficies disjuntas por fase (REPO-10). `README.md`, `CONTRATOS.md`, manifiesto y `docs/` son compartidas: una unidad a la vez.
8. Prohibido YOLO para este proyecto (GLOB-19, REPO-06, DA-20). Sin commits ni push del agente sin autorización explícita por operación. Si un paso ODD exige commit/push, detenerse y pedir autorización.

## Permisos (resumen; el detalle manda en `PLAN.md §1`)

- Sin consultar: leer/listar/buscar + historial solo-lectura (GLOB-13).
- Solo con lista autorizada en el feature doc: suite de pruebas, scripts de verificación, análisis estático. Nada que descargue, borre o regenere datos (GLOB-14).
- Con consulta previa: red (GLOB-15), pip con versiones exactas (GLOB-16), borrar/regenerar `data/`/`resultados/` (GLOB-17).
- Crear/modificar solo dentro del alcance del plan; nunca enunciado, material de clase ni catálogo verificado sin decisión registrada (GLOB-18).
- Duda = pedir confirmación. Silencio no autoriza (GLOB-20).

## Puerta humana estándar (aplica a toda fase)

- Entrada: DAs bloqueantes de la fase firmadas (autor + fecha) en `specs/R#.md` o feature doc.
- Salida: diff revisado por persona + registro `docs/uso_ia.md` completo (REPO-07, GLOB-25) + ninguna tarea `[HUMANA]` marcada por el agente (GLOB-26).
- Textos del agente van marcados `BORRADOR` hasta firma humana (REPO-11).

## Qué darle al worker y qué no

- Dar: el archivo de fase + `specs/PLAN.md` secciones citadas + `CONTRATOS.md` + fragmentos literales del feature doc.
- No dar: el `PLAN.md` entero como único contexto, ni `odd/tasks/*.md` de otras fases, ni credenciales, ni permiso YOLO.
- Paralelo permitido solo tras congelar UT-00: UT-01, UT-05, UT-07, UT-09 con superficies disjuntas. UT-06, UT-08, UT-10 y UT-11 no son paralelizables entre sí (necesitan UT-01/UT-04 o resultados previos). Ver `PLAN.md §2.2`.
