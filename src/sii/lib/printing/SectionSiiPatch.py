# -*- coding: utf-8 -*-
""" SII Document Patch.

Contains:
    * RUT
    * Document Type Name
    * Document Serial Number
    * SII Branch

    * (thermal*mm only)(optional) Logo (path to EPS)
"""
from .TemplateElement import TemplateElement, Resource


DOC_TYPE_STRINGS = {
    33:  "FACTURA\\break ELECTRÓNICA",
    34:  "FACTURA\\break NO AFECTA O EXENTA\\break ELECTRÓNICA",
    52:  "GUÍA DE DESPACHO\\break ELECTRÓNICA",
    56:  "NOTA DE DÉBITO\\break ELECTRÓNICA",
    61:  "NOTA DE CRÉDITO\\break ELECTRÓNICA",
    46:  "FACTURA DE COMPRA\\break ELECTRÓNICA",
    43:  "LIQUIDACIÓN FACTURA\\break ELECTRÓNICA",
    110: "FACTURA\\break DE EXPORTACIÓN\\break ELECTRÓNICA",
    111: "NOTA DE DÉBITO\\break DE EXPORTACIÓN\\break ELECTRÓNICA",
    112: "NOTA DE CRÉDITO\\break DE EXPORTACIÓN\\break ELECTRÓNICA"
}


class SectionSiiPatch(TemplateElement):
    """
    %% -----------------------------------------------------------------
    %% SECTION - Sii Patch
    %% -----------------------------------------------------------------
    \\begin{center}
        \\begin{mdframed}[style=siipatch]
            \\begin{center}
                \\large{\\textbf{R.U.T.: %s}}\\break
                \\newline
                \\large{\\textbf{%s}}\\break
                \\newline
                \\large{\\textbf{N\\textdegree\\ %s}}
            \\end{center}
        \\end{mdframed}
        \\vspace{0.5em}
        \\large{\\textbf{S.I.I. - %s}}
        %s
    \\end{center}
    """
    def __init__(self, rut, dte_type, dte_serial, sii_branch, logo_path=''):
        self._rut          = rut
        self._dte_type     = dte_type
        self._dte_type_str = DOC_TYPE_STRINGS[dte_type]
        self._dte_serial   = dte_serial
        self._sii_branch   = sii_branch

        self._logo_path = logo_path
        if self._logo_path:
            with open(self._logo_path, 'r') as fh:
                self._logo_data = fh.read()

    @property
    def resources(self):
        ress = []

        if self._logo_path:
            ress.append(Resource('logo.eps', self._logo_data))

        return ress

    @property
    def carta(self):
        return self.__doc__ % (
            self._rut,
            self._dte_type_str,
            self._dte_serial,
            self._sii_branch,
            ''
        )

    @property
    def oficio(self):
        return self.__doc__ % (
            self._rut,
            self._dte_type_str,
            self._dte_serial,
            self._sii_branch,
            ''
        )

    @property
    def thermal80mm(self):
        tex_logo = ''
        if self._logo_path:
            tex_logo += '\\break'
            tex_logo += '\\vspace{0.5em}'
            tex_logo += '\\includegraphics[width=0.7\\textwidth]{logo.eps}'

        return self.__doc__ % (
            self._rut,
            self._dte_type_str,
            self._dte_serial,
            self._sii_branch,
            tex_logo
        )
