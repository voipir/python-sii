""" SII Additional Charges after Tax ? Information """
from .xml   import XMLNode
from .types import SiiUnidadValor, SiiMonto16Digitos2Decimales


class NodeSubRecargo(XMLNode):
    """ Some Notes about Elements in this Structure:

    TipoRecargo:  Tipo de SubRecargo.
    ValorRecargo: Valor de SubRecargo.
    """
    TipoRecargo  = SiiUnidadValor()
    ValorRecargo = SiiMonto16Digitos2Decimales()
