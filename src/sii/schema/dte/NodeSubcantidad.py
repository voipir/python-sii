""" SII Sub-Quantity Information """
from ..xml   import XMLNode
from ..types import String, SiiMonto12Digitos6Decimales


class NodeSubcantidad(XMLNode):
    """ Some Notes about Elements in this Structure:

    SubQty: Cantidad Distribuida.
    SubCod: Codigo Descriptivo de la Subcantidad.
    """
    SubQty = SiiMonto12Digitos6Decimales()
    SubCod = String(max_length=35)
