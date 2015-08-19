""" Prints Document Nodes.
"""
import os
import tempfile

from sii.system import PdfLaTeX

from .TemplateDocument   import TemplateDocument
from .TemplatePreamble   import TemplatePreamble
from .TemplateEmitter    import TemplateEmitter
from .TemplateSiiPatch   import TemplateSiiPatch
from .TemplateReceiver   import TemplateReceiver
from .TemplateItems      import TemplateItems
from .TemplatePayments   import TemplatePayments
from .TemplateTotals     import TemplateTotals
from .TemplateReferences import TemplateReferences
from .TemplateBarcode    import TemplateBarcode
from .TemplateSignature  import TemplateSignature
from .TemplateDisclaimer import TemplateDisclaimer


class DocumentPrinter(object):

    def __init__(self, medium, logo_path=''):
        """
        :param medium: Medium to generate PDF for; "carta", "oficio" or "thermal80mm"
        """
        assert medium in ('carta', 'oficio', 'thermal80mm')  # Currently supported types
        self.medium = medium

        self.logo_path = logo_path

        self.printers = {
            33: self.print_factura_venta,   # Factura Electronica,
            34: self.print_factura_exenta,  # Factura Electronica de Venta de Bienes y Servicios
                                            # No afectos o Exento de IVA.
            46: self.print_factura_compra,  # Factura de Compra Electronica
            52: self.print_guia_despacho,   # Guia de Despacho Electronica
            56: self.print_nota_debito,     # Nota de Debito Electronica
            61: self.print_nota_credito     # Nota de Credito Electronica
        }

    def print_dte(self, document):
        """ Prints whatever needs printing based on DTE Type """
        return self.printers[document.Encabezado.IdDoc.TipoDTE](document)

    def print_factura_venta(self, factura_venta):
        """ FACTURA ELECTRÓNICA """
        template = self._build_dte_template(factura_venta)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_factura_exenta(self, factura_exenta):
        """ FACTURA NO AFECTA O EXENTA ELECTRÓNICA """
        template = self._build_dte_template(factura_exenta)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_factura_compra(self, factura_compra):
        """ FACTURA DE COMPRA ELECTRÓNICA """
        template = self._build_dte_template(factura_compra)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_liquidacion_factura(self, liquidacion_factura):
        """ LIQUIDACIÓN FACTURA ELECTRÓNICA """
        template = self._build_dte_template(liquidacion_factura)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_factura_exportacion(self, factura_exportacion):
        """ FACTURA DE EXPORTACIÓN ELECTRÓNICA """
        template = self._build_dte_template(factura_exportacion)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_documento_boleta(self, documento_boleta):
        """ BOLETA """
        template = self._build_dte_template(documento_boleta)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_guia_despacho(self, guia_despacho):
        """G UÍA DE DESPACHO ELECTRÓNICA """
        template = self._build_dte_template(guia_despacho)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_nota_debito(self, nota_debito):
        """ NOTA DE DÉBITO ELECTRÓNICA """
        template = self._build_dte_template(nota_debito)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_nota_debito_exportacion(self, nota_debito_exportacion):
        """ NOTA DE DÉBITO DE EXPORTACIÓN ELECTRÓNICA """
        template = self._build_dte_template(nota_debito_exportacion)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_nota_credito(self, nota_credito):
        """ NOTA DE CRÉDITO ELECTRÓNICA """
        template = self._build_dte_template(nota_credito)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def print_nota_credito_exportacion(self, nota_credito_exportacion):
        """ NOTA DE CRÉDITO DE EXPORTACIÓN ELECTRÓNICA """
        template = self._build_dte_template(nota_credito_exportacion)
        tex      = getattr(template, self.medium)
        pdf      = self._pdf_from_tex(tex)

        return pdf

    def _build_dte_template(self, document):
        template = TemplateDocument()

        template.preamble   = TemplatePreamble()
        template.emitter    = TemplateEmitter(
            emitter_name_long   = None,
            emitter_name_short  = None,
            emitter_activity    = None,
            emitter_hq_addr     = None,
            emitter_branch_addr = None,
            order_number        = None,
            emitter_salesman    = None,
            licence_plate       = None,
            logo_path           = self.logo_path
        )
        template.sii_patch  = TemplateSiiPatch(
            rut                 = None,
            doc_type            = None,
            doc_serial          = None,
            sii_branch          = None,
            logo_path           = ''
        )
        template.receiver   = TemplateReceiver(
            emission_date       = None,
            expiration_date     = None,
            receivername        = None,
            receiverrut         = None,
            receiveraddress     = None,
            receivercomune      = None,
            receiveractivity    = None,
            receivercity        = None,
            emittersalesman     = '',
            ordernumber         = '',
            licenceplate        = ''
        )
        template.items      = TemplateItems(
            column_layout       = None,
            table_margins       = False,
            amount_unit         = 'Kg'
        )
        template.payments   = TemplatePayments(
            table_margins       =False
        )
        template.totals     = TemplateTotals(
            discount            = None,
            net_value           = None,
            exempt_value        = None,
            tax                 = None,
            total               = None
            # **kwargs
        )
        template.references = TemplateReferences(
            doc_type            = None,
            doc_serial          = None,
            doc_date            = None,
            reason              = None
        )
        template.barcode    = TemplateBarcode(
            data                = None,
            resolution_number   = None,
            resolution_datestr  = None
        )
        template.signature  = TemplateSignature()
        template.disclaimer = TemplateDisclaimer()

        return template

    def _pdf_from_tex(self, tex):
        pdflatex = PdfLaTeX()
        pdflatex.check(fail=True)

        tmp       = tempfile.TemporaryDirectory()
        tex_fname = os.path.join(tmp.name, '.tex')
        pdf_fname = os.path.join(tmp.name, '.pdf')
        result    = None

        with open(tex_fname, 'w') as fh:
            fh.write(self.ps)

        converter = PdfLaTeX()
        converter.call(tex_fname)

        with open(pdf_fname, 'r') as fh:
            result = fh.read()

        tmp.cleanup()
        return result
