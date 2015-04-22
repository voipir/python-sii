""" Builder for Factura de Liquidacion Electronica.
"""
from lxml.etree import tostring

from .Builder import Builder
from ..schema   import NodeDocumento


__all__ = ['SiiLiquidacionFactura']


class SiiLiquidacionFactura(Builder):
    def __init__(self, document, cert=None):
        assert isinstance(document, NodeDocumento), "Must be a DTE Document Node"

        self.document = document
        self.cert     = cert

    def __xml__(self):
        return self.document.__xml__()

    @property
    def certificate(self):
        if not self.cert:
            raise RuntimeError("No Certificate set for given Document; please set one with "
                               "`set_certificate` first")
        else:
            return self.cert

    def set_certificate(self, cert):
        self.cert = cert

    def xml(self):
        return tostring(self.__xml__()).decode('utf8')

    def pdf(self):
        raise NotImplementedError
