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

Comes in two flavours:

    * Emitter  (emitting company is the same as the one printing the document)
    * Provider (emitting company is a provider for the one printing the document)
"""
import os.path as path

from .TemplateElement import TemplateElement, Resource

__all__ = [
    'SectionEmitter',
    'SectionEmitterProvider'
]


class SectionEmitter(TemplateElement):
    """
    %% -----------------------------------------------------------------
    %% SECTION - Emitter
    %% -----------------------------------------------------------------
    \\begin{minipage}[t]{\\textwidth}
        \\begin{center}
            \\Large{\\textbf{%s}}\\break
            \\normalsize{%s}
            \\vspace{2mm}
            {
                \\extrarowsep=_-1pt^-1pt
                \\begin{tabu}{X[-1r] X[-1l]}
                    \\rowfont{\\scriptsize}
                    \\everyrow{\\rowfont{\\scriptsize}}
                    \\textbf{CASA MATRIZ:}      & %s  \\\\
                    \\textbf{SUCURSAL EMISORA:} & %s  \\\\
                    \\textbf{FONO:}             & %s  \\\\
                \\end{tabu}
            }
            \\vspace{2mm}
            %s
        \\end{center}
        \\vfill
    \\end{minipage}%%%%
    """
    def __init__(self, emitter_name_long, emitter_name_short,
                       emitter_activity,
                       emitter_hq_addr, emitter_branch_addr, emitter_phone,
                       order_number='', emitter_salesman='', licence_plate='',
                       logo_path=''):
        self._emitter_name_long   = emitter_name_long
        self._emitter_name_short  = emitter_name_short
        self._emitter_activity    = emitter_activity
        self._emitter_hq_addr     = emitter_hq_addr
        self._emitter_branch_addr = emitter_branch_addr
        self._emitter_phone       = emitter_phone

        # carta/oficio specifics
        self._logo_path = logo_path
        if self._logo_path:
            with open(self._logo_path, 'rb') as fh:
                self._logo_data = fh.read()

        # thermal*mm specifics
        self._order_number     = order_number
        self._licence_plate    = licence_plate
        self._emitter_salesman = emitter_salesman

    @property
    def resources(self):
        ress = []

        if self._logo_path:
            _, ext = path.splitext(self._logo_path)
            ress.append(Resource('logo' + ext, self._logo_data))

        return ress

    @property
    def carta(self):
        return self.__doc__ % (
            self._emitter_name_long,
            self._emitter_activity,
            self._emitter_hq_addr,
            self._emitter_branch_addr,
            self._emitter_phone,
            self._logo_template()
        )

    @property
    def oficio(self):
        return self.__doc__ % (
            self._emitter_name_long,
            self._emitter_activity,
            self._emitter_hq_addr,
            self._emitter_branch_addr,
            self._emitter_phone,
            self._logo_template()
        )

    @property
    def thermal80mm(self):
        tex = """
           {
            \\scriptsize
            \\tabulinesep=_1.0mm^1.0mm

            \\textbf{RAZON SOCIAL EMISOR:} \\\\
            \\begin{tabu}{@{} X[-1l] X[l] @{}}
                \\textbf{Nombre:}               & %s  \\\\
                \\textbf{Giro:}                 & %s  \\\\
                \\textbf{Casa Matriz:}          & %s  \\\\
                \\textbf{Sucursal:}             & %s  \\\\
                \\textbf{Fono:}                 & %s  \\\\
                \\textbf{N\\textdegree Pedido:} & %s  \\\\
                \\textbf{Vendedor:}             & %s  \\\\
                \\textbf{Patente:}              & %s  \\\\
            \\end{tabu}
            }%%%%
        """
        return tex % (
            self._emitter_name_short,
            self._emitter_activity,
            self._emitter_hq_addr,
            self._emitter_branch_addr,
            self._emitter_phone,
            self._order_number,
            self._emitter_salesman,
            self._licence_plate
        )

    def _logo_template(self):
        if self._logo_path:
            _, ext = path.splitext(self._logo_path)

            height    = '15mm'
            width     = '0.7\\textwidth'
            keepratio = 'true'

            return '\\includegraphics[height={h}, width={w}, keepaspectratio={r}]{{logo{ext}}}'.format(
                h   = height,
                w   = width,
                r   = keepratio,
                ext = ext
            )
        else:
            return ''


class SectionEmitterProvider(TemplateElement):
    """
    %% -----------------------------------------------------------------
    %% SECTION - Emitter
    %% -----------------------------------------------------------------
    \\begin{minipage}[t]{\\textwidth}
        \\begin{center}
            \\Large{\\textbf{%s}}\\break
            \\normalsize{%s}
            \\vspace{2mm}
            {
                \\extrarowsep=_-1pt^-1pt
                \\begin{tabu}{X[-1r] X[-1l]}
                    \\rowfont{\\scriptsize}
                    \\everyrow{\\rowfont{\\scriptsize}}
                    \\textbf{DIRECCION:} & %s \\\\
                    \\textbf{FONO:}      & %s \\\\
                \\end{tabu}
            }
            \\vspace{0.6cm}
            \\centerline{\\textbf{\\large --- DOCUMENTO PROVEEDOR ---}}
        \\end{center}
        \\vfill
    \\end{minipage}%%%%
    """
    def __init__(self, emitter_name, emitter_activity, emitter_address, emitter_phone):
        self._emitter_name     = emitter_name
        self._emitter_activity = emitter_activity
        self._emitter_address  = emitter_address
        self._emitter_phone    = emitter_phone

    @property
    def carta(self):
        return self.__doc__ % (
            self._emitter_name,
            self._emitter_activity,
            self._emitter_address,
            self._emitter_phone
        )

    @property
    def oficio(self):
        return self.__doc__ % (
            self._emitter_name,
            self._emitter_activity,
            self._emitter_address,
            self._emitter_phone
        )

    @property
    def thermal80mm(self):
        tex = """
           {
            \\scriptsize
            \\tabulinesep=_1.0mm^1.0mm

            \\textbf{RAZON SOCIAL EMISOR:} \\\\
            \\begin{tabu}{@{} X[-1l] X[l] @{}}
                \\textbf{Nombre:}               & %s  \\\\
                \\textbf{Giro:}                 & %s  \\\\
                \\textbf{Direccion:}            & %s  \\\\
                \\textbf{Fono:}                 & %s  \\\\
            \\end{tabu}
            \\centerline{\\textbf{\\large --- DOCUMENTO PROVEEDOR ---}}
            }%%%%
        """
        return tex % (
            self._emitter_name,
            self._emitter_activity,
            self._emitter_address,
            self._emitter_phone
        )
