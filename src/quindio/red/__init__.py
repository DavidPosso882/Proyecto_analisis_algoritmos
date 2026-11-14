"""Exporta el modelo de red (R1)."""
from .componente import componente_mas_grande  # noqa: F401
from .descarga import (  # noqa: F401
    CENTRO_ARMENIA,
    ETIQUETA_DEPTO,
    ETIQUETAS_RADIO,
    construir_metadato,
    descargar_todo,
    guardar_crudo,
    parametros_descarga,
    validar_metadato,
)
from .memoria import estimar_mb  # noqa: F401
from .pesos import aplicar_pesos, tiempo_viaje_s, verificar_pesos  # noqa: F401
