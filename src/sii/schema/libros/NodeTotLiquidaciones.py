"""
"""
from ..xml   import XMLNode
from ..types import SiiValor


class NodeTotLiquidaciones(XMLNode):
    """ Info. Elect. de Venta (LV) """

    TotValComNeto = SiiValor()  # Valor Neto Comisiones y Otros Cargos (LV).
    TotValComExe  = SiiValor()  # Val. Comis. y Otros Cargos no Afectos o Exentos (LV).
    TotValComIVA  = SiiValor()  # Valor IVA Comisiones y Otros Cargos   (LV).
