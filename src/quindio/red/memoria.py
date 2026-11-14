"""Estimación de memoria matriz vs listas (R1-02).

Supuestos escritos (no a mano: V y E vienen del metadato):
- matriz: V² celdas × bytes_por_celda (default 8, float64).
- listas: V cabeceras × bytes_por_nodo (default 8, referencia) + E entradas
  × bytes_por_entrada (default 24: vecino + peso + overhead).
- multigrafo: E cuenta paralelas y lazos; simple: E_simple dado aparte.
- megabyte = 1024² bytes (convención declarada).
"""
MB = 1024 * 1024


def estimar_mb(nodos, aristas, bytes_por_celda=8, bytes_por_nodo=8,
               bytes_por_entrada=24):
    """Puro y testeable con V/E pequeños (R1-02)."""
    matriz_mb = nodos * nodos * bytes_por_celda / MB
    listas_mb = (nodos * bytes_por_nodo + aristas * bytes_por_entrada) / MB
    return {"matriz_mb": matriz_mb, "listas_mb": listas_mb}
