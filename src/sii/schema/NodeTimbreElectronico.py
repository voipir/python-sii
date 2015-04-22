""" SII Document Signature (W3C-XML-SIG) """
from .xml   import XMLNode
from .types import String  # XMLSignatureSHA1withRSA

from .NodeTimbreDD import NodeTimbreDD


class NodeTimbreElectronico(XMLNode):
    """ Timbre Electronico de DTE.

    DD:   Datos Basicos de Documento.
    FRMT: Valor de Firma Digital sobre DD.
    """
    DD   = NodeTimbreDD()
    # FRMT = XMLSignatureSHA1withRSA()
    FRMT = String()
