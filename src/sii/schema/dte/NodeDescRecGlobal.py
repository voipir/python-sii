""" SII Global Discounts and Additional Charges Information """
from functools import partial

from ..xml   import XMLNode
from ..types import (UnsignedInteger, String, Enumeration,
                     SiiUnidadValor, SiiMonto14Digitos4Decimales, SiiMonto16Digitos2Decimales)


EnumIndExeDR = partial(
    Enumeration,
    1,  # Descuento/Recargo Global No Afecto
    2,  # Descuento/Recargo No Facturable
    optional=True
)


class NodeDescRecGlobal(XMLNode):
    """ Some Notes about Elements in this Structure:

    NroLinDR:       Numero Secuencial de Linea.
    TpoMov:         Tipo de Movimiento.
    GlosaDR:        Descripcion del Descuento o Recargo.
    TpoValor:       Unidad en que se Expresa el Valor.
    ValorDR:        Valor del Descuento o Recargo.
    ValorDROtrMnda: Valor en otra moneda.
    IndExeDR:       Indica si el D/R es No Afecto o No Facturable.
    """
    NroLinDR       = UnsignedInteger()
    TpoMov         = Enumeration('D', 'R')  # Descuento / Recargo
    GlosaDR        = String(optional=True, max_length=45)
    TpoValor       = SiiUnidadValor()
    ValorDR        = SiiMonto16Digitos2Decimales()
    ValorDROtrMnda = SiiMonto14Digitos4Decimales(optional=True)
    IndExeDR       = EnumIndExeDR()
