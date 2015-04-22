""" SII Discount Information """
from .xml   import XMLNode
from .types import SiiUnidadValor, SiiMonto16Digitos2Decimales


class NodeSubDescuento(XMLNode):
    """ Some Notes about Elements in this Structure:

    TipoDscto:  Tipo de SubDescuento
    ValorDscto: Valor del SubDescuento
    """
    TipoDscto  = SiiUnidadValor()
    ValorDscto = SiiMonto16Digitos2Decimales()
