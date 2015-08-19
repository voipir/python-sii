"""
"""
from ..xml   import XMLNode
from ..types import SiiImpuesto, SiiValor


class NodeTotOtrosImp(XMLNode):
    """ Totales de Otros Impuestos """

    CodImp     = SiiImpuesto()  # Codigo del Otro Impuesto
    TotMntImp  = SiiValor()     # Monto Total del Otro Impuesto
