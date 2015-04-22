""" SII Tributary Document Submission Node """
from .xml   import XMLNode, XMLNodeContainer
from .types import XMLSignatureSHA1withRSA

from .NodeSetDTE import NodeSetDTE


class NodeEnvioDTE(XMLNode):
    """
    """
    __attributes__ = {'version': "1.0"}

    SetDTE    = XMLNodeContainer(NodeSetDTE)
    Signature = XMLSignatureSHA1withRSA()
