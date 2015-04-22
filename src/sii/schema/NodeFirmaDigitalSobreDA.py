""" SII x509 RSA Signature of the  """
from .xml import XMLNode


class NodeFirmaDigitalSobreDA(XMLNode):
    """ Firma Digital (RSA) del SII Sobre DA.

    """
    __attributes__ = {'algoritmo': 'SHA1withRSA'}

    # TODO... here probably goes the base64 binary encoded Signature
