""" XML Types specified by the SII
"""
import datetime

from .TypeBases import (String,
                        Integer,
                        UnsignedInteger,
                        # Decimal,
                        UnsignedDecimal,
                        Enumeration,
                        Date,
                        DateTime)


class SiiDoc(Enumeration):
    """ Todos los tipos de Documentos Tributarios Electronicos """

    def __init__(self, optional=False):
        super().__init__(
            33,   # Factura Electronica,
            34,   # Factura Electronica de Venta de Bienes y Servicios No afectos o Exento de IVA
            43,   #
            46,   # Factura de Compra Electronica
            52,   # Guia de Despacho Electronica
            56,   # Nota de Debito Electronica
            61,   # Nota de Credito Electronica
            110,  #
            111,  #
            112,  #
            optional=optional)


class SiiDTE(Enumeration):
    """ Tipos de Documentos Tributarios Electronicos """

    def __init__(self, optional=False):
        super().__init__(
            33,  # Factura Electronica
            34,  # Factura Electronica de Venta de Bienes y Servicios No afectos o Exento de IVA
            46,  # Factura de Compra Electronica

            # #FIXME: delete
            39,

            52,  # Guia de Despacho Electronica
            56,  # Nota de Debito Electronica
            61,  # Nota de Credito Electronica
            optional=optional)


class SiiDTEFactura(Enumeration):
    """ Tipos de Documentos Tributarios Electronicos """

    def __init__(self, optional=False):
        super().__init__(
            33,  # Factura Electronica
            34,  # Factura Electronica de Venta de Bienes y Servicios No afectos o Exento de IVA
            43,  # Liquidacion factura Electronica
            46,  # Factura de Compra Electronica
            optional=optional)


class SiiRUT(String):
    """ Rol Unico Tributario (99..99-X) """

    def __init__(self, optional=False):
        super().__init__(min_length=3,
                         max_length=10,
                         regex=r'^[0-9]+-([0-9]|K)$',
                         optional=optional)


class SiiMontoImpuesto(UnsignedInteger):
    """ Monto de Impuesto - 18 digitos """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=18,
                         optional=optional)


class SiiValor(Integer):
    """ Monto de 18 digitos - Positivo o Negativo """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=18,
                         optional=optional)


class SiiMonto(UnsignedInteger):
    """ Monto de 18 digitos - Positivo o Negativo """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=18,
                         optional=optional)


class SiiFolio(UnsignedInteger):
    """ Folio de DTE - 10 digitos """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=10,
                         optional=optional)


class SiiFolioReferencia(String):
    """ Folio de Referencia - 18 digitos (incluye el cero) """

    def __init__(self, optional=False):
        super().__init__(min_length=1,
                         max_length=18,
                         regex=r'^\d+$',
                         optional=optional)


class SiiMonto18Digitos(UnsignedInteger):
    """ Monto de 18 digitos """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=18,
                         optional=optional)


class SiiMonto16Digitos2Decimales(UnsignedDecimal):
    """ Monto con 16 Digitos de Cuerpo y 2 Decimales """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=16,
                         min_decimals=1,
                         max_decimals=2,
                         optional=optional)


class SiiMonto14Digitos4Decimales(UnsignedDecimal):
    """ Monto con 14 Digitos de Cuerpo y 4 Decimales """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=14,
                         min_decimals=1,
                         max_decimals=4,
                         optional=optional)


class SiiMonto12Digitos6Decimales(UnsignedDecimal):
    """ Monto con 12 Digitos de Cuerpo y 6 Decimales """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=12,
                         min_decimals=1,
                         max_decimals=6,
                         optional=optional)


class SiiMonto8Digitos4Decimales(UnsignedDecimal):
    """ Monto con 8 Digitos de Cuerpo y 4 Decimales """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=8,
                         min_decimals=1,
                         max_decimals=4,
                         optional=optional)


class SiiMonto6Digitos4Decimales(UnsignedDecimal):
    """ Monto con 6 Digitos de Cuerpo y 4 Decimales """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=6,
                         min_decimals=1,
                         max_decimals=4,
                         optional=optional)


class SiiMontoPorcentaje(UnsignedDecimal):
    """ Monto de Porcentaje (3 y 2) """

    def __init__(self, optional=False, **kwargs):
        super().__init__(min_digits=1,
                         max_digits=3,
                         min_decimals=1,
                         max_decimals=2,
                         optional=optional,
                         **kwargs)


class SiiUnidadValor(Enumeration):
    """ Unidad en que se expresa el Valor """

    def __init__(self, optional=False):
        super().__init__(
            '%',  # El valor se Expresa como Porcentaje
            '$',  # El Valor se Expresa en Pesos
            optional=optional)


class SiiMontoImpuestoAdicional(Enumeration):
    """ Tipo de Impuesto o Retencion Adicional """

    def __init__(self, optional=False):
        super().__init__(
            14,   # IVA Margen Comercializacion (Factura Venta del Contribuyente) [F29 - C039]
            15,   # IVA Retenido Total (Factura Compra del Contribuyente) [F29 - C039]
            16,   # IVA Retenido Parcial (Factura Compra del Contribuyente) [F29]
            17,   # IVA Anticipado Faenamiento Carne [F29 - C042]
            18,   # IVA Anticipado Carne [F29 - C042]
            19,   # IVA Anticipado Harina [F29 - C042]
            23,   # Impuesto Adicional Productos Art. 37 a) b) c)  Oro, Joyas, Pieles
                  # [F29 - C113]
            24,   # Impuesto Art. 42 a) Licores, Pisco, Destilados [F29 - C148]
            25,   # Impuesto Art. 42 c) Vinos
            26,   # Impuesto Art. 42 c) Cervezas y Bebidas Alcoholicas [F29 - C150]
            27,   # Impuesto Art. 42 d) y e) Bebidas Analcoholicas y Minerales [F29 - C146]
            28,   # Impuesto Especifico Diesel [F29 - C127]
            29,   # Recuperación Impuesto Específico diesel Transportistas  Para transportistas
                  # de carga Art 2° Ley N°19.764/2001
            30,   # IVA Retenido Legumbres
            31,   # IVA Retenido Silvestres
            32,   # IVA Retenido Ganado
            33,   # IVA Retenido Madera
            34,   # IVA Retenido Trigo
            35,   # Impuesto Especifico Gasolina
            36,   # IVA Retenido Arroz
            37,   # IVA Retenido Hidrobiologicas
            38,   # IVA Retenido Chatarra
            39,   # IVA Retenido PPA
            40,   # IVA Retenido Opcional
            41,   # IVA Retenido Construccion
            44,   # Impuesto Adicional Productos Art. 37 e) h) i) l) 1ra Venta (Alfombras, C.
                  # Rodantes, Caviar, Armas) [F29 - C113]
            45,   # Impuesto Adicional Productos Art. 37 j)  1ra Venta (Pirotecnia)
                  # [F29 - C113]
            46,   #
            47,   #
            48,   #
            49,   #
            50,   #
            51,   #
            52,   #
            53,   #
            301,  #
            321,  #
            331,  #
            341,  #
            361,  #
            371,  #
            481,  #
            optional=optional)


class SiiUnidadDinero(Enumeration):
    """ Unidad en que se expresa el Valor """

    def __init__(self, optional=False):
        super().__init__(
            '%',  # El valor se Expresa como Porcentaje
            '$',  # El Valor se Expresa en Pesos
            optional=optional)


class SiiMail(String):
    """ Dirección Email """

    def __init__(self, optional=False):
        super().__init__(max_length=80,
                         optional=optional)
        # regex=r'\w'  # TODO


class SiiMontoImpuestoAdicionalDTE(Enumeration):
    """ Tipo de Impuesto o Retencion Adicional de los DTE """

    def __init__(self, optional=False):
        super().__init__(
            14,   # IVA Margen Comercializacion (Factura Venta del Contribuyente) [F29 - C039]
            15,   # IVA Retenido Total (Factura Compra del Contribuyente) [F29 - C039]
            16,   # IVA Retenido Parcial (Factura Compra del Contribuyente) [F29]
            17,   # IVA Anticipado Faenamiento Carne [F29 - C042]
            18,   # IVA Anticipado Carne [F29 - C042]
            19,   # IVA Anticipado Harina [F29 - C042]
            23,   # Impuesto Adicional Productos Art. 37 a) b) c)  Oro, Joyas, Pieles
                  # [F29 - C113]
            24,   # Impuesto Art. 42 a) Licores, Pisco, Destilados [F29 - C148]
            25,   # Impuesto Art. 42 c) Vinos
            26,   # Impuesto Art. 42 c) Cervezas y Bebidas Alcoholicas [F29 - C150]
            27,   # Impuesto Art. 42 d) y e) Bebidas Analcoholicas y Minerales [F29 - C146]
            28,   # Impuesto Especifico Diesel [F29 - C127]
            30,   # IVA Retenido Legumbres
            31,   # IVA Retenido Silvestres
            32,   # IVA Retenido Ganado
            33,   # IVA Retenido Madera
            34,   # IVA Retenido Trigo
            35,   # Impuesto Especifico Gasolina
            36,   # IVA Retenido Arroz
            37,   # IVA Retenido Hidrobiologicas
            38,   # IVA Retenido Chatarra
            39,   # IVA Retenido PPA
            40,   # IVA Retenido Opcional
            41,   # IVA Retenido Construccion
            44,   # Impuesto Adicional Productos Art. 37 e) h) i) l)  1ra Venta (Alfombras, C.
                  # Rodantes, Caviar, Armas) [F29 - C113]
            45,   # Impuesto Adicional Productos Art. 37 j)  1ra Venta (Pirotecnia)
                  # [F29 - C113]
            46,   #
            47,   #
            48,   #
            49,   #
            50,   #
            51,   #
            52,   #
            53,   #
            301,  #
            321,  #
            331,  #
            341,  #
            361,  #
            371,  #
            481,  #
            optional=optional)


class SiiNroResolucion(UnsignedInteger):
    """ Número de Resolución """

    def __init__(self, optional=False):
        super().__init__(min_digits=1,
                         max_digits=6,
                         optional=optional)


class SiiRazonSocialLarga(String):
    """ Razón Social (max 100) """

    def __init__(self, optional=False):
        super().__init__(min_length=1,
                         max_length=100,
                         optional=optional)


class SiiRazonSocialCorta(String):
    """ Dirección (max 40) """

    def __init__(self, optional=False):
        super().__init__(min_length=1,
                         max_length=40,
                         optional=optional)


class SiiDireccion(String):
    """ Dirección (max 80) """

    def __init__(self, optional=False):
        super().__init__(max_length=80,
                         optional=optional)


class SiiDireccionDTE(String):
    """ Dirección (max 60) """

    def __init__(self, optional=False):
        super().__init__(max_length=60,
                         optional=optional)


class SiiComuna(String):
    """ Comuna """

    def __init__(self, optional=False):
        super().__init__(max_length=20,
                         optional=optional)


class SiiCiudad(String):
    """ Ciudad """

    def __init__(self, optional=False):
        super().__init__(max_length=20,
                         optional=optional)


class SiiFono(String):
    """ Fono """

    def __init__(self, optional=False):
        super().__init__(max_length=40,
                         optional=optional)


class SiiNombre(String):
    """ Nombre """

    def __init__(self, optional=False):
        super().__init__(max_length=40,
                         optional=optional)


class SiiTipoLiquidacion(Enumeration):
    """ Tipos de Liquidaciones """

    def __init__(self, optional=False):
        super().__init__(43,
                         optional=optional)


class SiiFacturaExporatacion(Enumeration):
    """ Tipos de Facturas de  Exportacion """

    def __init__(self, optional=False):
        super().__init__(
            110,  # unknown
            111,  # unknown
            112,  # unknown
            optional=optional)


class SiiMedioDePago(Enumeration):
    """ Medios de Pago """

    def __init__(self, optional=False):
        super().__init__(
            'CH',  # Cheque
            'LT',  # Letra
            'EF',  # Efectivo
            'PE',  # Pago a Cuenta Corriente
            'TC',  # Tarjeta de Credito
            'CF',  # Cheque a Fecha
            'OT',  # Otro
            optional=optional)


class SiiTipoMoneda(Enumeration):
    """ Tipos de Moneda de Aduana """

    def __init__(self, optional=False):
        super().__init__(
            'BOLIVAR',
            'BOLIVIANO',
            'CHELIN',
            'CORONA DIN',
            'CORONA NOR',
            'CORONA SC',
            'CRUZEIRO REAL',
            'DIRHAM',
            'DOLAR AUST',
            'DOLAR CAN',
            'DOLAR HK',
            'DOLAR NZ',
            'DOLAR SIN',
            'DOLAR TAI',
            'DOLAR USA',
            'DRACMA',
            'ESCUDO',
            'EURO',
            'FLORIN',
            'FRANCO BEL',
            'FRANCO FR',
            'FRANCO SZ',
            'GUARANI',
            'LIBRA EST',
            'LIRA',
            'MARCO AL',
            'MARCO FIN',
            'NUEVO SOL',
            'OTRAS MONEDAS',
            'PESETA',
            'PESO',
            'PESO CL',
            'PESO COL',
            'PESO MEX',
            'PESO URUG',
            'RAND',
            'RENMINBI',
            'RUPIA',
            'SUCRE',
            'YEN',
            optional=optional)


class SiiFecha(Date):
    """ Fecha entre 2000-01-01 y 2050-12-31 """

    def __init__(self, optional=False):
        super().__init__(
            min_date=datetime.date(year=2000, month=1,  day=1),
            max_date=datetime.date(year=2050, month=12, day=31),
            formatting='%Y-%m-%d',
            optional=optional)


class SiiFechaHora(DateTime):
    """ Fecha + Hora entre 00:00 y 23:59 """

    def __init__(self, default=None, optional=False):
        super().__init__(
            min_datetime=datetime.datetime(year=2000, month=1,  day=1,
                                           hour=0,    minute=0, second=0),
            max_datetime=datetime.datetime(year=2050, month=12,  day=31,
                                           hour=23,   minute=59, second=59),
            formatting='%Y-%m-%dT%H-%M-%S',
            default=default,
            optional=optional)


class SiiIndicadorExtencion(Enumeration):
    """ Indicador de Exencion """

    def __init__(self, optional=False):
        super().__init__(
            1,  # El Producto o Servicio NO ESTA Afecto a IVA.
            2,  # El Producto o Servicio NO ES Facturable.
            3,  # Garantia por Deposito/Envase.
            4,  # El producto No Constituye Venta.
            5,  # Item a Rebajar.
            6,  # No facturables negativos.
            optional=optional
        )


# Added for Libros de Venta/Compra
class SiiImpuesto(Enumeration):
    """ Tipo de Impuestos Adicionales (ImptoType) """

    def __init__(self, optional=False):
        super().__init__(
            14,  # IVA Margen de Comercializacion
            15,  # IVA Retenido Total
            16,  # IVA Retenido Parcial
            17,  # IVA Anticipado Faenamiento Carne
            18,  # IVA Anticipado Carne
            19,  # IVA Anticipado Harina
            23,  # Impuesto Art. 37 Letras a, b, c
            24,  # Impuesto Art. 42 Ley 825/74 Letra a
            25,  # Impuesto Art. 42 Letra c
            26,  # Impuesto Art. 42 Letra c
            27,  # Impuesto Art. 42 Letra d y e
            28,  # Impuesto Especifico Diesel
            29,  # Recuperacion Impuesto Especifico Diesel Transportistas
            30,  # IVA Retenido Legumbres
            31,  # IVA Retenido Silvestres
            32,  # IVA Retenido Ganado
            33,  # IVA Retenido Madera
            34,  # IVA Retenido Trigo
            35,  # Impuesto Especifico Gasolina
            36,  # IVA Retenido Arroz
            37,  # IVA Retenido Hidrobiologicas
            38,  # IVA Retenido Chatarra
            39,  # IVA Retenido PPA
            40,  # IVA Retenido Opcional
            # 41,
            44,  # Impuesto Art. 37 Letras e, f, g y h
            45,  # Impuesto Art. 37 Letra j
            # 46,
            # 47,
            # 48,
            # 49,
            # 50,
            # 51,
            # 52,
            53,  # Impuesto retenido a los suplementeros Art. 74 N°5
            # 60,
            # 301,
            # 321,
            # 331,
            # 341,
            # 361,
            # 371,
            # 481,
            optional=optional
        )


class SiiDoctoType(Enumeration):
    """ Tipos de Documentos """

    def __init__(self, optional=False):
        super().__init__(
            29,
            30,
            32,
            33,
            34,
            35,
            38,
            39,
            40,
            41,
            43,
            45,
            46,
            53,
            55,
            56,
            60,
            61,
            101,
            102,
            103,
            104,
            105,
            106,
            108,
            109,
            110,
            111,
            112,
            175,
            180,
            185,
            900,
            901,
            902,
            903,
            904,
            905,
            906,
            907,
            909,
            910,
            911,
            914,
            918,
            919,
            920,
            921,
            922,
            924,
            500,
            501,
            optional=optional
        )
