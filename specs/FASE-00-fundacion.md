# FASE-00 — Fundación y gates (UT-00)

**UT:** UT-00. **Fuente:** `PLAN.md §2.1, §5 REPO-01..REPO-10, §1 GLOB-13..GLOB-20, §6 DA-20, DA-23, DA-25`.
**Objetivo:** dejar contratos, estructura, manifiesto y permisos congelados antes de cualquier writer paralelo.

## Entradas (leer antes de tocar nada)

- `specs/PLAN.md §1` (GLOB-13..20), `§5` completo, `§6` DA-20, DA-23, DA-25.
- `specs/00-INDICE.md` (orden y puertas).
- `../Proyecto_final_2026-2.md §3, §7` + `../Anexo_proyecto.md` introducción (nombres exactos de columnas).

## IDs que cubre

UT-00, REPO-01..REPO-10, GLOB-13..GLOB-20, DA-01, DA-02, DA-05, DA-20, DA-23, DA-25. Toca CONTRATOS esquema (no datos).

## Puerta de entrada (humana, bloquea todo lo demás)

- [x] DA-25 firmada: TDD sí/no, ejecutor (propuesto pytest), SDD/OpenSpec no (solo ODD + `specs/`), modo de permisos declarado en el feature doc.
- [x] DA-23 firmada: comandos exactos autorizados de pruebas/verificación/análisis + sí/no a web de docs y teselas R5.
- [x] DA-20 firmada: sin YOLO; commits por persona tras revisar diff, con coautoría IA; cada commit/push con autorización por separado. Consultar al docente si coautoría afecta nota.
- Sin estas 3 firmas, no se implementa nada (PLAN.md §2.2, §3 R1-R5 «Insumos ODD»).

## Tareas (una unidad, sin paralelo)

1. Crear estructura `REPO-01` (ver árbol en PLAN.md §5). Solo `specs/` existe hoy; crear resto vacío con `.gitkeep` si hace falta. `verificacion/` separado de módulos evaluables.
2. Congelar `specs/CONTRATOS.md`: quitar `BORRADOR` solo cuando DA-10, DA-15, DA-17, DA-18 tengan valor. Hasta entonces queda `BORRADOR` + `PENDIENTE-DA`.
3. Crear manifiesto único (REPO-08, propuesto): un archivo con paquete==versión exacta + requerimiento que lo usa. Sin instalar nada aún (GLOB-16 exige consulta con lista exacta).
4. Crear `specs/R1.md..R5.md` vacíos de estructura (encabezado + lista de IDs + «Fragmentos literales» pendientes) para cumplir REPO-02 antes del primer cambio de código de cada R. Este repo ya los crea en los siguientes archivos de fase; no duplicar.
5. Fijar en el feature doc la lista autorizada GLOB-14 (comandos exactos) y el modo de permisos. Registrar todo acceso a red/pip/borrado posterior contra esa lista.
6. Inicializar `docs/uso_ia.md` según REPO-07 (una entrada por tarea: fecha, herramienta/modelo, ID plan, pedido, aceptado/rechazado, verificación).

## Superficies permitidas

`specs/CONTRATOS.md`, `specs/R#.md` (encabezados), manifiesto, `README.md` (solo estructura), `docs/uso_ia.md` (init), árbol de dirs. Prohibido tocar `data/`, `src/`, enunciado, material de clase.

## Cómo lanzarlo en gentle shell

- `Spec: specs/FASE-00-fundacion.md`. Orquestador crea `odd/tasks/fase-00-fundacion.md` con `## Specs` (S# = DA-20, DA-23, DA-25 textuales + REPO-01 árbol) y `## Tasks` = las 6 de arriba. Un solo worker inline (no paralelo: es superficie compartida).
- Cierre: `CONTRATOS.md` con esquema + manifiesto + lista GLOB-14 + 3 DAs firmadas. Recién ahí se habilita FASE-01 y writers paralelos futuros.

## Verificación de salida

- Árbol concuerda con REPO-01 o desviación registrada.
- Todo import futuro podrá chequearse contra manifiesto (REPO-08).
- `docs/uso_ia.md` existe y cada tarea tiene entrada (GLOB-25).
- Cero commits/push del agente sin autorización registrada (GLOB-19).

## Decisiones firmadas

| DA | Decisión | Autor | Fecha |
|---|---|---|---|
| DA-25 | ODD solo, sin SDD/OpenSpec. TDD sí para R2, R3, R4. Ejecutor: pytest. | David Posso | 2026-10-20 |
| DA-23 | Autorizados: `pytest`, `python -m pytest`, `ruff check`. Web de docs solo lectura sí. Teselas R5 en local sí. Red/pip/borrado fuera de esto, por consulta. | David Posso | 2026-10-20 |
| DA-20 | Sin YOLO. Commits los hace la persona tras revisar diff, con línea de coautoría IA. Cada commit/push con autorización aparte. | David Posso | 2026-10-20 |
