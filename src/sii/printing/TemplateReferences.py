""" References Section of the Document

Contains:
    * Document Type
    * Document Serial Number
    * Document Date
    * Reason of Reference
"""
from .TemplateElement import TemplateElement


class TemplateReferences(TemplateElement):
    """
    {
        \\extrarowsep=^-1pt_-1pt

        %%%% ITEM TABLE
        \\begin{longtabu}{@{} X[-1l] X[-1r] X[-1c] X[-1r] @{}}
            %%%% HEADER
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            \\textbf{Tipo}  &
            \\textbf{Folio} &
            \\textbf{Fecha} &
            \\textbf{Razón} \\\\

            \\tabucline{1-4}

            %%%% CONTENT
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            %s
        \\end{longtabu}
    }
    """
    def __init__(self):
        self._refs = []

    def append_reference(self, doc_type, doc_serial, doc_date, reason):
        self._refs.append((doc_type, doc_serial, doc_date, reason))

    @property
    def carta(self):
        return self.__doc__ % ('small', 'footnotesize',
                               self._build_references())

    @property
    def oficio(self):
        return self.__doc__ % ('small', 'footnotesize',
                               self._build_references())

    @property
    def thermal80mm(self):
        return self.__doc__ % ('scriptsize', 'scriptsize',
                               self._build_references())

    def _build_references(self):
        refs = []
        for ref in self._refs:
            refs.append('{0} & {1} & {2} & {3} \\\\'.format(*ref))
        return ('\n' + ' ' * 4 * 3).join(refs)
