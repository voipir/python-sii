""" Interface for Builders
"""
from io               import StringIO
from base64           import b64encode
from datetime         import datetime
from xml.sax.saxutils import escape as xml_escape

import xmlsec
from lxml             import etree
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash      import SHA as SHA1
from Crypto.PublicKey import RSA

from ..schema   import NodeDocumento, NodeDTE
from ..types    import CodigoAutorizacionFolios
from ..printing import DocumentPrinter


class Builder(object):

    def __init__(self, document: NodeDocumento):
        assert isinstance(document, NodeDocumento), "Must be a DTE.Document Node"

        self.document  = document
        self._dte      = None
        self.dte_etree = None

        self._build_dte()

    @property
    def dte(self):
        return self._dte

    @property
    def xml(self):
        return etree.tostring(self.__xml__(), encoding='unicode')

    @property
    def pdf(self, medium):
        printer = DocumentPrinter(medium)
        return printer.print_dte(self._document)  # -> pdf

    def __xml__(self):
        return self.dte_etree if self.dte_etree is not None else self.document.__xml__()

    def sign(self, caf: CodigoAutorizacionFolios):
        """ Signs the Document and adds the Signature to the Document Structure """
        assert isinstance(caf, CodigoAutorizacionFolios), "Must be a Codigo Autorizacion de Folios"

        self._verify_caf_vs_document_type(caf, self.document)
        self._generate_timbre_electronico(caf, self.document)

        self.dte_etree = etree.Element('DTE')
        self.dte_etree.append(self.document.__xml__())

        signode = self._build_signature_template(self.dte_etree)
        self.dte_etree.append(signode)

        # Load Key and Certificate
        key_io  = StringIO(caf.private_key)
        # cert_io = StringIO(caf.public_key)

        key = xmlsec.Key.from_memory(key_io, xmlsec.KeyFormat.PEM)
        # key.load_cert_from_memory(cert_io, xmlsec.KeyFormat.PEM)

        # Create Crypto Context and sign Signature Node
        ctx = xmlsec.SignatureContext()
        ctx.key = key
        ctx.sign(signode)

        self._dte.Document  = self.document
        self._dte.Signature = etree.tostring(signode, encoding='unicode')

    def _build_dte(self):
        self._dte = NodeDTE()
        self._dte.Documento = self.document

    def _verify_caf_vs_document_type(self, caf, document):
        doc_type = self.document.Encabezado.IdDoc.TipoDTE
        if doc_type != caf.doc_type:
            raise ValueError("You are trying to sign a document of type: {0} with a CAF for "
                             "doc type {1}".format(doc_type, caf.doc_type))
        # TODO verify document id within caf signature interval

    def _generate_timbre_electronico(self, caf, document):
        document.__check__()

        document.TED.DD.RE    = document.Encabezado.Emisor.RUTEmisor
        document.TED.DD.TD    = document.Encabezado.IdDoc.TipoDTE
        document.TED.DD.FE    = datetime.strptime(document.Encabezado.IdDoc.FchEmis, '%Y-%m-%d').date()
        document.TED.DD.F     = document.Encabezado.IdDoc.Folio
        document.TED.DD.RR    = document.Encabezado.Receptor.RUTRecep
        document.TED.DD.RSR   = document.Encabezado.Receptor.RznSocRecep[:40]  # FIXME assignment does not boundary check properly?
        document.TED.DD.MNT   = sum([item.MontoItem for item in document.Detalle])
        document.TED.DD.IT1   = document.Detalle[0].NmbItem
        document.TED.DD.CAF   = caf.__xml__()
        document.TED.DD.TSTED = datetime.now()

        document.TED.FRMT = self._build_digital_stamp_digest(caf, document)

    def _build_digital_stamp_digest(self, caf, document):
        string    = xml_escape(etree.tostring(document.TED.DD.__xml__(), encoding='unicode'))
        bytstring = bytes(string, 'utf8')
        hash      = SHA1.new(bytstring)

        key       = RSA.importKey(caf.private_key)
        signer    = PKCS1_v1_5.new(key)
        signature = signer.sign(hash)

        return str(b64encode(signature), 'utf8')

    def _build_signature_template(self, document):
        # Create and insert Signature Template
        signode = xmlsec.template.create(document, c14n_method=xmlsec.Transform.EXCL_C14N,
                                                   sign_method=xmlsec.Transform.RSA_SHA1)

        # Add the <ds:Reference/> node to the signature template.
        doc_type  = self.document.Encabezado.IdDoc.TipoDTE
        doc_id    = self.document.Encabezado.IdDoc.Folio
        target_id = "F{folio}T{type}".format(folio=doc_id, type=doc_type)

        ref = xmlsec.template.add_reference(signode, digest_method=xmlsec.Transform.SHA1,
                                                     id=target_id)

        # Add the enveloped transform descriptor.
        xmlsec.template.add_transform(ref, transform=xmlsec.Transform.ENVELOPED)

        # Add Key Value Info and x509 Data
        key_info = xmlsec.template.ensure_key_info(signode)
        xmlsec.template.add_key_value(key_info)
        xmlsec.template.add_x509_data(key_info)

        return signode
