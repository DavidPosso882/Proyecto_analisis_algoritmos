# Prueba en Windows (2026-11-14)

- Máquina: Windows 11 Home Single Language (compilación 26200), Intel Core i5-1135G7 (4 núcleos / 8 hilos), 16 GB de RAM, Python 3.14.0.
- Responsable: Juan Diego García.
- Rama: `correcciones-Diego`.

## Automática

- `ruff check src tests experimentos verificacion`: sin errores.
- `pytest -q`: 100 pruebas pasan.
- `verificacion/`: los 6 scripts pasan (R1-01/R1-04, R1-06/R1-12, R2-06, R2-11, R3-13, R4-06).

## Manual de la aplicación

| # | Caso | Resultado |
|---|---|---|
| 1 | Inicio: 40 lugares, 15 atractivos, 14 vértices | OK |
| 2 | Ruta T02 → F03: 22,95 min | OK |
| 3 | Ruta C01 → A13: 45,9 min | OK |
| 4 | Ruta A03 → A12: 0,00 min (limitación documentada) | OK |
| 5 | Ruta C01 → C01: 0 min sin error | OK |
| 6 | Envolvente: 14 vértices | OK |
| 7 | Itinerario C01 + A14, A04, A10, A05, A07, A08: recorrido de R4.4 | OK |
| 8 | Itinerario con 5 y con 9 atractivos: mensaje de error | OK |
| 9 | Itinerario con partida F06 | OK |
| 10 | Resultados: cifras de Windows y gráficas | OK |