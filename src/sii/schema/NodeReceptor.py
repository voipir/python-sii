""" SII Document Receiver """
from .xml   import XMLNode
from .types import String, SiiRUT, SiiRazonSocialLarga, SiiMail, SiiComuna, SiiCiudad

from .NodeExtranjero import NodeExtranjero


class NodeReceptor(XMLNode):
    """ Some Notes about Elements in this Structure:

    CdgIntRecep: Codigo Interno del Receptor
    """
    # Required Elements
    RUTRecep    = SiiRUT()
    RznSocRecep = SiiRazonSocialLarga()

    # Optional Elements
    CdgIntRecep  = String(optional=True, max_length=20)
    GiroRecep    = String(optional=True, max_length=40)
    Contacto     = String(optional=True, max_length=80)
    CorreoRecep  = SiiMail(optional=True)
    DirRecep     = String(optional=True, max_length=70)
    CmnaRecep    = SiiComuna(optional=True)
    CiudadRecep  = SiiCiudad(optional=True)
    DirPostal    = String(optional=True, max_length=70)
    CmnaPostal   = SiiComuna(optional=True)
    CiudadPostal = SiiCiudad(optional=True)

    # Nodes
    Extranjero = NodeExtranjero(optional=True)
