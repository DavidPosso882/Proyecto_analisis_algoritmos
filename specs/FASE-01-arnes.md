# FASE-01 — Arnés de medición (UT-01)

**UT:** UT-01. **Fuente:** `PLAN.md §4 EXP-01..EXP-16, §2.1 UT-01, §6 DA-16, DA-17`.
**Objetivo:** un módulo de medición que todos los R usan. Se prueba con funciones de duración conocida, sin algoritmos reales.

## Entradas

- `specs/PLAN.md §4` completo + `§6` DA-16, DA-17.
- `specs/CONTRATOS.md §5` (esquema de resultados).
- `specs/FASE-00-fundacion.md` (manifiesto + lista GLOB-14).

## IDs que cubre

UT-01, EXP-01..EXP-16, GLOB-06..GLOB-10 (en lo que toca al arnés), DA-03, DA-04, DA-16, DA-17.

## Puerta de entrada

- [x] FASE-00 cerrada en mínimo (estructura REPO-01 + `manifiesto.txt` BORRADOR + `docs/uso_ia.md` init, 2026-10-27).
- [x] DA-16 firmada: recomendación del plan (ver Decisiones firmadas abajo). Firma: David Posso, 2026-10-27.
- [x] DA-17 firmada: semilla maestra 42; derivadas `42 + índice estable` (CONTRATOS.md, 2026-10-20).
- Sin arnés, no se mide R1.3, R2, R3.2 ni R4.1.

## Tareas

1. Implementar arnés en `src/<paquete>/medicion/`: mediana de 5 (EXP-03, sin descartar 1ª), 1 sola si >1 min (EXP-04), corte >5 min con `estado=no_completada` sin tiempo ni deducción (EXP-08, DA-04), solo-algoritmo en región (EXP-02), huella de entrada por algoritmo comparado (EXP-11), estado limpio por repetición sin cachés ni mutación (EXP-13), metadatos + 5 crudos (EXP-14), escritura incremental reanudable sin mezclar máquinas (EXP-16, EXP-01).
2. Unidad ms con único punto de conversión (EXP-05). Rechazar fusionar máquinas distintas (EXP-01).
3. Pruebas del arnés (todas con límites reducidos configurables; la constante real sigue 1 min / 5 min): mediana = 3er ordenado; >umbral = 1 medición; función lenta = `no_completada` terminada y sin tiempo; E/S fuera de región; huella coincide por algoritmo; entrada idéntica antes/después; interrumpir+reanudar = mismo determinista que ininterrumpido (EXP-15, EXP-16); dos semillas iguales = datos idénticos byte a byte (GLOB-07).
4. Verificación previa obligatoria: el ejecutor corre verificación y aborta si falla; probar aborto con doble con fallo deliberado (GLOB-06).
5. Tablas/gráficas solo desde CSV/JSON; borrar y regenerar = mismas cifras (GLOB-08). Esquema de columnas del Anexo (GLOB-09).

## Superficies permitidas

`src/<paquete>/medicion/`, `tests/medicion/`, `specs/FASE-01-arnes.md`, `experimentos/medicion/`, `resultados/medicion/`. No tocar `red/`, `caminos/`, `envolvente/`, `recorrido/`, `app/`, `data/`.

## Cómo lanzarlo en gentle shell

- `Spec: specs/FASE-01-arnes.md, S# = EXP-01..EXP-16 + DA-16 + DA-17`. Feature doc `odd/tasks/fase-01-arnes.md`. Un worker (superficie propia). Explorador solo-lectura opcional para temporizador/GC en versión instalada (no asumir).
- Alto riesgo «Protocolo de medición»: verificación independiente con funciones de duración conocida (mediana, 1-min, 5-min, exclusión E/S, huella). Ver `PLAN.md §2.2`.
- Cierre: arnés + pruebas en verde + `resultados/medicion/` demo con funciones sintéticas. Recién ahí R1/R2/R3/R4 pueden medir.

## Verificación de salida

- `grep -rn "perf_counter\|monotonic" src/<paquete>/medicion/` muestra un único punto de conversión.
- `grep -rn "cache\|lru_cache" src/<paquete>/medicion/` vacío (EXP-13).
- Constante límite real = 5 min (búsqueda estática, EXP-08).
