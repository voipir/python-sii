""" SII Foreigener Information """
from ..xml   import XMLNode
from ..types import String


class NodeExtranjero(XMLNode):

    NumId        = String(optional=True, min_length=1, max_length=20)
    Nacionalidad = String(optional=True, min_length=1, max_length=3)
