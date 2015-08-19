""" SII Transport Driver Information """
from ..xml   import XMLNode
from ..types import String, SiiRUT


class NodeChofer(XMLNode):

    RUTChofer    = SiiRUT()
    NombreChofer = String(max_length=30)
