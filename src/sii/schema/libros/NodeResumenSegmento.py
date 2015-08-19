"""
"""
from ..xml import XMLNode, XMLNodeContainer

from .NodeTotalesSegmento import NodeTotalesSegmento


class NodeResumenSegmento(XMLNode):
    """ Resumen del Segmento de Informacion Enviado """

    TotalesSegmento = XMLNodeContainer(NodeTotalesSegmento, max_occurs=40)
