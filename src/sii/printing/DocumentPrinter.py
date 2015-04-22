""" Prints Document Nodes.
"""
from .TemplatePreamble   import TemplatePreamble
from .TemplateEmitter    import TemplateEmitter
from .TemplateSiiPatch   import TemplateSiiPatch
from .TemplateReceiver   import TemplateReceiver
from .TemplateItems      import TemplateItems
from .TemplateReferences import TemplateReferences
from .TemplateBarcode    import TemplateBarcode
from .TemplateSignature  import TemplateSignature
from .TemplateDisclaimer import TemplateDisclaimer


class DocumentPrinter(object):

    def __init__(self, medium):
        """
        :param medium: Medium to generate PDF for; "carta", "oficio" or "thermal80mm"
        """
        assert medium in ('carta', 'oficio', 'thermal80mm')  # Currently supported types
        self.medium = medium

    def print_factura_venta(self, factura_venta_etree):
        """ FACTURA ELECTRÓNICA """
        raise NotImplementedError

    def print_factura_exenta(self, factura_exenta_etree):
        """ FACTURA NO AFECTA O EXENTA ELECTRÓNICA """
        raise NotImplementedError

    def print_factura_compra(self, factura_compra_etree):
        """ FACTURA DE COMPRA ELECTRÓNICA """
        raise NotImplementedError

    def print_liquidacion_factura(self, liquidacion_factura_etree):
        """ LIQUIDACIÓN FACTURA ELECTRÓNICA """
        raise NotImplementedError

    def print_factura_exportacion(self, factura_exportacion_etree):
        """ FACTURA DE EXPORTACIÓN ELECTRÓNICA """
        raise NotImplementedError

    def print_documento_boleta(self, documento_boleta_etree):
        raise NotImplementedError

    def print_guia_despacho(self, guia_despacho_etree):
        """G UÍA DE DESPACHO ELECTRÓNICA """
        raise NotImplementedError

    def print_nota_debito(self, nota_debito_etree):
        """ NOTA DE DÉBITO ELECTRÓNICA """
        raise NotImplementedError

    def print_nota_debito_exportacion(self, nota_debito_exportacion_etree):
        """ NOTA DE DÉBITO DE EXPORTACIÓN ELECTRÓNICA """
        raise NotImplementedError

    def print_nota_credito(self, nota_credito_etree):
        """ NOTA DE CRÉDITO ELECTRÓNICA """
        raise NotImplementedError

    def print_nota_credito_exportacion(self, nota_credito_exportacion_etree):
        """ NOTA DE CRÉDITO DE EXPORTACIÓN ELECTRÓNICA """
        raise NotImplementedError
