""" SII Tax Retainee Information """
from .xml   import XMLNode
from .types import String, SiiMonto


class NodeRetenedor(XMLNode):
    """ Some Notes about Elements in this Structure:

    IndAgente:    Indicador Agente Retenedor.
    MntBaseFaena: Monto Base Faenamiento.
    MntMargComer: Márgenes de Comercialización.
    PrcConsFinal: Precio Unitario Neto Consumidor Final.
    """
    IndAgente    = String(regex=r'^R$')
    MntBaseFaena = SiiMonto(optional=True)
    MntMargComer = SiiMonto(optional=True)
    PrcConsFinal = SiiMonto(optional=True)
