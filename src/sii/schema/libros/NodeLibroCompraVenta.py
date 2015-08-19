"""
"""
from ..xml   import XMLNode
from ..types import String

from .NodeEnvioLibro import NodeEnvioLibro


class NodeLibroCompraVenta(XMLNode):
    """ Informacion Electronica de Libros de Compra y Venta """

    EnvioLibro = NodeEnvioLibro()
    Signature  = String()
