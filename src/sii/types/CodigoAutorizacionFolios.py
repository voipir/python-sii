""" Wrapper for CAF XML's as provided by the SII at Document ID Signature Keypair Request
"""
from copy             import deepcopy
from xml.sax.saxutils import unescape as xml_unescape

from lxml import etree


class CodigoAutorizacionFolios(object):

    def __init__(self, caf_xml):
        self._root = etree.fromstring(caf_xml)

    @property
    def xml(self):
        return xml_unescape(etree.tostring(self._root, encoding='unicode'))

    def __xml__(self):
        return deepcopy(self._root.find('CAF'))

    @property
    def company(self):
        rut = self._ctrld_xpath('//DA/RE/text()',
                                "Could not parse company RUT in CAF:\n{0}".format(self.xml))
        return rut

    @property
    def doc_type(self):
        typ = self._ctrld_xpath('//TD/text()',
                                "Could not parse document type in CAF:\n{0}".format(self.xml))
        return int(typ)

    @property
    def doc_id_first(self):
        id_first = self._ctrld_xpath('//RNG/D/text()',
                                     "Could not parse range <first> in CAF:\n{0}".format(self.xml))
        return int(id_first)

    @property
    def doc_id_last(self):
        id_last = self._ctrld_xpath('//RNG/H/text()',
                                     "Could not parse range <last> in CAF:\n{0}".format(self.xml))
        return int(id_last)

    @property
    def private_key(self):
        return self._ctrld_xpath('//RSASK/text()',
                                 "Could not parse private key in CAF:\n{0}".format(self.xml))

    @property
    def public_key(self):
        return self._ctrld_xpath('//RSAPUBK/text()',
                                 "Could not parse public key in CAF:\n{0}".format(self.xml))

    def _ctrld_xpath(self, xpath, failmsg):
        values = self._root.xpath(xpath)

        if not values:
            raise RuntimeError(failmsg)
        elif len(values) > 1:
            raise RuntimeError("Found more than one values matching "
                               "\"{0}\" in:\n{1}".format(xpath, self.xml))
        else:
            return values[0]

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as fh:
            xml_string = fh.read()
            return cls(xml_string)
