# -*- coding: utf-8 -*-
""" Signature Section of the Document

Contains:
    * Form for
"""
from .TemplateElement import TemplateElement


class SectionSignature(TemplateElement):
    """
    %% -----------------------------------------------------------------
    %% SECTION - Signature
    %% -----------------------------------------------------------------
    \\begin{mdframed}[style=signature]
        \\begin{spacing}{1.5}
            \\%s{
                Nombre:{\\leaders\\hbox{\\rule{1mm}{0.8pt}}\\hfill}  \\\\
                RUT:{\\leaders\\hbox{\\rule{1mm}{0.8pt}}\\hfill}
                FECHA:{\\leaders\\hbox{\\rule{1mm}{0.8pt}}\\hfill}   \\\\
                Recinto:{\\leaders\\hbox{\\rule{1mm}{0.8pt}}\\hfill}
                FIRMA:{\\leaders\\hbox{\\rule{1mm}{0.8pt}}\\hfill}
            }
        \\end{spacing}%%%%
        %%%%
        \\tiny{
            El acuse de recibo que se declara en este acto, de acuerdo a lo
            dispuesto en la letra b) del Art. 4° y la letra c) del Art. 5° de la
            Ley 19.983, acredita que la entrega de mercadería(s) o servicio(s)
            prestado(s) ha(n) sido recibido(s).
        }
    \\end{mdframed}
    \\vspace{0.5em}
    %s
    """
    @property
    def carta(self):
        return self._template('small')

    @property
    def oficio(self):
        return self._template('small')

    @property
    def thermal80mm(self):
        return self._template('scriptsize')

    def _template(self, size):
        assert self.__document__, "Have not been yet registered onto a Document"

        if self.__document__.tex_cedible:
            if self.__document__.doc_type == 52:
                cedible = "CEDIBLE CON SU FACTURA"
            else:
                cedible = "CEDIBLE"

            return self.__doc__ % (size, "\\raggedleft{\\textbf{%s}}" % cedible)
        else:
            return ""
