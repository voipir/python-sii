"""
"""
from ..xml   import XMLNode
from ..types import SiiRUT, SiiValor


class NodeLiquidaciones(XMLNode):
    """ Info. Elect. de Venta (LV) """

    RutEmisor  = SiiRUT()    # Rut Emisor (LV)
    ValComNeto = SiiValor()  # Valor Neto Comisiones y Otros Cargos (LV)
    ValComExe  = SiiValor()  # Val. Comis. y Otros Cargos no Afectos o Exentos (LV)
    ValComIVA  = SiiValor()  # Valor IVA Comisiones y Otros Cargos (LV)
