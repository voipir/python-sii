""" SII Tributary Document Node """
from .xml import XMLNode, XMLNodeContainer

from .NodeCaratula import NodeCaratula
from .NodeDTE      import NodeDTE


class NodeSetDTE(XMLNode):
    """
    Informacion Tributaria dentro de un Envío (child del envio en sí)
    """
    __attributes__ = {'ID': "SetDoc"}

    Caratula = NodeCaratula()
    DTE      = XMLNodeContainer(NodeDTE, attributes={'version': "1.0"})
