"""
"""
from ..xml   import XMLNode
from ..types import String


class NodeExtranjero(XMLNode):
    """ Receptor Extranjero (LV) """

    NumId        = String(min_length=1, max_length=20)  # Num. Identif. Receptor Extranjero (LV).
    Nacionalidad = String(min_length=1, max_length=3)   # Nacionalidad Recptor Extranjero (LV).
