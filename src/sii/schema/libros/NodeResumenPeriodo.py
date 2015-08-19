"""
"""
from .xml import XMLNode, XMLNodeContainer

from .NodeTotalesPeriodo import NodeTotalesPeriodo


class NodeResumenPeriodo(XMLNode):
    """ Resumen Para el Periodo Tributario """

    TotalesPeriodo = XMLNodeContainer(NodeTotalesPeriodo, max_occurs=40)
