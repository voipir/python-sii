""" SII Document Header """
from .xml   import XMLNode
from .types import SiiRUT

from .NodeIdDoc      import NodeIdDoc
from .NodeEmisor     import NodeEmisor
from .NodeReceptor   import NodeReceptor
from .NodeTransporte import NodeTransporte
from .NodeTotales    import NodeTotales
from .NodeOtraMoneda import NodeOtraMoneda


class NodeEncabezado(XMLNode):

    IdDoc       = NodeIdDoc()
    Emisor      = NodeEmisor()
    RUTMandante = SiiRUT(optional=True)
    Receptor    = NodeReceptor()

    RUTSolicita = SiiRUT(optional=True)
    Transporte  = NodeTransporte(optional=True)
    Totales     = NodeTotales()
    OtraMoneda  = NodeOtraMoneda(optional=True)
