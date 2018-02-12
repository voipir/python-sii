# -*- coding: utf-8 -*-
""" SII Document Signature Verification Process Functions
"""
from io   import BytesIO
from copy import deepcopy
import tempfile

import xmlsec
from lxml import etree

from .schemas import resolve_schema
from .helpers import (
    prepend_dtd,
    extract_signodes,
    extract_signode_certificate,
    extract_signode_reference,
)

__all__ = [
    'validate_signatures',
    'validate_schema'
]


def validate_signatures(xml):
    """ Validate internal Document Signatures. Public Key are provided by them, so no need for
    anything else than the XML itself.

    :param `etree.Element` xml: Element to the rootnode of the document.

    :return: [tuple(URI, True | False), ...]
    """
    xml = prepend_dtd(xml)

    signodes = extract_signodes(xml)
    results  = []
    for signode in signodes:
        cert = extract_signode_certificate(signode)
        ref  = extract_signode_reference(signode)

        # Load Public Key
        key_mgr = xmlsec.KeysManager()
        with tempfile.NamedTemporaryFile(mode='wb', buffering=0) as tmpf:
            tmpf.write(bytes(cert, 'utf8'))

            key_mgr.load_cert(tmpf.name, xmlsec.KeyFormat.PEM, xmlsec.KeyDataType.TRUSTED)

        # Verify the Document
        ctx = xmlsec.SignatureContext(key_mgr)

        try:
            ctx.verify(signode)
        except xmlsec.error.Error:
            validity = (ref.attrib['URI'], False)
        else:
            validity = (ref.attrib['URI'], True)

        results.append(validity)

    return results


def validate_schema(doc_xml, schema_xml=None):
    """ Validate XML against its XSD Schema definition provided by the SII.

    :param `lxml.etree.Element` doc_xml: Handle to XML etree root node.
    """
    doc_xml = deepcopy(doc_xml)

    doc_new    = etree.Element(doc_xml.tag, nsmap={None: 'http://www.sii.cl/SiiDte'})
    doc_new[:] = doc_xml[:]                # move children into new root
    doc_new.attrib.update(doc_xml.attrib)  # copy attributes of the root node

    # reload xml
    buff = BytesIO(etree.tostring(doc_new, method='c14n'))
    xml  = etree.parse(buff).getroot()

    if not schema_xml:
        schema_pth = resolve_schema(doc_xml)

        with open(schema_pth, 'rb') as fh:
            schema_xml = etree.parse(fh)

    schema = etree.XMLSchema(schema_xml)
    schema.assertValid(xml)

    return True  # if no assertion gets thrown above, we can safely assume a `True` validity.
