# -*- coding: utf-8 -*-
""" SII WebService Authentication Seed.
"""
import re

from suds.client import Client
from lxml        import etree

from .helpers import with_retry

__all__ = [
    'Seed'
]


class Seed(object):

    SEED_OK         = 0
    SEED_LINE_ERR   = -1
    SEED_RETURN_ERR = -2

    def __init__(self, sii_host="https://palena.sii.cl/DTEWS/CrSeed.jws?wsdl"):
        self.sii_host = sii_host
        self.sii_soap = Client(self.sii_host)

        self._status = None
        self._seed   = None
        self._error  = None

        self._seed_xml    = self._fetch_seed()
        self._seed_etree  = self._prepare_seed_xml(self._seed_xml)
        self._seed_values = self._parse_seed_xml(self._seed_etree)

    def _fetch_seed(self):
        return with_retry(lambda: self.sii_soap.service.getSeed())

    def _prepare_seed_xml(self, seed_xml):
        clean_xml   = re.sub(r'>\s+<', '><', seed_xml)
        encoded_xml = clean_xml.encode('utf8')
        etree_xml   = etree.fromstring(encoded_xml)
        return etree_xml

    def _parse_seed_xml(self, seed_etree):
        status = seed_etree.xpath('//ESTADO/text()')
        seed   = seed_etree.xpath('//SEMILLA/text()')
        error  = seed_etree.xpath('//GLOSA/text()')

        self._status = int(status[0]) if status else None
        self._seed   = seed[0]  if seed  else None
        self._error  = error[0] if error else None

    @property
    def status(self):
        return self._status

    @property
    def seed(self):
        # return self._seed
        return str(int(self._seed))

    @property
    def error(self):
        return self._error
