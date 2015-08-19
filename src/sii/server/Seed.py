""" Authentication Seed to request Token.

"""
import re

from suds.client import Client
from lxml        import etree

# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds').setLevel(logging.DEBUG)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)  # MUST BE THIS?
# logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
# logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
# logging.getLogger('suds.resolver').setLevel(logging.DEBUG)
# logging.getLogger('suds.xsd.query').setLevel(logging.DEBUG)
# logging.getLogger('suds.xsd.basic').setLevel(logging.DEBUG)
# logging.getLogger('suds.binding.marshaller').setLevel(logging.DEBUG)


__all__ = ['Seed',
           'SeedDummy']


class Seed(object):

    SOAP_URL_PRODUCTION    = "https://palena.sii.cl/DTEWS/CrSeed.jws?wsdl"
    SOAP_URL_CERTIFICATION = "https://maullin.sii.cl/DTEWS/CrSeed.jws?wsdl"

    SEED_OK         = 0
    SEED_LINE_ERR   = -1
    SEED_RETURN_ERR = -2

    def __init__(self, cert_env=True):
        """
        :param cert_env: If you are in the process of certification (SII Ambiente de Certificacion)
        """
        if cert_env:
            self.sii_host = self.SOAP_URL_CERTIFICATION
        else:
            self.sii_host = self.SOAP_URL_PRODUCTION

        self.sii_soap = Client(self.sii_host)
        self.sii_soap.set_options(location=self.sii_host)

        self._status = None
        self._seed   = None
        self._msg    = None

        self._seed_xml    = self._fetch_seed()
        self._seed_etree  = self._prepare_seed_xml(self._seed_xml)
        self._seed_values = self._parse_seed_xml(self._seed_etree)

    def _fetch_seed(self):
        return self.sii_soap.service.getSeed()

    def _prepare_seed_xml(self, seed_xml):
        clean_xml   = re.sub(r'>\s+<', '><', seed_xml)
        encoded_xml = clean_xml.encode('utf8')
        etree_xml   = etree.fromstring(encoded_xml)
        return etree_xml

    def _parse_seed_xml(self, seed_etree):
        status = seed_etree.xpath('//ESTADO/text()')
        seed   = seed_etree.xpath('//SEMILLA/text()')
        msg    = seed_etree.xpath('//GLOSA/text()')

        self._status = int(status[0]) if status else None
        self._seed   = seed[0]        if seed   else None
        self._msg    = msg[0]         if msg    else None

    @property
    def status(self):
        return self._status

    @property
    def seed(self):
        return str(int(self._seed))

    @property
    def message(self):
        return self._msg


class SeedDummy(object):

    def __init__(self, seed: int):
        self.status = 0
        self.seed   = str(seed)
        self.error  = ''
