""" Common Local Utilities.
"""
import re
import io

from lxml import etree

__all__ = [
    'prepend_dtd',
    'extract_signode',
    'extract_signodes',
    'extract_signode_reference',
    'extract_signode_certificate'
]

DTD_PREAMBLE = """
<!DOCTYPE {root} [
    <!ATTLIST Documento       ID ID #IMPLIED>
    <!ATTLIST SetDTE          ID ID #IMPLIED>
    <!ATTLIST EnvioLibro      ID ID #IMPLIED>
    <!ATTLIST Resultado       ID ID #IMPLIED>
    <!ATTLIST SetRecibos      ID ID #IMPLIED>
    <!ATTLIST DocumentoRecibo ID ID #IMPLIED>
]>
"""


def prepend_dtd(xml):
    """ Prepends a DTD providing a definition of a to a non-standard xml:id pointer. Necessary for
    signature and signature verification.

    :param `etree.Element` xml: XML tree to prepend the DTD to.

    :param str sig_tag:   Tag name to contain the URI.
    :param str uri_attr:  Attribute name to contain the URI.

    :return: An `etree.Element` with the now DTD contextualized XML.
    """
    root = None
    if hasattr(xml, 'getroot'):
        root = xml.getroot()
    else:
        root = xml.getroottree().getroot()

    tag      = re.sub('\{.*\}', '', root.tag)
    preamble = DTD_PREAMBLE.format(root=tag)

    buff = io.BytesIO()
    buff.write(bytes(preamble, 'utf8'))
    buff.write(etree.tostring(xml, pretty_print=True, method='xml'))
    buff.seek(0)

    tree = etree.parse(buff)
    root = tree.getroot()

    return root


def extract_signode(xml):
    """ Extracts the <ds:Signature> node from right under the root node in an XML document. If none
    is found there, an RuntimeException gets risen.

    :param `etree.Element` xml: Root node of the document.

    :return: `etree.Element` of the <ds:Signature>
    """
    signode = xml.find('{http://www.w3.org/2000/09/xmldsig#}Signature')

    if signode is None:
        raise ValueError("Did not find a '{http://www.w3.org/2000/09/xmldsig#}Signature' under the root node")

    return signode


def extract_signodes(xml):
    """ Extracts all <ds:Signature> nodes from given XML.

    :param `etree.Element` xml: Root node of the document.

    :return: list of `etree.Element` of the <ds:Signature>'s
    """
    signodes = xml.xpath('//ds:Signature', namespaces={'ds': 'http://www.w3.org/2000/09/xmldsig#'})
    return signodes


def extract_signode_reference(signode):
    """ Extracts the <ds:Reference> of a <ds:Signature> node.

    :param `etree.Element` xml: Root node of the document.

    :return: `etree.Element` of the <ds:Reference>
    """
    refs = signode.xpath('.//ds:Reference', namespaces={'ds': 'http://www.w3.org/2000/09/xmldsig#'})

    if len(refs) != 1:
        raise ValueError("Could not find x509 reference on this signode")
    else:
        return refs[0]


def extract_signode_certificate(signode):
    """ Extract the x509 Certificate Information from a <ds:Signature>.

    Raises exception if it does not find any <X509Certificate> information in the <Signature>.

    :param `etree.Element` signode: Root node of the document.

    :return: UTF8 encoded string containing the base64 encoded PEM certificate in it.
    """
    cert_node = signode.find('.//{http://www.w3.org/2000/09/xmldsig#}X509Certificate')
    cert_text = ''

    if cert_node is None:
        raise ValueError("Could not find x509 certificate on this signode")
    else:
        cert_text = cert_node.text

    buff  = '-----BEGIN CERTIFICATE-----\n'
    buff += cert_text.strip('\n')
    buff += '\n-----END CERTIFICATE-----\n'

    return buff
