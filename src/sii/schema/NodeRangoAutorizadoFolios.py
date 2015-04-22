""" SII Document Serial Number Range Information """
from .xml   import XMLNode
from .types import SiiFolio


class NodeRangoAutorizadoFolios(XMLNode):
    """ Rango Autorizado de Folios.

    D: Folio Inicial (Desde).
    H: Folio Final (Hasta).
    """
    D = SiiFolio()
    H = SiiFolio()
