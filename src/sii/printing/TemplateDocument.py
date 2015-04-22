""" Containing Document Structure
"""
from .TemplateElement import TemplateElement


class TemplateDocument(TemplateElement):

    def __init__(self):
        self.preamble   = None
        self.emitter    = None
        self.sii_patch  = None
        self.receiver   = None
        self.items      = None
        self.payments   = None
        self.totals     = None
        self.references = None
        self.barcode    = None
        self.signature  = None  # Optional
        self.disclaimer = None  # Optional

    @property
    def carta(self):
        tex  = '\\begin{document}'

        # HEAD
        tex += '\\begin{minipage}[t]{0.6\\textwidth}'
        tex += self.emitter.carta
        tex += '\\end{minipage}%'
        tex += '\\begin{minipage}[t]{0.4\\textwidth}'
        tex += '    \\vspace{-2em}'
        tex += self.sii_patch.carta
        tex += '    \\vfill'
        tex += '\\end{minipage}%'
        tex += '\\vspace{2mm}'
        tex += self.receiver.carta

        # ITEMS/PAYMENTS/TOTALS
        tex += '\\begin{mdframed}[style=items]'
        tex += self.items.carta
        tex += '    \\vspace{-3.1em} % Zip them together (suppress spacing)'
        tex += '    \\begin{minipage}[t]{0.7\\textwidth}'
        tex += self.payments.carta
        tex += '    \\end{minipage}%'
        tex += '    \\begin{minipage}[t]{0.3\\textwidth}'
        tex += self.totals.carta
        tex += '    \\end{minipage}'
        tex += '\\end{mdframed}'

        # FEFERENCES
        tex += '\\null'
        tex += '\\vfill'
        tex += '\\begin{mdframed}[style=items]'
        tex += self.references.carta
        tex += '\\end{mdframed}'

        # BARCODE
        tex += '\\begin{minipage}[t]{0.5\\textwidth}'
        tex += '    \\vfill'
        tex += self.barcode.carta
        tex += '\\end{minipage}%'

        # SIGNATURE (§19.983)
        tex += '\\begin{minipage}[t]{0.5\\textwidth}'
        tex += '    \\vfill'
        tex += self.signature.carta
        tex += '\\end{minipage}%'

        # DISCLAIMER
        tex += self.disclaimer.carta

        tex += '\\end{document}'
        return tex

    @property
    def oficio(self):
        tex  = '\\begin{document}'

        tex += '\\begin{minipage}[t]{0.6\\textwidth}'
        tex += self.emitter.oficio
        tex += '\\end{minipage}%'
        tex += '\\begin{minipage}[t]{0.4\\textwidth}'
        tex += '    \\vspace{-2em}'
        tex += self.sii_patch.oficio
        tex += '    \\vfill'
        tex += '\\end{minipage}%'
        tex += '\\vspace{2mm}'
        tex += self.receiver.oficio

        # ITEMS/PAYMENTS/TOTALS
        tex += '\\begin{mdframed}[style=items]'
        tex += self.items.oficio
        tex += '    \\vspace{-3.1em} % Zip them together (suppress spacing)'
        tex += '    \\begin{minipage}[t]{0.7\\textwidth}'
        tex += self.payments.oficio
        tex += '    \\end{minipage}%'
        tex += '    \\begin{minipage}[t]{0.3\\textwidth}'
        tex += self.totals.oficio
        tex += '    \\end{minipage}'
        tex += '\\end{mdframed}'

        # FEFERENCES
        tex += '\\null'
        tex += '\\vfill'
        tex += '\\begin{mdframed}[style=items]'
        tex += self.references.oficio
        tex += '\\end{mdframed}'

        # BARCODE
        tex += '\\begin{minipage}[t]{0.5\\textwidth}'
        tex += '    \\vfill'
        tex += self.barcode.oficio
        tex += '\\end{minipage}%'

        # SIGNATURE (§19.983)
        tex += '\\begin{minipage}[t]{0.5\\textwidth}'
        tex += '    \\vfill'
        tex += self.signature.oficio
        tex += '\\end{minipage}%'

        # DISCLAIMER
        tex += self.disclaimer.oficio

        tex += '\\end{document}'
        return tex

    @property
    def thermal80mm(self):
        tex  = '\\begin{document}'

        tex += self.sii_patch.thermal80mm
        tex += '\\vspace{1mm}'
        tex += '\hrule\hrule\hrule'
        tex += self.emitter.thermal80mm
        tex += '\hrule\hrule\hrule'
        tex += self.receiver.thermal80mm
        tex += '\hrule\hrule\hrule'
        tex += self.items.thermal80mm
        tex += '\hrule\hrule\hrule'
        tex += self.totals.thermal80mm
        tex += '\hrule\hrule\hrule'
        tex += self.payments.thermal80mm
        tex += '\hrule\hrule\hrule'
        tex += self.references.thermal80mm
        tex += '\hrule\hrule\hrule'

        # FOOTER
        tex += self.signature.thermal80mm
        tex += self.barcode.thermal80mm
        tex += self.disclaimer.thermal80mm

        tex += '\\end{document}'
        return tex

    def set_preamble(self, preamble_section):
        self.preamble = preamble_section

    def set_emitter(self, emitter_section):
        self.emitter = emitter_section

    def set_sii_patch(self, sii_patch_section):
        self.sii_patch = sii_patch_section

    def set_receiver(self, receiver_section):
        self.receiver = receiver_section

    def set_items(self, items_section):
        self.items = items_section

    def set_payments(self, payments_section):
        self.payments = payments_section

    def set_totals(self, totals_section):
        self.totals = totals_section

    def set_references(self, references_section):
        self.references = references_section

    def set_barcode(self, barcode_section):
        self.barcode = barcode_section

    def set_signature(self, signature_section):
        self.signature = signature_section

    def set_disclaimer(self, disclaimer_section):
        self.disclaimer = disclaimer_section
