""" Creation and management of SII Digital Stamp Utilities
"""
import re
import copy
import base64
import datetime as dt

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash      import SHA as SHA1
from Crypto.PublicKey import RSA

from .lib import xml


def build_digital_stamp(doc_xml, caf_xml):
    """ Builds a digital stamp digest from a DTE.

    :param `etree.Element` doc_xml: DTE Document node.
    :param `etree.Element` caf_xml: Codigo autorizacion de folios XML.

    :return: `etree.Element` of the 'TED' (Timbre Electronico Digital?) node.
    """
    caf = xml.wrap_xml(caf_xml)
    doc = xml.wrap_xml(doc_xml)

    stamp   = xml.create_xml(name='TED')
    doc.TED = stamp

    stamp['version'] = '1.0'

    stamp.DD       = xml.create_xml(name='DD')
    stamp.DD.RE    = doc.Encabezado.Emisor.RUTEmisor._str
    stamp.DD.TD    = doc.Encabezado.IdDoc.TipoDTE._str
    stamp.DD.F     = doc.Encabezado.IdDoc.Folio._int
    stamp.DD.FE    = doc.Encabezado.IdDoc.FchEmis._str
    stamp.DD.RR    = doc.Encabezado.Receptor.RUTRecep._str
    stamp.DD.RSR   = doc.Encabezado.Receptor.RznSocRecep._str
    stamp.DD.MNT   = doc.Encabezado.Totales.MntTotal._int
    stamp.DD.IT1   = doc.Detalle.NmbItem._str
    stamp.DD.CAF   = copy.deepcopy(caf.CAF)
    stamp.DD.TSTED = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    digest              = xml.create_xml(name='FRMT', value=_build_digital_stamp_digest(doc_xml, caf_xml))
    digest['algoritmo'] = "SHA1withRSA"
    stamp.FRMT          = digest

    return xml.dump_etree(stamp)


def _build_digital_stamp_digest(doc_xml, caf_xml):
    doc = xml.wrap_xml(doc_xml)
    caf = xml.wrap_xml(caf_xml)

    xml_buff = xml.dump_xml(doc.TED.DD, encoding='ISO-8859-1', xml_declaration=False)
    xml_buff = re.sub(b'(?<=>)[\n\r]*(?=<)', b'', xml_buff)
    hash     = SHA1.new(xml_buff)

    key       = RSA.importKey(caf.RSASK._str)
    signer    = PKCS1_v1_5.new(key)
    signature = signer.sign(hash)

    return str(base64.b64encode(signature), 'utf8')
