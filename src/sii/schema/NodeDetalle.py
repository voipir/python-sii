""" SII Document Items Information """
from .xml   import XMLNode, XMLTypeContainer, XMLNodeContainer
from .types import (UnsignedInteger, String,
                    SiiIndicadorExtencion, SiiMonto12Digitos6Decimales,
                    SiiFecha, SiiMonto, SiiMontoPorcentaje, SiiMontoImpuesto,
                    SiiMontoImpuestoAdicionalDTE)

from .NodeCdgItem          import NodeCdgItem
from .NodeRetenedor        import NodeRetenedor
from .NodeSubcantidad      import NodeSubcantidad
from .NodePrecioOtraMoneda import NodePrecioOtraMoneda
from .NodeSubDescuento     import NodeSubDescuento
from .NodeSubRecargo       import NodeSubRecargo


class NodeDetalle(XMLNode):
    """ Some Notes about Elements in this Structure:

    Retenedor: Sólo para transacciones realizadas por agentes retenedores.
    UnmdItem:  Unidad de medida.
    PrcItem:   Precio Unitario del Item en Pesos.

    DescuentoPct:   Porcentaje de Descuento.
    DescuentoMonto: Monto de Descuento.
    SubDscto:       Desglose del Descuento.

    CodImpAdic: Codigo de Impuesto Adicional o Retencion.
    MontoItem:  Monto por Linea de Detalle. Corresponde al Monto Neto, a menos que MntBruto Indique
                lo Contrario.
    """
    NroLinDet = UnsignedInteger(max_value=99)
    CdgItem   = XMLNodeContainer(NodeCdgItem, min_occurs=0, max_occurs=5)
    IndExe    = XMLTypeContainer(SiiIndicadorExtencion, min_occurs=0)
    Retenedor = XMLNodeContainer(NodeRetenedor, min_occurs=0)

    NmbItem = String(max_length=80)
    DscItem = String(optional=True, max_length=1000)
    QtyRef  = SiiMonto12Digitos6Decimales(optional=True)
    UnmdRef = String(optional=True, max_length=4)
    PrcRef  = SiiMonto12Digitos6Decimales(optional=True)
    QtyItem = SiiMonto12Digitos6Decimales(optional=True)

    Subcantidad = XMLNodeContainer(NodeSubcantidad, min_occurs=0, max_occurs=5)

    FchElabor = SiiFecha(optional=True)
    FchVencim = SiiFecha(optional=True)

    UnmdItem = String(optional=True, max_length=4)
    PrcItem  = SiiMonto12Digitos6Decimales()
    OtrMnda  = XMLNodeContainer(NodePrecioOtraMoneda, min_occurs=0)

    DescuentoPct   = SiiMontoPorcentaje(optional=True)
    DescuentoMonto = SiiMontoImpuesto(optional=True)
    SubDscto       = XMLNodeContainer(NodeSubDescuento, min_occurs=0, max_occurs=5)
    RecargoPct     = SiiMontoPorcentaje(optional=True, max_value=999.99)
    RecargoMonto   = SiiMontoImpuesto(optional=True)
    SubRecargo     = XMLNodeContainer(NodeSubRecargo, min_occurs=0, max_occurs=5)

    CodImpAdic = XMLTypeContainer(SiiMontoImpuestoAdicionalDTE, min_occurs=0, max_occurs=2)
    MontoItem  = SiiMonto()
