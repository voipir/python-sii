"""
"""
from ..xml   import XMLNode
from ..types import SiiImpuesto, SiiMontoPorcentaje, SiiValor


class NodeOtrosImp(XMLNode):
    """ Otros Impuestos o Recargos """

    CodImp  = SiiImpuesto()         # Codigo del Impuesto o Recargo.
    TasaImp = SiiMontoPorcentaje()  # Tasa del Impuesto o Recargo.
    MntImp  = SiiValor()            # Monto del Impuesto o Recargo. En el LC Registrar Solo el Monto Con Derecho a Credito.
