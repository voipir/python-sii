""" SII Customs Information """
from ..xml   import XMLNode, XMLNodeContainer
from ..types import (String, UnsignedInteger, Decimal,
                    SiiRUT, SiiMonto16Digitos2Decimales, SiiMonto14Digitos4Decimales)

from .NodeBultos import NodeBultos


class NodeAduana(XMLNode):
    """ Some Notes about Elements in this Structure:

    CodModVenta:    Código según  tabla "Modalidad de Venta" de aduana.
    CodClauVenta:   Código según  Tabla "Cláusula compra-venta" de aduana.
    CodViaTransito: Indicar el Código de la vía de transporte utilizada para transportar la
                    mercadería, según tabla Vías de Transporte de Aduana.
    Booking:        Numero de reserva del Operador.
    Operador:       Código del Operador
    CodPtoEmbarque: Código del puerto de embarque según tabla de Aduana.
    PesoBruto:      Sumatoria de los pesos brutos de todos los ítems del documento.
    MntFlete:       Monto del flete según moneda de venta.
    MntSeguro:      Monto del seguro según moneda de venta.
    CodPaisRecep:   Código del país del receptor extranjero de la mercadería,
                    según tabla Países aduana.
    CodPaisDestin:  Código del país de destino extranjero de la mercadería,
                    según tabla Países aduana.
    """

    CodModVenta     = UnsignedInteger(optional=True, min_digits=2, max_digits=2)
    CodClauVenta    = UnsignedInteger(optional=True, min_digits=2, max_digits=2)
    TotClauVenta    = SiiMonto16Digitos2Decimales(optional=True)
    CodViaTransito  = UnsignedInteger(optional=True, min_digits=2, max_digits=2)
    NombreTransp    = String(optional=True, max_length=40)
    RUTCiaTransp    = SiiRUT(optional=True)
    NomCiaTransp    = String(optional=True, max_length=40)
    IdAdicTransp    = String(optional=True, min_length=1, max_length=20)
    Booking         = String(optional=True, min_length=1, max_length=20)
    Operador        = String(optional=True, min_length=1, max_length=20)
    CodPtoEmbarque  = UnsignedInteger(optional=True, min_digits=4, max_digits=4)
    IdAdicPtoEmb    = String(optional=True, min_length=1, max_length=20)
    CodPtoDesemb    = UnsignedInteger(optional=True, min_digits=4, max_digits=4)
    IdAdicPtoDesemb = String(optional=True, min_length=1, max_length=20)
    Tara            = UnsignedInteger(optional=True, min_digits=7, max_digits=7)
    CodUnidMedTara  = UnsignedInteger(optional=True, min_digits=2, max_digits=2)
    PesoBruto       = Decimal(optional=True, min_digits=8, max_digits=8,
                                                 min_decimals=2, max_decimals=2)
    CodUnidPesoBruto = UnsignedInteger(optional=True, min_digits=2, max_digits=2)
    PesoNeto         = Decimal(optional=True, min_digits=8, max_digits=8,
                                                  min_decimals=2, max_decimals=2)
    CodUnidPesoNeto = UnsignedInteger(optional=True, min_digits=2, max_digits=2)
    TotItems        = UnsignedInteger(optional=True, max_digits=18)
    TotBultos       = UnsignedInteger(optional=True, max_digits=18)
    TipoBultos      = XMLNodeContainer(NodeBultos, min_occurs=0, max_occurs=10)
    MntFlete        = SiiMonto14Digitos4Decimales(optional=True)
    MntSeguro       = SiiMonto14Digitos4Decimales(optional=True)
    CodPaisRecep    = UnsignedInteger(optional=True, min_digits=3, max_digits=3)
    CodPaisDestin   = UnsignedInteger(optional=True, min_digits=3, max_digits=3)
