""" SII Document Items Information """
from .xml   import XMLNode, XMLNodeContainer
from .types import UnsignedInteger, StringType, SiiMonto16Digitos2Decimales


class NodeSubTotalInfo(XMLNode):
    """ Some Notes about Elements in this Structure:

    NroSTI:        Número de Subtotal.
    GlosaSTI:      Glosa.
    OrdenSTI:      Ubicación para Impresión.
    SubTotNetoSTI: Valor Neto del Subtotal.
    SubTotIVASTI:  Valor del IVA del Subtotal.
    SubTotAdicSTI: Valor de los Impuestos adicionales o específicos del Subtotal.
    SubTotExeSTI:  alor no Afecto o Exento del Subtotal.
    ValSubtotSTI:  Valor de la línea de subtotal.
    LineasDeta:    TABLA de Líneas de Detalle que se agrupan en el Subtotal.
    """
    NroSTI        = UnsignedInteger(max_value=99)
    GlosaSTI      = StringType(max_lenght=40)
    OrdenSTI      = UnsignedInteger(max_value=99)
    SubTotNetoSTI = SiiMonto16Digitos2Decimales(optional=True)
    SubTotIVASTI  = SiiMonto16Digitos2Decimales(optional=True)
    SubTotAdicSTI = SiiMonto16Digitos2Decimales(optional=True)
    SubTotExeSTI  = SiiMonto16Digitos2Decimales(optional=True)
    ValSubtotSTI  = SiiMonto16Digitos2Decimales(optional=True)
    LineasDeta    = XMLNodeContainer(UnsignedInteger, optional=True, max_ocurrs=60)
