""" Items Section of the Document

Contains:
    * Header Tags
    * Item Rows
"""
from .TemplateElement import TemplateElement


class TemplateItems(TemplateElement):
    """
    {
        \\extrarowsep=^-1pt_-1pt

        %%%% ITEM TABLE
        \\begin{longtabu}{%s}
            %%%% HEADER
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            %s

            \\firsthline[1mm]

            %%%% CONTENT
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            %s
            \\lasthline
        \\end{longtabu}
    }
    """
    def __init__(self, column_layout, table_margins=False, amount_unit='Kg'):
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
        self._amount_unit   = amount_unit

        self.__doc__ = self.__doc__ % (self._build_tablecols(), '%s', '%s', '%s', '%s', '%s', '%s')

    def append_row(self, row: tuple):
        """ Expecting the column tuple to be in the expected order the column layout was set up at
        init time.
        """
        if len(row) != len(self._colsettings):
            raise ValueError("Rows have to provide one value per set up Column:\n"
                             ">{0}<\n"
                             ">{1}<".format(', '.join([col for col in row]),
                                            ', '.join([col['name'] for col in self._colsettings])))
        else:
            self._items.append(row)

    @property
    def carta(self):
        return self.__doc__ % ('small', 'small',
                               self._build_headers(),
                               'footnotesize', 'footnotesize',
                               self._build_rows())

    @property
    def oficio(self):
        return self.__doc__ % ('small', 'small',
                               self._build_headers(),
                               'footnotesize', 'footnotesize',
                               self._build_rows())

    @property
    def thermal80mm(self):
        return self.__doc__ % ('scriptsize', 'scriptsize',
                               self._build_headers(),
                               'scriptsize', 'scriptsize',
                               self._build_rows())

    def _build_tablecols(self):
        cols = []
        cols.append('' if self._table_margins else '@{}')

        for coldef in self._colsettings:
            setstr  = 'X{'
            setstr += {True: '', False: '-1'}[coldef['expand']]
            setstr += {'left': 'l', 'center': 'c', 'right': 'r'}[coldef['align']]
            setstr += '}'
            cols.append(setstr)

        cols.append('' if self._table_margins else '@{}')
        return ' '.join(cols)

    def _build_headers(self):
        cols = ['\\textbf{%s}' % col['name'] for col in self._colsettings]
        tex  = (' & \n' + ' ' * 4 * 3).join(cols)
        tex += ' \\\\\n'

        return tex

    def _build_rows(self):
        rows = []
        for row in self._items:
            rows.append(' & '.join(row) + ' \\\\')
        return '\n'.join(rows)
