""" SII Comissions Information """
from ..xml   import XMLNode
from ..types import SiiMonto


class NodeTotalComisiones(XMLNode):
    """ Some Notes about Elements in this Structure:

    ValComNeto: Valor Neto Comisiones y Otros Cargos
    ValComExe:  Val. Comis. y Otros Cargos no Afectos o Exentos
    ValComIVA:  Valor IVA Comisiones y Otros Cargos
    """
    ValComNeto = SiiMonto(optional=True)
    ValComExe  = SiiMonto(optional=True)
    ValComIVA  = SiiMonto(optional=True)
