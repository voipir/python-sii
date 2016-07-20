""" Items Section of the Document

Contains:
    * Header Tags
    * Item Rows
"""
from .helpers import escape_tex

from .TemplateElement import TemplateElement


GUIA_DESPACHO_TYPES = {
    1: "OPERACIÓN CONSTITUYE VENTA",
    2: "VENTA POR EFECTUAR",
    3: "CONSIGNACION",
    4: "ENTREGA GRATUITA",
    5: "TRASLADO INTERNO",
    6: "OTRO TRASLADOS NO VENTA",
    7: "GUÍA DE DEVOLUCIÓN",
    8: "TRASLADO PARA EXPORTACIÓN. (NO VENTA)",
    9: "VENTA PARA EXPORTACIÓN"
}


class SectionItems(TemplateElement):
    """
    %%%% -----------------------------------------------------------------
    %%%% SECTION - Items
    %%%% -----------------------------------------------------------------
    {
        %%%% ITEM TABLE
        \\begin{longtabu}{%s}
            %%%% HEADER
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            %s

            \\firsthline[1mm]

            %%%% CONTENT
            %s
        \\end{longtabu}

        %s
    }
    """
    def __init__(self, column_layout, table_margins=False, draft=False, provider=False):
        """ Before using this Object you need to determine how the Columns are named, aligned and
        if they are expanding or not.
        You do that by providing the `column_layout` argument in the following Format:

            (
                {'name': 'Colname1', 'align': 'left'|'right'|'center', expand: True|False},
                {'name': 'Colname2', 'align': 'left'|'right'|'center', expand: True|False},
                {'name': 'Colname3', 'align': 'left'|'right'|'center', expand: True|False},
                ...
            )

        For proper LaTeX results it is recomended to make all but one Column non-expanding. This
        way the expanding one will take up as much space as possible without making spacing look
        ugly, but also ensuring everything looks not so overy spread (specially the numeric
        columns)
        """
        self._colsettings   = column_layout
        self._items         = []
        self._table_margins = table_margins
        self._draft         = draft
        self._provider      = provider

        self.__doc__ = self.__doc__ % (
            self._build_tablecols(),
            '%s', '%s', '%s', '%s', '%s'
        )

    def append_row(self, row: tuple):
        """ Expecting the column tuple to be in the expected order the column layout was set up at
        init time.
        """
        if len(row) != len(self._colsettings):
            raise ValueError(
                "Rows have to provide one value per set up Column:\n"
                ">{0}<\n"
                ">{1}<".format(
                    ', '.join([col for col in row]),
                    ', '.join([col['name'] for col in self._colsettings])
                )
            )
        else:
            self._items.append(row)

    @property
    def carta(self):
        return self.__doc__ % (
            'small', 'footnotesize',
            self._build_headers(),
            self._build_rows(),
            self._build_disclaimer()

        )

    @property
    def oficio(self):
        return self.__doc__ % (
            'small', 'footnotesize',
            self._build_headers(),
            self._build_rows(),
            self._build_disclaimer()
        )

    @property
    def thermal80mm(self):
        return self.__doc__ % (
            'scriptsize', 'scriptsize',
            self._build_headers(),
            self._build_rows(),
            self._build_disclaimer()
        )

    def _build_tablecols(self):
        cols = []
        cols.append('' if self._table_margins else '@{}')

        for coldef in self._colsettings:
            setstr  = 'X['
            setstr += {True: '', False: '-1'}[coldef['expand']]
            setstr += {'left': 'l', 'center': 'c', 'right': 'r'}[coldef['align']]
            setstr += ']'
            cols.append(setstr)

        cols.append('' if self._table_margins else '@{}')
        return ' '.join(cols)

    def _build_headers(self):
        cols = ['\\textbf{%s}' % escape_tex(col['name']) for col in self._colsettings]
        tex  = (' & \n' + ' ' * 4 * 3).join(cols)
        tex += ' \\\\\n'

        return tex

    def _build_rows(self):
        rows = []

        for row in self._items:
            stringed = (str(col) for col in row)
            escaped  = (escape_tex(colstr) for colstr in stringed)

            rows.append(' & '.join(escaped) + ' \\\\')

        return '\n'.join(rows)

    def _build_disclaimer(self):
        assert self.__document__, "Have not been yet registered onto a Document"

        disclaimers = []
        doc_gd_type = self.__document__.doc_gd_type

        if doc_gd_type:
            disclaimers.append('\\centerline{\\textbf{\\large --- %s ---}}' % GUIA_DESPACHO_TYPES[doc_gd_type])

        if self._draft:
            disclaimers.append('\\centerline{\\textbf{\\large --- %s ---}}' % "BORRADOR")

        if self._provider:
            disclaimers.append('\\centerline{\\textbf{\\large --- %s ---}}' % "DOCUMENTO PROVEEDOR")

        return "\n".join(disclaimers)
