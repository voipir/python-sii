""" Interface for Builders """
from io import StringIO

import xmlsec
from lxml import etree

from ..schema import NodeDocumento
from ..types  import CodigoAutorizacionFolios


class Builder(object):

    def __init__(self, document):
        assert isinstance(document, NodeDocumento), "Must be a DTE Document Node"

        self.document  = document
        self.dte_etree = None

    def __xml__(self):
        return self.dte_etree or self.document.__xml__()

    def sign(self, caf: CodigoAutorizacionFolios):
        """ Signs the Document and adds the Signature to the Document Structure """
        self.caf       = caf
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

    def xml(self):
        return etree.tostring(self.__xml__(), encoding='unicode')

    def pdf(self):
        raise NotImplementedError

    def _build_signature_template(self, dte):
        # Create and insert Signature Template
        signode = xmlsec.template.create(dte, c14n_method=xmlsec.Transform.EXCL_C14N,
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
