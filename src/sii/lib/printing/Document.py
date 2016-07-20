""" Containing Document Structure
"""
from sii.lib.lib import xml

from .TemplateElement import TemplateElement


class Document(TemplateElement):

    def __init__(self, doc_xml, cedible=False):
        self.doc_xml = doc_xml
        self.doc     = None

        # Templating Globals
        self.tex_cedible = cedible

        # Document Globals
        self.doc_type    = None
        self.doc_id      = None

        # 52 - Guia Despacho
        self.doc_gd_type = None

        # TeX Sections
        self.preamble   = None
        self.emitter    = None
        self.sii_patch  = None
        self.receiver   = None
        self.items      = None
        self.payments   = None
        self.totals     = None
        self.references = None
        self.barcode    = None
        self.signature  = None
        self.disclaimer = None

        # Init Hooks
        self.init_docvars()
        self.init_checks()

    def init_docvars(self):
        """ Extract Information, to be used by the individual sections once registered """
        doc = xml.wrap_xml(self.doc_xml)

        self.doc_type = doc.Documento.Encabezado.IdDoc.TipoDTE._int
        self.doc_id   = doc.Documento.Encabezado.IdDoc.Folio._int

        # Guia Despacho Specifics
        if self.doc_type == 52:
            self.doc_gd_type = doc.Documento.Encabezado.IdDoc.IndTraslado._int

    def init_checks(self):
        """ Run Global Assertions """
        if self.tex_cedible:
            if self.doc_type in (56, 61):
                raise AssertionError("NC and ND are not subject to the CEDIBLE template")

            if self.doc_type == 52:
                non_cedibles = (2, 4, 5, 7, 8)

                if self.doc_gd_type in non_cedibles:
                    raise AssertionError("GD of types {0} are not subject to a CEDIBLE template".format(non_cedibles))

    @property
    def resources(self):
        resources = []

        for name, attr in self.__dict__.items():
            if isinstance(attr, TemplateElement):
                section    = getattr(self, name)
                resources += section.resources

        return resources

    @property
    def carta(self):
        self._check()

        tex = self.preamble.carta

        tex += '\n'
        tex += '\n'

        tex += '\\begin{document}\n'

        # HEAD
        tex += '\\begin{minipage}[t]{0.6\\textwidth}\n'
        tex += self.emitter.carta
        tex += '\\end{minipage}%\n'
        tex += '\\begin{minipage}[t]{0.4\\textwidth}\n'
        tex += '    \\vspace{-2em}\n'
        tex += self.sii_patch.carta
        tex += '    \\vfill\n'
        tex += '\\end{minipage}%\n'
        tex += '\\vspace{2mm}\n'
        tex += self.receiver.carta

        # ITEMS
        tex += '\\begin{mdframed}[style=items]\n'
        tex += self.items.carta
        tex += '\\end{mdframed}\n'

        tex += '\\null\n'
        tex += '\\vfill\n'

        # FEFERENCES
        tex += '\\begin{mdframed}[style=references]\n'
        tex += self.references.carta
        tex += '\\end{mdframed}\n'

        # PAYMENTS/TOTALS
        tex += '\\begin{mdframed}[style=summary]\n'
        tex += '    \\vspace{-1em} % Zip them together (suppress spacing)\n'
        tex += '    \\begin{minipage}[t]{0.7\\textwidth}\n'
        tex += self.payments.carta
        tex += '    \\end{minipage}%\n'
        tex += '    \\begin{minipage}[t]{0.3\\textwidth}\n'
        tex += self.totals.carta
        tex += '    \\end{minipage}\n'
        tex += '    \\vspace{-1em} % Zip them together (suppress spacing)\n'
        tex += '\\end{mdframed}\n'

        # BARCODE
        tex += '\\begin{minipage}[t]{0.5\\textwidth}\n'
        tex += '    \\vfill\n'
        tex += self.barcode.carta
        tex += '\\end{minipage}%\n'

        # SIGNATURE (§19.983)
        tex += '\\begin{minipage}[t]{0.5\\textwidth}\n'
        tex += '    \\vfill\n'
        tex += self.signature.carta
        tex += '\\end{minipage}%\n'

        # DISCLAIMER
        tex += self.disclaimer.carta

        tex += '\\end{document}\n'
        return tex

    @property
    def oficio(self):
        self._check()

        tex = self.preamble.oficio

        tex += '\n'
        tex += '\n'

        tex += '\\begin{document}\n'

        # HEAD
        tex += '\\begin{minipage}[t]{0.6\\textwidth}\n'
        tex += self.emitter.oficio
        tex += '\\end{minipage}%\n'
        tex += '\\begin{minipage}[t]{0.4\\textwidth}\n'
        tex += '    \\vspace{-2em}\n'
        tex += self.sii_patch.oficio
        tex += '    \\vfill\n'
        tex += '\\end{minipage}%\n'
        tex += '\\vspace{2mm}\n'
        tex += self.receiver.oficio

        # ITEMS
        tex += '\\begin{mdframed}[style=items]\n'
        tex += self.items.oficio
        tex += '\\end{mdframed}\n'

        tex += '\\null\n'
        tex += '\\vfill\n'

        # FEFERENCES
        tex += '\\begin{mdframed}[style=references]\n'
        tex += self.references.oficio
        tex += '\\end{mdframed}\n'

        # PAYMENTS/TOTALS
        tex += '\\begin{mdframed}[style=summary]\n'
        tex += '    \\vspace{-1em} % Zip them together (suppress spacing)\n'
        tex += '    \\begin{minipage}[t]{0.7\\textwidth}\n'
        tex += self.payments.oficio
        tex += '    \\end{minipage}%\n'
        tex += '    \\begin{minipage}[t]{0.3\\textwidth}\n'
        tex += self.totals.oficio
        tex += '    \\end{minipage}\n'
        tex += '    \\vspace{-1em} % Zip them together (suppress spacing)\n'
        tex += '\\end{mdframed}\n'

        # BARCODE
        tex += '\\begin{minipage}[t]{0.5\\textwidth}\n'
        tex += '    \\vfill\n'
        tex += self.barcode.oficio
        tex += '\\end{minipage}%\n'

        # SIGNATURE (§19.983)
        tex += '\\begin{minipage}[t]{0.5\\textwidth}\n'
        tex += '    \\vfill\n'
        tex += self.signature.oficio
        tex += '\\end{minipage}%\n'

        # DISCLAIMER
        tex += self.disclaimer.oficio

        tex += '\\end{document}\n'
        return tex

    @property
    def thermal80mm(self):
        self._check()

        tex = self.preamble.thermal80mm

        tex += '\n'
        tex += '\n'

        tex += '\\begin{document}\n'

        tex += self.sii_patch.thermal80mm
        tex += '\\vspace{1mm}\n'
        tex += '\hrule\hrule\hrule\n'
        tex += self.emitter.thermal80mm
        tex += '\hrule\hrule\hrule\n'
        tex += self.receiver.thermal80mm
        tex += '\hrule\hrule\hrule\n'
        tex += self.items.thermal80mm
        tex += '\hrule\hrule\hrule\n'
        tex += self.totals.thermal80mm
        tex += '\hrule\hrule\hrule\n'
        tex += self.payments.thermal80mm
        tex += '\hrule\hrule\hrule\n'
        tex += self.references.thermal80mm
        tex += '\hrule\hrule\hrule\n'

        # FOOTER
        tex += self.signature.thermal80mm
        tex += self.barcode.thermal80mm
        tex += self.disclaimer.thermal80mm

        tex += '\\end{document}\n'
        return tex

    def set_preamble(self, preamble_section):
        self.preamble                 = preamble_section
        preamble_section.__document__ = self

    def set_emitter(self, emitter_section):
        self.emitter                 = emitter_section
        emitter_section.__document__ = self

    def set_sii_patch(self, sii_patch_section):
        self.sii_patch                 = sii_patch_section
        sii_patch_section.__document__ = self

    def set_receiver(self, receiver_section):
        self.receiver                 = receiver_section
        receiver_section.__document__ = self

    def set_items(self, items_section):
        self.items                 = items_section
        items_section.__document__ = self

    def set_payments(self, payments_section):
        self.payments                 = payments_section
        payments_section.__document__ = self

    def set_totals(self, totals_section):
        self.totals                 = totals_section
        totals_section.__document__ = self

    def set_references(self, references_section):
        self.references                 = references_section
        references_section.__document__ = self

    def set_barcode(self, barcode_section):
        self.barcode                 = barcode_section
        barcode_section.__document__ = self

    def set_signature(self, signature_section):
        self.signature                 = signature_section
        signature_section.__document__ = self

    def set_disclaimer(self, disclaimer_section):
        self.disclaimer                 = disclaimer_section
        disclaimer_section.__document__ = self

    def _check(self):
        errmsg = ""

        if not self.preamble:
            errmsg = "Missing 'Preamble' Section"

        if not self.emitter:
            errmsg = "Missing 'Emitter' Section"

        if not self.sii_patch:
            errmsg = "Missing 'Sii Patch' Section"

        if not self.receiver:
            errmsg = "Missing 'Receiver' Section"

        if not self.items:
            errmsg = "Missing 'Items' Section"

        if not self.payments:
            errmsg = "Missing 'Payments' Section"

        if not self.totals:
            errmsg = "Missing 'Totals' Section"

        if not self.references:
            errmsg = "Missing 'References' Section"

        if not self.barcode:
            errmsg = "Missing 'Barcode' Section"

        if not self.signature:
            errmsg = "Missing 'Signature' Section"

        if not self.disclaimer:
            errmsg = "Missing 'Disclaimer' Section"

        if errmsg:
            raise ValueError("Cannot create Template: " + errmsg)
