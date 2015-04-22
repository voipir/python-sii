""" SII Item Code Information """
from .xml   import XMLNode
from .types import String


class NodeCdgItem(XMLNode):
    """ Some Notes about Elements in this Structure:

    TpoCodigo: Tipo de Codificacion (?)
    VlrCodigo: Valor del Codigo de Item, para la Codificacion Particular.
    """
    TpoCodigo = String(max_length=10)
    VlrCodigo = String(max_length=35)
