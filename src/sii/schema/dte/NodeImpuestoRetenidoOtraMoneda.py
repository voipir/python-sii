""" SII Withheld Tax on Foreign Currency Information """
from ..xml   import XMLNode
from ..types import SiiMontoImpuestoAdicionalDTE, SiiMontoPorcentaje, SiiMonto14Digitos4Decimales


class NodeImpuestoRetenidoOtraMoneda(XMLNode):
    """ Some Notes about Elements in this Structure:

    TipoImpOtrMnda: Tipo de Impuesto o Retencion Adicional.
    TasaImpOtrMnda: Tasa de Impuesto o Retencion.
    VlrImpOtrMnda:  Valor del impuesto o retención en otra moneda.
    """
    TipoImpOtrMnda = SiiMontoImpuestoAdicionalDTE()
    TasaImpOtrMnda = SiiMontoPorcentaje(optional=True)
    VlrImpOtrMnda  = SiiMonto14Digitos4Decimales()
