""" SII Codigo Autorizacion de Folio Node """
from .xml   import XMLNode
from .types import XMLSignatureSHA1withRSA

from .NodeDatosAutFolio import NodeDatosAutFolio


class NodeCodigoAutFolio(XMLNode):
    """ Codigo Autorizacion Folios.

    DA:   Datos de Autorizacion de Folios.
    FRMA: Firma Digital (RSA) del SII Sobre DA.
    """
    DA   = NodeDatosAutFolio()
    FRMA = XMLSignatureSHA1withRSA()
