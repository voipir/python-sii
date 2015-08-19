"""
"""
from functools import partial

from ..xml   import XMLNode, XMLNodeContainer
from ..types import Enumeration, UnsignedInteger, String
from ..types import SiiDoctoType, SiiMontoPorcentaje, SiiFecha, SiiRUT, SiiValor, SiiMonto

from .NodeExtranjero    import NodeExtranjero
from .NodeIVANoRec      import NodeIVANoRec
from .NodeOtrosImp      import NodeOtrosImp
from .NodeLiquidaciones import NodeLiquidaciones


EnumIndFactCompra = partial(
    Enumeration,
    1,  # Emitido por el Emisor del Libro de Compra.
    optional=True
)

EnumEmisor = partial(
    Enumeration,
    1,  # Emitido por el Emisor del Libro de Compra.
    optional=True
)

EnumAnulado = partial(
    Enumeration,
    'A',  # Documento Anulado
    optional=True
)

EnumOperacion = partial(
    Enumeration,
    1,  # Agrega
    2,  # Elimina
    optional=True
)

EnumTpoImp = partial(
    Enumeration,
    1,  # IVA
    2,  # Ley 18.211
    optional=True
)

EnumIndServicio = partial(
    Enumeration,
    1,  # Facturacion de Servicios Periodicos Domiciliarios.
    2,  # Facturacion de Otros Servicios Periodicos.
    3,  # Facturacion de Servicios No Periodicos.
    optional=True
)

EnumIndSinCosto = partial(
    Enumeration,
    1,  # Entrega Gratuita
    optional=True
)


class NodeDetalle(XMLNode):
    """ Detalle de Documentos que Componen el Libro Electronico """

    # Specific to both Libro de Compra and Libro de Venta (General)
    TpoDoc        = SiiDoctoType()         # Tipo de Documento.
    NroDoc        = UnsignedInteger()      # Identificador o Folio del Documento.
    Emisor        = EnumEmisor()           # Indica si NDébito o NCrédito afecta a una Factura de Compra.
    IndFactCompra = EnumIndFactCompra()    # Indica si NDébito o NCrédito afecta a una Factura de Compra.
    Anulado       = EnumAnulado()          # Indica que el Estado del Documento es Anulado.
    Operacion     = EnumOperacion()        # Indica si Agrega o Elimina Informacion.
    TasaImp       = SiiMontoPorcentaje()   # Tasa de impuesto usada en la operación.
    NumInt        = String(max_length=10)  # Numero Interno.
    FchDoc        = SiiFecha               # Fecha del Documento (AAAA-MM-DD).
    CdgSIISucur   = UnsignedInteger()      # Codigo de Sucursal Entregado por el SII.
    RUTDoc        = SiiRUT()               # RUT del Contraparte en la Operación Comercial.
    RznSoc        = String(max_length=50)  # Razon Social de la Contraparte del Documento.
    MntExe        = SiiValor()             # Monto Exento o no Gravado del Documento.
    MntNeto       = SiiValor()             # Monto Neto del Documento.
    MntIVA        = SiiValor()             # Monto de IVA del Documento.
    Ley18211      = SiiMonto()             # Ley 18211.
    MntTotal      = SiiValor()             # Monto Total del Documento.
    IVANoRetenido = SiiMonto()             # IVA No Retenido.

    # Specific to Libro de Compra
    TpoImp           = EnumTpoImp()  # Tipo de Impuesto Usado en la Operacion (LC).
    MntActivoFijo    = SiiMonto()    # Monto Neto Activo Fijo (LC).
    MntIVAActivoFijo = SiiMonto()    # IVA de la Operacion de Activo Fijo (LC).
    IVAUsoComun      = SiiMonto()    # IVA de Compras Destinadas en Parte a Ventas Exentas y Afectas (LC).
    MntSinCred       = SiiMonto()    # Monto del Impuesto Sin Derecho a Credito (LC).
    TabPuros         = SiiMonto()    # Tabacos - Puros (LC).
    TabCigarrillos   = SiiMonto()    # Tabacos - Cigarrillos (LC).
    TabElaborado     = SiiMonto()    # Tabacos - Elaborados (LC).
    ImpVehiculo      = SiiMonto()    # Impuesto a Vehiculo (LC).

    # Specific to Libro de Venta
    IndServicio   = EnumIndServicio()  # Indica si Corresponde a un Servicio (LV).
    IndSinCosto   = EnumIndSinCosto()  # Indicador de Venta sin Costo (LV).
    TpoDocRef     = SiiDoctoType()     # Tipo de Documento de Referencia (LV).
    FolioDocRef   = UnsignedInteger()  # Folio del Documento Referenciado (LV).
    IVAFueraPlazo = SiiMonto()         # Solo Nota de Credito Fuera de Plazo (LV).
    IVAPropio     = SiiValor()         # IVA Propio en Operaciones a Cuenta de Terceros (LV).
    IVATerceros   = SiiValor()         # IVA por Cuenta de Terceros (LV).
    IVARetTotal   = SiiMonto()         # IVA Retenido Total (LV).
    IVARetParcial = SiiMonto()         # IVA Retenido Parcial (LV).
    CredEC        = SiiMonto()         # Credito 65% Empresas Constructoras (LV).
    DepEnvase     = SiiMonto()         # Deposito por Envase (LV).
    MntNoFact     = SiiValor()         # Monto No Facturable (LV).
    MntPeriodo    = SiiValor()         # Total Monto Periodo (LV).
    PsjNac        = SiiMonto()         # Venta Pasaje Nacional (LV).
    PsjInt        = SiiMonto()         # Venta Pasaje Internacional (LV).

    Extranjero    = XMLNodeContainer(NodeExtranjero, min_ocurrs=0)
    IVANoRec      = NodeIVANoRec()
    OtrosImp      = NodeOtrosImp()
    Liquidaciones = NodeLiquidaciones()
