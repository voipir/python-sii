""" SII Subtotal DTE """
from ..xml   import XMLNode
from ..types import SiiDTE, SiiFolio


class NodeSubtotalDTE(XMLNode):

    TpoDTE = SiiDTE()
    NroDTE = SiiFolio()
