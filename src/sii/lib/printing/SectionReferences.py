""" References Section of the Document

Contains:
    * Document Type
    * Document Serial Number
    * Document Date
    * Reason of Reference
"""
from .TemplateElement import TemplateElement


DOC_TYPE_STRINGS = {
    30:    "FACTURA",
    33:    "FACTURA ELECTRÓNICA",
    34:    "FACTURA NO AFECTA O EXENTA ELECTRÓNICA",
    50:    "GUÍA DE DESPACHO",
    52:    "GUÍA DE DESPACHO ELECTRÓNICA",
    56:    "NOTA DE DÉBITO ELECTRÓNICA",
    61:    "NOTA DE CRÉDITO ELECTRÓNICA",
    46:    "FACTURA DE COMPRA ELECTRÓNICA",
    43:    "LIQUIDACIÓN FACTURA ELECTRÓNICA",
    110:   "FACTURA DE EXPORTACIÓN ELECTRÓNICA",
    111:   "NOTA DE DÉBITO DE EXPORTACIÓN ELECTRÓNICA",
    112:   "NOTA DE CRÉDITO DE EXPORTACIÓN ELECTRÓNICA",
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
