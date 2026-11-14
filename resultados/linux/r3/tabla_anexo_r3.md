| Conjunto de puntos | n | Vértices de la envolvente | Tiempo propio (ms) | Tiempo SciPy (ms) | Cociente | generados |
|---|---|---|---|---|---|---|
| Nodos de la red | 8803 | 14 | 9.719 | 1.258 | 7.73 | 8803 |
| Cuadrado, 1 000 puntos | 1000 | 17 | 1.975 | 0.430 | 4.59 | 1000 |
| Cuadrado, 10 000 puntos | 10000 | 22 | 13.760 | 1.466 | 9.39 | 10000 |
| Cuadrado, 50 000 puntos | 50000 | 34 | 73.127 | 6.622 | 11.04 | 50000 |

Tiempos en milisegundos (ms): mediana de 5 repeticiones (EXP-03). `n` = puntos tras deduplicar; `generados` = puntos antes de deduplicar (DA-18). Cociente = tiempo propio ÷ tiempo SciPy (DA-18), recalculable desde las dos columnas de tiempo. Vértices: idénticos entre la versión propia y SciPy en las cuatro filas (R3-08).
