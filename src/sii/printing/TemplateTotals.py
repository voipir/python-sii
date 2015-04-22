""" Totals Section of the Document

Contains:
    * Discount
    * Net Amount
    * Tax exempt Amount
    * Tax
    * (optional) Other Tax Types
    * Total
"""
from .TemplateElement import TemplateElement


class TemplateTotals(TemplateElement):
    r"""
    {
        %s
        \\begin{longtabu}{%s}
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            & \\textbf{Descuento:}      & \\$%s \\
            & \\textbf{Monto Neto:}     & \\$%s \\
            & \\textbf{Monto Exento:}   & \\$%s \\
            %s
            & \\textbf{IVA (19\\%%%%):} & \\$%s \\

            \\tabucline{%s}

            & \\textbf{Monto Total:}  & \\$%s \\
        \\end{longtabu}
        %s
    }
    """
    def __init__(self, discount, net_value, exempt_value, tax, total, **kwargs):
        """ The only thing to remark here is the **kwargs/"other tax" which
        expects the following structure:

            {
                (19,        123456)  # as in...
                (<percent>, <value>)
                ...
            }
        """
        self._payments = []

        self._discount     = discount
        self._net_value    = net_value
        self._exempt_value = exempt_value
        self._tax          = tax
        self._other_tax    = kwargs
        self._total        = total

    @property
    def carta(self):
        return self.__doc__ % ('', '|X[-1] X[-1r] X[-1r]'
                               'small', 'small',
                               self._discount,
                               self._net_value,
                               self._exempt_value,
                               self._build_other_tax(),
                               self._tax,
                               '2-',
                               self._total,
                               '')

    @property
    def oficio(self):
        return self.__doc__ % ('', '|X[-1] X[-1r] X[-1r]'
                               'small', 'small',
                               self._discount,
                               self._net_value,
                               self._exempt_value,
                               self._build_other_tax(),
                               self._tax,
                               '2-',
                               self._total,
                               '')

    @property
    def thermal80mm(self):
        tex_spacing  = '\\extrarowsep=^-1pt_-1pt'
        tex_spacing += '\\vspace{-1em}'

        return self.__doc__ % (tex_spacing, '@{} X[-1l] X[r] @{}'
                               'scriptsize', 'scriptsize',
                               self._discount,
                               self._net_value,
                               self._exempt_value,
                               self._build_other_tax(),
                               self._tax,
                               '-',
                               self._total,
                               '\\vspace{-1em}')

    def _build_other_tax(self):
        rows = []
        for tax_type, detail in self._other_tax.items():
            percent, value = detail
            rows.append('& \\textbf{%s (%s\\%%%%):} & \\$%s \\' % (tax_type, percent,
                                                                   '{0:n}'.format(value)))
        return ('\n' + ' ' * 4 * 3).join(rows)
