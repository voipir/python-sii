""" SII Caratula """
from ..xml   import XMLNode  # , XMLNodeContainer
from ..types import SiiRUT, SiiFecha, SiiFechaHora, SiiNroResolucion

from .NodeSubtotalDTE import NodeSubtotalDTE


class NodeCaratula(XMLNode):

    __attributes__ = {'version': "1.0"}

    RutEmisor    = SiiRUT()
    RutEnvia     = SiiRUT()
    RutReceptor  = SiiRUT()
    FchResol     = SiiFecha()
    NroResol     = SiiNroResolucion()
    TmstFirmaEnv = SiiFechaHora()

    SubTotDTE    = NodeSubtotalDTE()
