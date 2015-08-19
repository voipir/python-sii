"""
"""
import datetime

from ..xml   import XMLNode, XMLNodeContainer
from ..types import SiiFechaHora

from .NodeCaratula        import NodeCaratula
from .NodeResumenSegmento import NodeResumenSegmento
from .NodeResumenPeriodo  import NodeResumenPeriodo
from .NodeDetalle         import NodeDetalle


class NodeEnvioLibro(XMLNode):
    """ Identificacion, Resumen y Detalles del Libro Electronico """

    Caratula        = NodeCaratula()
    ResumenSegmento = XMLNodeContainer(NodeResumenSegmento, min_occurs=0, max_ocurrs=40)
    ResumenPeriodo  = XMLNodeContainer(NodeResumenPeriodo,  min_occurs=0, max_ocurrs=40)
    Detalle         = XMLNodeContainer(NodeDetalle,         min_occurs=0)
    TmstFirma       = SiiFechaHora(default=datetime.datetime.now())
