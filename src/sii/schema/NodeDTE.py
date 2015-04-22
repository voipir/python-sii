""" SII Tributary Document and Signature Pair Node """
from .xml   import XMLNode
from .types import String

# from .NodeDocumento import NodeDocumento


class NodeDTE(XMLNode):
    """
    Documento Tributario Electronico con su respectiva Firma Digital
    """
    Documento = None      # Placeholder for NodeDocumento
    Signature = String()  # Here we have to insert the XMLSec Signature Template Nodes
