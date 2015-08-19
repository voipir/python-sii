""" SII Document Node """
import datetime

from ..xml   import XMLNode, XMLNodeContainer
from ..types import SiiFechaHora

from .NodeEncabezado    import NodeEncabezado
from .NodeDetalle       import NodeDetalle
from .NodeSubTotInfo    import NodeSubTotInfo
from .NodeDescRecGlobal import NodeDescRecGlobal
from .NodeReferencia    import NodeReferencia
from .NodeComisiones    import NodeComisiones

from .NodeTimbreElectronico import NodeTimbreElectronico


class NodeDocumento(XMLNode):
    """
    TmstFirma: Fecha y Hora en que se Firmo Digitalmente el Documento AAAA-MM-DDTHH:MI:SS
    """
    __attributes__ = {'ID': 'F{self.Encabezado.IdDoc.Folio}T{self.Encabezado.IdDoc.TipoDTE}'}

    Encabezado   = NodeEncabezado()
    Detalle      = XMLNodeContainer(NodeDetalle,       min_occurs=1, max_occurs=60)
    SubTotInfo   = XMLNodeContainer(NodeSubTotInfo,    min_occurs=0, max_occurs=40)

    DscRcgGlobal = XMLNodeContainer(NodeDescRecGlobal, min_occurs=0, max_occurs=20)
    Referencia   = XMLNodeContainer(NodeReferencia,    min_occurs=0, max_occurs=40)
    Comisiones   = XMLNodeContainer(NodeComisiones,    min_occurs=0, max_occurs=20)
    TED          = NodeTimbreElectronico()
    TmstFirma    = SiiFechaHora(default=datetime.datetime.now())
