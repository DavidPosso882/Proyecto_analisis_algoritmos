# Comparación de tiempos: máquina B (Windows) frente a máquina A (Linux)

- Máquina A: Linux 7.2.11-200.fc44.x86_64, Python 3.14.8, 15372 MB
- Máquina B: Windows 11, Python 3.14.0, 16149 MB

Razón = mediana en Windows ÷ mediana en Linux (mayor que 1: Windows más lento).

| Requerimiento | Mediciones comparables | Excluidas | Razón mediana | Mínima | Máxima |
|---|---|---|---|---|---|
| R1 | 5 | 0 | 1.09 | 1.07 | 1.22 |
| R2 | 66 | 4 | 1.18 | 0.98 | 1.42 |
| R3 | 8 | 0 | 1.22 | 0.80 | 4.36 |
| R4 | 55 | 1 | 1.06 | 0.97 | 1.53 |

## Resultados lógicos (no dependen de la máquina)

- Linux fuerza_bruta mayor k completado = 11
- Linux held_karp mayor k completado = 12
- Windows fuerza_bruta mayor k completado = 11
- Windows held_karp mayor k completado = 12
- V y E de R1 y vértices de R3: idénticos en ambas máquinas

Generado por `experimentos/comparar_maquinas.py` desde `resultados/linux/` y `resultados/r1`–`r4`.
