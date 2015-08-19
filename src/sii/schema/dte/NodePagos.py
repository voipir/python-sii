""" SII Payment Node """
from ..xml   import XMLNode
from ..types import String, SiiFecha, SiiMonto


class NodePagos(XMLNode):
    """ Represents a single Payment (eventually amongst many) on this Document.

    FchPago:    Fecha de Pago (AAAA-MM-DD).
    MntPago:    Monto de Pago.
    GlosaPagos: Glosa.
    """

    FchPago    = SiiFecha()
    MntPago    = SiiMonto()
    GlosaPagos = String(max_length=40, optional=True)
