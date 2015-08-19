""" SII Document Serial Number Authorizations Information """
from ..xml   import XMLNode
from ..types import String, UnsignedInteger, SiiRUT, SiiFecha, SiiDTE

from .NodeRangoAutorizadoFolios import NodeRangoAutorizadoFolios
from .NodePubKey                import NodePubKey


class NodeDatosAutFolio(XMLNode):
    """

    RE:    RUT Emisor.
    RS:    Razon Social Emisor.
    TD:    Tipo DTE.
    RNG:   Rango Autorizado de Folios.
    FA:    Fecha Autorizacion en Formato AAAA-MM-DD.
    RSAPK: Clave Publica RSA del Solicitante.
    IDK:   Identificador de Llave.
    """
    RE    = SiiRUT()
    RS    = String(min_length=1, max_length=40)
    TD    = SiiDTE()
    RNG   = NodeRangoAutorizadoFolios()
    FA    = SiiFecha()
    RSAPK = NodePubKey()
    IDK   = UnsignedInteger()

    # DSAPK =  # They also give the choice of a DSA based PK (disastrous :S)
