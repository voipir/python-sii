""" SII Document Patch.

Contains:
    * RUT
    * Document Type Name
    * Document Serial Number
    * SII Branch

    * (thermal*mm only)(optional) Logo (path to EPS)
"""
from .TemplateElement import TemplateElement


class TemplateSiiPatch(TemplateElement):
    """
    \\begin{center}
        \\begin{mdframed}[style=siipatch]
            \\begin{center}
                \\large{\\textbf{%s}}\\break
                \\newline
                \\large{\\textbf{%s}}\\break
                \\newline
                \\large{\\textbf{N\\textdegree %s}}
            \\end{center}
        \\end{mdframed}
        \\vspace{0.5em}
        \\large{\\textbf{S.I.I. - %s}}
        %s
    \\end{center}
    """
    def __init__(self, rut, doc_type, doc_serial, sii_branch,
                       logo_path=''):
        self._rut        = rut
        self._doc_type   = doc_type
        self._doc_serial = doc_serial
        self._sii_branch = sii_branch
        self._logo_path  = logo_path

    @property
    def carta(self):
        return self.__doc__ % (self._rut,
                               self._doc_type, self._doc_serial,
                               self._sii_branch,
                               '')

    @property
    def oficio(self):
        return self.__doc__ % (self._rut,
                               self._doc_type, self._doc_serial,
                               self._sii_branch,
                               '')

    @property
    def thermal80mm(self):
        tex_logo = ''
        if self._logo_path:
            tex_logo += '\\break'
            tex_logo += '\\vspace{0.5em}'
            tex_logo += '\\includegraphics[width=0.7\\textwidth]{%s}' % self._logo_path

        return self.__doc__ % (self._rut,
                               self._doc_type, self._doc_serial,
                               self._sii_branch,
                               tex_logo)
