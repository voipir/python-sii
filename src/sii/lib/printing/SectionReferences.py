""" References Section of the Document

Contains:
    * Document Type
    * Document Serial Number
    * Document Date
    * Reason of Reference
"""
from .TemplateElement import TemplateElement


DOC_TYPE_STRINGS = {
    30   : "FACTURA",
    32   : "FACTURA NO AFECTA O EXENTA",
    33   : "FACTURA ELECTRÓNICA",
    34   : "FACTURA NO AFECTA O EXENTA ELECTRÓNICA",
    35   : "BOLETA",
    38   : "BOLETA EXENTA",
    39   : "BOLETA ELECTRÓNICA",
    40   : "LIQUIDACIÓN FACTURA",
    41   : "BOLETA EXENTA ELECTRÓNICA",
    43   : "LIQUIDACIÓN FACTURA ELECTRÓNICA",
    45   : "FACTURA DE COMPRA",
    46   : "FACTURA DE COMPRA ELECTRÓNICA",
    50   : "GUÍA DE DESPACHO.",
    52   : "GUÍA DE DESPACHO ELECTRÓNICA",
    55   : "NOTA DE DÉBITO",
    56   : "NOTA DE DÉBITO ELECTRÓNICA",
    60   : "NOTA DE CRÉDITO",
    61   : "NOTA DE CRÉDITO ELECTRÓNICA",
    103  : "LIQUIDACIÓN",
    110  : "FACTURA DE EXPORTACIÓN ELECTRÓNICA",
    111  : "NOTA DE DÉBITO DE EXPORTACIÓN ELECTRÓNICA",
    112  : "NOTA DE CRÉDITO DE EXPORTACIÓN ELECTRÓNICA",
    801  : "ORDEN DE COMPRA",
    802  : "NOTA DE PEDIDO",
    803  : "CONTRATO",
    804  : "RESOLUCIÓN",
    805  : "PROCESO CHILECOMPRA",
    806  : "FICHA CHILECOMPRA",
    807  : "DUS",
    808  : "B/L (CONOCIMIENTO DE EMBARQUE)",
    809  : "AWB (AIR WILL BILL)",
    810  : "MIC/DTA",
    811  : "CARTA DE PORTE",
    812  : "RESOLUCIÓN DEL SNA DONDE CALIFICA SERVICIOS DE EXPORTACIÓN",
    813  : "PASAPORTE",
    814  : "CERTIFICADO DE DEPÓSITO BOLSA PROD. CHILE.",
    815  : "VALE DE PRENDA BOLSA PROD. CHILE",
    'SET': "SET"
}


class SectionReferences(TemplateElement):
    """
    %% -----------------------------------------------------------------
    %% SECTION - References
    %% -----------------------------------------------------------------
    {
        %%%% ITEM TABLE
        \\begin{longtabu}{@{} X[-1l] X[l] X[-1r] X[-1r] X[-1r] @{}}
            %%%% HEADER
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            \\textbf{Nro.}  &
            \\textbf{Razón} &
            \\textbf{Tipo}  &
            \\textbf{Folio} &
            \\textbf{Fecha} \\\\

            %%\\tabucline{1-4}
            \\firsthline[1mm]

            %%%% CONTENT
            %s
        \\end{longtabu}
    }
    """
    def __init__(self):
        self._refs = []

    def append_reference(self, reason, index, dte_type, dte_serial, dte_date):
        self._refs.append((
            index,
            reason,
            DOC_TYPE_STRINGS[dte_type],
            dte_serial,
            dte_date
        ))

    @property
    def carta(self):
        return self.__doc__ % (
            'small',
            'footnotesize',
            self._build_references(),
        )

    @property
    def oficio(self):
        return self.__doc__ % (
            'small',
            'footnotesize',
            self._build_references()
        )

    @property
    def thermal80mm(self):
        return self.__doc__ % (
            'scriptsize',
            'scriptsize',
            self._build_references()
        )

    def _build_references(self):
        refs = []

        for ref in self._refs:
            refs.append('{0} & {1} & {2} & {3} & {4}\\\\'.format(*ref))

        if refs:
            return ('\n' + ' ' * 4 * 3).join(refs)
        else:
            return '– sin referencias –'
