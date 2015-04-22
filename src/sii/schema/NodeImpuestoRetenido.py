""" SII Withheld Tax Information """
from .xml   import XMLNode
from .types import SiiMontoImpuestoAdicionalDTE, SiiMontoPorcentaje, SiiMontoImpuesto


class NodeImpuestoRetenido(XMLNode):
    """ Some Notes about Elements in this Structure:

    TipoImp:  Tipo de Impuesto o Retencion Adicional.
    TasaImp:  Tasa de Impuesto o Retencion.
    MontoImp: Monto del Impuesto o Retencion.
    """
    TipoImp  = SiiMontoImpuestoAdicionalDTE(optional=True)
    TasaImp  = SiiMontoPorcentaje(optional=True)
    MontoImp = SiiMontoImpuesto(optional=True)
