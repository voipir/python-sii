""" SII Transport Information """
from ..xml   import XMLNode
from ..types import String, SiiRUT, SiiComuna, SiiCiudad

from .NodeChofer import NodeChofer
from .NodeAduana import NodeAduana


class NodeTransporte(XMLNode):
    """ Some Notes about Elements in this Structure:
    """
    Patente    = String(optional=True, max_length=8)
    RUTTrans   = SiiRUT(optional=True)
    Chofer     = NodeChofer(optional=True)
    DirDest    = String(optional=True, max_length=70)
    CmnaDest   = SiiComuna(optional=True)
    CiudadDest = SiiCiudad(optional=True)
    Aduana     = NodeAduana(optional=True)
