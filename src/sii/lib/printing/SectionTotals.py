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


SPECIAL_TAX = {
    19:  ('IAH',   12, '+'),
    15:  ('RTT',   19, '-'),
    33:  ('IRM',    8, '-'),
    331: ('IRM',   19, '-'),
    34:  ('IRT',    4, '-'),
    39:  ('IRPPA', 19, '-')
}


class SectionTotals(TemplateElement):
    """
    %%%% -----------------------------------------------------------------
    %%%% SECTION - Totals
    %%%% -----------------------------------------------------------------
    {
        %s
        \\begin{longtabu}{%s}
            \\rowfont{\\%s}
            \\everyrow{\\rowfont{\\%s}}
            \\textbf{Desc. Global:}   & %s \\$ \\\\
            \\textbf{Monto Neto:}     & %s \\$ \\\\
            \\textbf{Monto Exento:}   & %s \\$ \\\\
            \\textbf{(19\\%%) IVA:}   & %s \\$ \\\\
            %s

            \\tabucline{%s}

            \\textbf{Monto Total:}  & %s \\$ \\\\
        \\end{longtabu}
        %s
    }
    """
    def __init__(self, discount, net_value, exempt_value, tax, total, special_tax=None):
        """ The only thing to remark here is the **kwargs/"other tax" which
        expects the following structure:

            {
                19: (12, 123456),  # as in... <code>: (<rate>, <value>)
                ...
            }
        """
        self._payments = []

        self._discount     = discount
        self._net_value    = net_value
        self._exempt_value = exempt_value
        self._tax          = tax
        self._other_tax    = special_tax or {}
        self._total        = total

    @property
    def carta(self):
        tex = self.__doc__ % (
            '',
            'X[-1r] X[-1r]',
            'small',
            'small',
            self._discount,
            self._net_value,
            self._exempt_value,
            self._tax,
            self._build_other_tax(),
            '2-',
            self._total,
            ''
        )
        return tex

    @property
    def oficio(self):
        tex = self.__doc__ % (
            '',
            'X[-1r] X[-1r]',
            'small',
            'small',
            self._discount,
            self._net_value,
            self._exempt_value,
            self._tax,
            self._build_other_tax(),
            '2-',
            self._total,
            ''
        )
        return tex

    @property
    def thermal80mm(self):
        tex_spacing  = '\\extrarowsep=^-1pt_-1pt'
        tex_spacing += '\\vspace{-1em}'

        tex = self.__doc__ % (
            tex_spacing,
            '@{} X[-1l] X[r] @{}',
            'scriptsize',
            'scriptsize',
            self._discount,
            self._net_value,
            self._exempt_value,
            self._tax,
            self._build_other_tax(),
            '-',
            self._total,
            '\\vspace{-1em}'
        )
        return tex

    def _build_other_tax(self):
        rows = []

        for code, detail in self._other_tax.items():
            name, rate, sign = SPECIAL_TAX[code]
            _, value         = detail

            value_templ = ""
            if sign == '-':
                value_templ += "-{0}"
            else:
                value_templ += "{0}"

            rows.append(
                '\\textbf{(%s\\%%) %s:} & %s \\$\\\\' % (
                    value_templ.format(rate),
                    name,
                    value_templ.format(value)
                )
            )

        if rows:
            return ('\n' + ' ' * 4 * 3).join(rows)
        else:
            return ''
