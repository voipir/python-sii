""" SII Price in Foreign Currency Information

TODO: make the currency a enumeration field to further constrain data integrity.
"""
from ..xml   import XMLNode
from ..types import (String,
                    SiiMonto6Digitos4Decimales,
                    SiiMonto12Digitos6Decimales,
                    SiiMonto14Digitos4Decimales)


class NodePrecioOtraMoneda(XMLNode):
    """ Some Notes about Elements in this Structure:

    PrcOtrMon:        Precio Unitario en Otra Moneda.
    Moneda:           Codigo de Otra Moneda (Usar Codigos de Moneda del Banco Central).
    FctConv:          Factor para Conversion a Pesos.
    DctoOtrMnda:      Descuento en Otra Moneda.
    RecargoOtrMnda:   Recargo en Otra Moneda.
    MontoItemOtrMnda: Valor por línea de detalle en Otra Moneda.
    """
    PrcOtrMon        = SiiMonto12Digitos6Decimales()
    Moneda           = String(max_length=3)
    FctConv          = SiiMonto6Digitos4Decimales(optional=True)
    DctoOtrMnda      = SiiMonto14Digitos4Decimales(optional=True)
    RecargoOtrMnda   = SiiMonto14Digitos4Decimales(optional=True)
    MontoItemOtrMnda = SiiMonto14Digitos4Decimales(optional=True)
