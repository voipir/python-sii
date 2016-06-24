""" Wrapper for CAF XML's as provided by the SII at Document ID Signature Keypair Request
"""
from lxml import etree


class CAF(object):

    def __init__(self, caf_xml):
        if isinstance(caf_xml, str):
            self._root = etree.fromstring(caf_xml)
        elif isinstance(caf_xml, etree._Element):
            self._root = caf_xml
        else:
            raise ValueError("Expected XML string or etree.Element as argument")

    def __str__(self):
        return etree.tostring(self._root, encoding='unicode')

    @property
    def xml(self):
        return self._root

    @property
    def company_rut(self):
        rut = self._ctrld_xpath(
            '//RE/text()',
            "Could not parse company RUT in CAF:\n{0}".format(str(self))
        )
        return rut

    @property
    def dte_type(self):
        typ = self._ctrld_xpath(
            '//TD/text()',
            "Could not parse document type in CAF:\n{0}".format(str(self))
        )
        return int(typ)

    @property
    def dte_id_from(self):
        id_from = self._ctrld_xpath(
            '//RNG/D/text()',
            "Could not parse range <from> in CAF:\n{0}".format(str(self))
        )
        return int(id_from)

    @property
    def dte_id_until(self):
        id_until = self._ctrld_xpath(
            '//RNG/H/text()',
            "Could not parse range <until> in CAF:\n{0}".format(str(self))
        )
        return int(id_until)

    @property
    def private_key(self):
        return self._ctrld_xpath(
            '//RSASK/text()',
            "Could not parse private key in CAF:\n{0}".format(str(self))
        )

    @property
    def public_key(self):
        return self._ctrld_xpath(
            '//RSAPUBK/text()',
            "Could not parse public key in CAF:\n{0}".format(str(self))
        )

    def _ctrld_xpath(self, xpath, failmsg):
        values = self._root.xpath(xpath)

        if not values:
            raise RuntimeError(failmsg)
        elif len(values) > 1:
            raise RuntimeError("Found more than one values matching "
                               "\"{0}\" in:\n{1}".format(xpath, self.xml))
        else:
            return values[0]
