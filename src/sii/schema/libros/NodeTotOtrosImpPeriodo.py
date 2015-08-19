"""
"""
from ..xml   import XMLNode
from ..types import SiiImpuesto, SiiMontoPorcentaje, SiiValor, SiiMonto


class NodeTotOtrosImpPeriodo(XMLNode):
    """ Totales de Otros Impuestos """

    CodImp     = SiiImpuesto()         # Codigo del Otro Impuesto
    TotMntImp  = SiiValor()            # Monto Total del Otro Impuesto

    FctImpAdic = SiiMontoPorcentaje()  # Factor Impuesto Adicional (LC)
    TotCredImp = SiiMonto()            # Total Credito Impuesto (LC)
