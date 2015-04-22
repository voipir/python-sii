""" Emitter Section of the Document

Contains:
    * Emitter Name (full Version)
    * Emitter Activity (Economic Role)
    * Emitter HQ Address String
    * Emitter emitting Branch String

    * (carta/oficio only) Logo (Optional) [takes the path to the logo EPS]

    * (thermal*mm only) Emitter Name (short Version)
    * (thermal*mm only) Emitter Salesman
    * (thermal*mm only) Order Number
    * (thermal*mm only) Licence Plate
"""
from .TemplateElement import TemplateElement


class TemplateEmitter(TemplateElement):
    """
    \\begin{minipage}[t]{0.6\\textwidth}
        \\begin{center}
            \\Large{\\textbf{%s}}\\break
            \\normalsize{%s}
            \\vspace{2mm}
            {
                \\extrarowsep=_-1pt^-1pt
                \\begin{tabu}{X[-1r] X[-1l]}
                    \\rowfont{\\scriptsize}
                    \\everyrow{\\rowfont{\\scriptsize}}
                    \\textbf{CASA MATRIZ:}      & %s  \\
                    \\textbf{SUCURSAL EMISORA:} & %s  \\
                \\end{tabu}
            }
            \\vspace{2mm}
            \\includegraphics[width=0.7\\textwidth]{%s}
        \\end{center}
        \\vfill
    \\end{minipage}%%%%
    """
    def __init__(self, emitter_name_long, emitter_name_short,
                       emitter_activity,
                       emitter_hq_addr, emitter_branch_addr,
                       order_number='', emitter_salesman='', licence_plate='',
                       logo_path=''):
        self._emitter_name_long   = emitter_name_long
        self._emitter_name_short  = emitter_name_short
        self._emitter_activity    = emitter_activity
        self._emitter_hq_addr     = emitter_hq_addr
        self._emitter_branch_addr = emitter_branch_addr

        # carta/oficio specifics
        self._logo_path = logo_path

        # thermal*mm specifics
        self._order_number     = order_number
        self._licence_plate    = licence_plate
        self._emitter_salesman = emitter_salesman

    @property
    def carta(self):
        return self.__doc__ % (self._emitter_name_long, self._emitter_activity,
                               self._emitter_hq_addr, self._emitter_branch_addr,
                               self._logo_path)

    @property
    def oficio(self):
        return self.__doc__ % (self._emitter_name_long, self._emitter_activity,
                               self._emitter_hq_addr, self._emitter_branch_addr,
                               self._logo_path)

    @property
    def thermal80mm(self):
        tex = """
           {
            \\scriptsize
            \\tabulinesep=_1.0mm^1.0mm

            \\textbf{RAZON SOCIAL EMISOR:} \\
            \\begin{tabu}{@{} X[-1l] X[l] @{}}
                \\textbf{Nombre:}               & %s  \\
                \\textbf{Giro:}                 & %s  \\
                \\textbf{Casa Matriz:}          & %s  \\
                \\textbf{Sucursal:}             & %s  \\
                \\textbf{N\\textdegree Pedido:} & %s  \\
                \\textbf{Vendedor:}             & %s  \\
                \\textbf{Patente:}              & %s  \\
            \\end{tabu}
            }%%%%
        """
        return tex % (self._emitter_name_short, self._emitter_activity,
                      self._emitter_hq_addr, self._emitter_branch_addr,
                      self._order_number, self._emitter_salesman, self._licence_plate)
