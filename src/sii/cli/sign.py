""" Utilities related with SII Document Signature.
"""
from sii import CodigoAutorizacionFolios, Builder


def sign_document(args, doc):
    caf = CodigoAutorizacionFolios.from_file(args['--sign'])

    builder = Builder(doc)
    builder.sign(caf)

    return builder
