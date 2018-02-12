# -*- coding: utf-8 -*-
""" Payments Section of the Document

Contains:
    * Payment Mode/Type
    * Amount
    * Descriptor (Payment Detail / further Information / Description)
"""
from .TemplateElement import TemplateElement


class SectionPayments(TemplateElement):
    """
    %%%% -----------------------------------------------------------------
    %%%% SECTION - Payments
    %%%% -----------------------------------------------------------------
    {
        \extrarowsep=^1pt_1pt

        \\begin{longtabu}{%s}
            %%%% HEADER
            \\rowfont{\\%s}
            \everyrow{\\rowfont{\\%s}}
            \\textbf{Tipo Pago} &
            \\textbf{Monto[\$]} &
            \\textbf{Detalle}   \\\\

            %%%% DATA
            \\rowfont{\\%s}
            \everyrow{\\rowfont{\\%s}}
            %s
        \end{longtabu}
    }
    """
    def __init__(self, table_margins=False):
        self._payments = []

        self._table_margins = table_margins

    def append_payment(self, mode, amount, detail):
        self._payments.append((mode, amount, detail))

    @property
    def carta(self):
        return self.__doc__ % (
            self._build_tablecols(),
            'small',
            'small',
            'footnotesize',
            'footnotesize',
            self._build_payments()
        )

    @property
    def oficio(self):
        return self.__doc__ % (
            self._build_tablecols(),
            'small',
            'small',
            'footnotesize',
            'footnotesize',
            self._build_payments()
        )

    @property
    def thermal80mm(self):
        return self.__doc__ % (
            self._build_tablecols(),
            'scriptsize',
            'scriptsize',
            'scriptsize',
            'scriptsize',
            self._build_payments()
        )

    def _build_tablecols(self):
        return 'X[-1l] X[-1r] X[l]' if self._table_margins else '@{} X[-1l] X[-1r] X[l] @{}'

    def _build_payments(self):
        pays = []
        for pay in self._payments:
            pays.append('{0} & {1} & {2} \\\\'.format(*pay))

        if pays:
            return ('\n' + ' ' * 4 * 3).join(pays)
        else:
            return ''
