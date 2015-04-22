""" SII Provided Public Key (RSA) """
from .xml   import XMLNode
from .types import Base64Binary


class NodePubKey(XMLNode):
    """ RSA Public Key

    M: RSA Modulo.
    E: RSA Exponent.
    """
    M = Base64Binary()
    E = Base64Binary()
