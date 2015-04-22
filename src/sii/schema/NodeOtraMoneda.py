""" SII Foreign Currency Information """
from .xml   import XMLNode, XMLNodeContainer
from .types import SiiTipoMoneda, SiiMonto6Digitos4Decimales, SiiMonto14Digitos4Decimales

from .NodeImpuestoRetenidoOtraMoneda import NodeImpuestoRetenidoOtraMoneda


class NodeOtraMoneda(XMLNode):
    """ Some Notes about Elements in this Structure:

    TpoMoneda:          Tipo Ottra moneda Tabla de Monedas  de Aduanas.
    TpoCambio:          Tipo de Cambio fijado por el Banco Central de Chile.
    MntNetoOtrMnda:     Monto Neto del DTE en Otra Moneda.
    MntExeOtrMnda:      Monto Exento del DTE en Otra Moneda .
    MntFaeCarneOtrMnda: Monto Base Faenamiento Carne en Otra Moneda.
    MntMargComOtrMnda:  Monto Base de Márgenes de Comercialización. Monto informado.
    IVAOtrMnda:         Monto de IVA del DTE en Otra Moneda.
    ImpRetOtrMnda:      Impuestos y Retenciones Adicionales.
    IVANoRetOtrMnda:    IVA no retenido Otra Moneda.
    MntTotOtrMnda:      Monto Total Otra Moneda.
    """
    TpoMoneda          = SiiTipoMoneda()
    TpoCambio          = SiiMonto6Digitos4Decimales(optional=True)
    MntNetoOtrMnda     = SiiMonto14Digitos4Decimales(optional=True)
    MntExeOtrMnda      = SiiMonto14Digitos4Decimales(optional=True)
    MntFaeCarneOtrMnda = SiiMonto14Digitos4Decimales(optional=True)
    MntMargComOtrMnda  = SiiMonto14Digitos4Decimales(optional=True)
    IVAOtrMnda         = SiiMonto14Digitos4Decimales(optional=True)
    ImpRetOtrMnda      = XMLNodeContainer(NodeImpuestoRetenidoOtraMoneda, min_occurs=0,
                                                                          max_occurs=20)
    IVANoRetOtrMnda    = SiiMonto14Digitos4Decimales(optional=True)
    MntTotOtrMnda      = SiiMonto14Digitos4Decimales()
