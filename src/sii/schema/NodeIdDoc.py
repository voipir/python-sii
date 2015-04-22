""" SII Document ID """
from .xml   import XMLNode, XMLNodeContainer
from .types import Enumeration, String, UnsignedInteger
from .types import SiiDTE, SiiFolio, SiiFecha, SiiMonto, SiiMedioDePago

from .NodePagos import NodePagos


class NodeIdDoc(XMLNode):
    """ Some Notes on Node Attributes;

    IndNoRebaja:  Nota de Credito sin Derecho a Descontar Debito;
                  1: Nota de Credito sin Derecho a Descontar Debito

    TipoDespacho: 1: Despacho por Cuenta del Comprador
                  2: Despacho por Cuenta del Emisor a Instalaciones del Comprador
                  3: Despacho por Cuenta del Emisor a Otras Instalaciones

    IndTraslado:  Incluido en Guias de Despacho para Especifiicar el Tipo de Traslado de Productos.
                  1: Operacion Constituye Venta.
                  2: Venta por Efectuar.
                  3: Consignacion.
                  4: Promocion o Donacion (RUT Emisor = RUT Receptor).
                  5: Traslado Interno.
                  6: Otros Traslados que no Constituyen Venta.
                  7: Guia de Devolucion.
                  8: –reservado/desconocido–
                  9: –reservado/desconocido–

    TpoImpresion: Tipo de impresión;
                  N: Normal
                  T: Ticket

    IndServicio:  Indica si Transaccion Corresponde a la Prestacion de un Servicio;
                  1: Facturacion de Servicios Periodicos Domiciliarios.
                  2: Facturacion de Otros Servicios Periodicos.
                  3: Factura de Servicio.

    MntBruto:     Indica el Uso de Montos Brutos en Detalle;
                  1: Monto de Lineas de Detalle Corresponde a Valores Brutos (IVA + Impuestos
                     Adicionales).

    FmaPago:      Forma de Pago del DTE;
                  1: Pago Contado.
                  2: Pago Credito.
                  3: Sin Costo.

    FmaPagExp:    Forma de Pago Exportación Tabla Formas de Pago de Aduanas.

    FchCancel:    Fecha de Cancelacion del DTE (AAAA-MM-DD).
    MntCancel:    Monto Cancelado al emitirse el documento.
    SaldoInsol:   Saldo Insoluto al emitirse el documento.

    MntPagos:     Tabla de Montos de Pago.

    PeriodoDesde: Periodo de Facturacion - Desde (AAAA-MM-DD).
    PeriodoHasta: Periodo Facturacion    - Hasta (AAAA-MM-DD).

    MedioPago:     Medio de Pago.
    TpoCtaPago:    Tipo Cuenta de Pago.
    NumCtaPago:    Número de la cuenta del pago.
    BcoPago:       Banco donde se realiza el pago.
    TermPagoCdg:   Codigo del Termino de Pago Acordado.
    TermPagoGlosa: Términos del Pago - Glosa.
    TermPagoDias:  Dias de Acuerdo al Codigo de Termino de Pago.
    FchVenc:       Fecha de Vencimiento del Pago (AAAA-MM-DD).
    """

    TipoDTE = SiiDTE()
    Folio   = SiiFolio()
    FchEmis = SiiFecha()

    IndNoRebaja = Enumeration(1,             optional=True)
    IndTraslado = Enumeration(*range(1, 10), optional=True)
    IndServicio = Enumeration(1, 2, 3,       optional=True)

    TipoDespacho = Enumeration(1, 2, 3,  optional=True)
    TpoImpresion = Enumeration("N", "T", optional=True)

    MntBruto = Enumeration(1, optional=True)

    FmaPago    = Enumeration(1, 2, 3, optional=True)
    FmaPagExp  = UnsignedInteger(max_digits=2, optional=True)
    FchCancel  = SiiFecha(optional=True)
    MntCancel  = SiiMonto(optional=True)
    SaldoInsol = SiiMonto(optional=True)

    MntPagos = XMLNodeContainer(NodePagos, min_occurs=0, max_occurs=30)

    PeriodoDesde = SiiFecha(optional=True)
    PeriodoHasta = SiiFecha(optional=True)

    MedioPago     = SiiMedioDePago(optional=True)
    TpoCtaPago    = Enumeration("AHORRO",
                                "CORRIENTE",
                                "VISTA",
                                optional=True)
    NumCtaPago    = String(max_length=20,         optional=True)
    BcoPago       = String(max_length=40,         optional=True)
    TermPagoCdg   = String(max_length=4,          optional=True)
    TermPagoGlosa = String(max_length=100,        optional=True)
    TermPagoDias  = UnsignedInteger(max_digits=3, optional=True)
    FchVenc       = SiiFecha(optional=True)
