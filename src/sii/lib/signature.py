""" SII Document Signing Process Functions
"""
import xmlsec

from .helpers import prepend_dtd, extract_signode, extract_signodes

__all__ = [
    'sign_document',
    'sign_document_all',
    'build_template'
]


def sign_document(xml, key_path, cert_path):
    """ Signs topmost XML <ds:Signature> node under the document root node.

    :param `etree.Element` xml: The XML to be signed.

    :param str key_path:  Path to PEM key file.
    :param str cert_path: Path to PEM certificate file.

    :return: `etree.Element` to the signed document. Should be the same with the provided xml param.
    """
    # HACK inject a DTD preamble in to direct non-standard xml:id
    # resolution for <Reference URI = "#XXXX">.
    xml = prepend_dtd(xml)

    signode = extract_signode(xml)

    # Load Private Key and Public Certificate
    key = xmlsec.Key.from_file(key_path, xmlsec.KeyFormat.PEM)
    key.load_cert_from_file(cert_path, xmlsec.KeyFormat.PEM)

    # Create Crypto Context and load in Key/Cert
    ctx     = xmlsec.SignatureContext()
    ctx.key = key

    ctx.sign(signode)

    return xml


def sign_document_all(xml, key_path, cert_path):
    """ Signs all XML's <ds:Signature> nodes under the document root node.

    :param `etree.Element` xml: The XML to be signed.

    :param str key_path:  Path to PEM key file.
    :param str cert_path: Path to PEM certificate file.

    :return: `etree.Element` to the signed document. Should be the same with the provided xml param.

    TODO: make sure we get all <ds:Signature> nodes in depth first order, otherwise we would break envolving
    signatures. Its not that it is not currently working, it is just without guaranteed order.
    """
    # HACK inject a DTD preamble in to direct non-standard xml:id
    # resolution for <Reference URI = "#XXXX">.
    xml = prepend_dtd(xml)

    for signode in extract_signodes(xml):
        # Load Private Key and Public Certificate
        key = xmlsec.Key.from_file(key_path, xmlsec.KeyFormat.PEM)
        key.load_cert_from_file(cert_path, xmlsec.KeyFormat.PEM)

        # Create Crypto Context and load in Key/Cert
        ctx     = xmlsec.SignatureContext()
        ctx.key = key

        ctx.sign(signode)

    return xml


def build_template(xml, sig_uri):
    """ Build a enveloped <ds:Signature> template on the provided xml, with a reference
    to sig_uri for signature.

    :param etree.Element xml:     XML to add the signature node to.
    :param str           sig_uri: The URI to use for the <Reference> which points to the node that will digested at
                                  signature-time.

    :return: Returns an `etree.Element` with the <Signature> template node, ready for signing.
    """
    # Create and insert Signature Template
    signode = xmlsec.template.create(
        xml,
        c14n_method=xmlsec.Transform.C14N,
        sign_method=xmlsec.Transform.RSA_SHA1
    )

    # Add the <ds:Reference/> node to the signature template.
    refnode = xmlsec.template.add_reference(
        signode,
        digest_method = xmlsec.Transform.SHA1,
        uri           = sig_uri
    )

    # Add the enveloped transform descriptor.
    xmlsec.template.add_transform(refnode, transform=xmlsec.Transform.ENVELOPED)

    # Add Key Value Info and x509 Data
    key_info = xmlsec.template.ensure_key_info(signode)

    xmlsec.template.add_key_value(key_info)
    xmlsec.template.add_x509_data(key_info)

    return signode
