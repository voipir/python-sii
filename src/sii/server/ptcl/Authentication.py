""" Authentication Message Objects

Returned Seed from SOAP request at <https://palena.sii.cl/DTEWS/CrSeed.jws?wsdl>:
<?xml version="1.0" encoding="UTF-8"?>
<SII:RESPUESTA xmlns:SII="http://www.sii.cl/XMLSchema">
    <SII:RESP_HDR>
        <ESTADO>00</ESTADO>
    </SII:RESP_HDR>
    <SII:RESP_BODY>
        <SEMILLA>001667858198</SEMILLA>
    </SII:RESP_BODY>
</SII:RESPUESTA>

"""
import re

import xmlsec
from suds.client import Client
from lxml        import etree

import logging
logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds').setLevel(logging.DEBUG)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)  # MUST BE THIS?
# logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
# logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
# logging.getLogger('suds.resolver').setLevel(logging.DEBUG)
# logging.getLogger('suds.xsd.query').setLevel(logging.DEBUG)
# logging.getLogger('suds.xsd.basic').setLevel(logging.DEBUG)
# logging.getLogger('suds.binding.marshaller').setLevel(logging.DEBUG)


__all__ = ['Seed',
           'SeedDummy',
           'Token']


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
        status  = seed_etree.xpath('//ESTADO/text()')
        seed    = seed_etree.xpath('//SEMILLA/text()')
        msg = seed_etree.xpath('//GLOSA/text()')

        self._status = int(status[0]) if status else None
        self._seed   = seed[0]        if seed   else None
        self._msg    = msg[0]         if msg  else None

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


class Token(object):

    SOAP_URL_PRODUCTION    = "https://palena.sii.cl/DTEWS/GetTokenFromSeed.jws?wsdl"
    SOAP_URL_CERTIFICATION = "https://maullin.sii.cl/DTEWS/GetTokenFromSeed.jws?wsdl"

    TOKEN_OK                   = 0
    TOKEN_XML_IO_ERR           = 1
    TOKEN_XML_SAX_ERR          = 2
    TOKEN_XML_PARSER_CFG_ERR   = 3
    TOKEN_XML_SIG_MISSING_ERR  = 4
    TOKEN_XML_SIG_INVALID_ERR  = 5
    TOKEN_XML_SEED_MISSING_ERR = 6
    TOKEN_MESSAGE_1_ERR        = 7
    TOKEN_RETURN_ERR           = 8
    TOKEN_MESSAGE_2_ERR        = 9
    TOKEN_XML_CERT_MISSING_ERR = 11
    TOKEN_PUBKEY_MISMATCH_ERR  = 21
    TOKEN_AUTH_ERR             = -3
    TOKEN_USER_ERR             = -7  # RUT correct? / User registered with cert auth at SII?

    def __init__(self, seed, key_path, cert_path, cert_env=True):
        """
        :param seed:      Instance of a `Seed` object.
        :param key_path:  Path to private key file.
        :param cert_path: Path to public certificate file.
        :param cert_env:  If you are in the process of certification
                          (SII Ambiente de Certificacion)
        """
        self.seed = seed

        if cert_env:
            self.sii_host = self.SOAP_URL_CERTIFICATION
        else:
            self.sii_host = self.SOAP_URL_PRODUCTION

        self.sii_soap = Client(self.sii_host)
        self.sii_soap.set_options(location=self.sii_host)

        self.key_path  = key_path
        self.cert_path = cert_path

        self._status = None
        self._token  = None
        self._msg    = None

        self._request_etree = self._build_token_request_xml(seed.seed)
        self._token_xml     = self._fetch_token(self._request_etree)
        self._token_etree   = self._prepare_token_xml(self._token_xml)
        self._token_values  = self._parse_token_xml(self._token_etree)

    def _build_token_request_xml(self, seed: str) -> str:
        """ Ex.:
        <getToken>
            <item>
                <Semilla>000002360958</Semilla>
            </item>
            <ds:Signature/>
        </getToken>
        """
        # Create the request Frame
        root = etree.Element('getToken')
        item = etree.SubElement(root, 'item')
        seed = etree.SubElement(item, 'Semilla')
        seed.text = self.seed.seed

        # Create and insert Signature Template
        signode = xmlsec.template.create(root, c14n_method=xmlsec.Transform.C14N,
                                               sign_method=xmlsec.Transform.RSA_SHA1)

        root.append(signode)

        # Add the <ds:Reference/> node to the signature template.
        ref = xmlsec.template.add_reference(signode, digest_method=xmlsec.Transform.SHA1)

        # Add the enveloped transform descriptor.
        xmlsec.template.add_transform(ref, transform=xmlsec.Transform.ENVELOPED)

        # Add Key Value Info and x509 Data
        key_info = xmlsec.template.ensure_key_info(signode)
        xmlsec.template.add_key_value(key_info)
        xmlsec.template.add_x509_data(key_info)

        # Load Key and Certificate
        key = xmlsec.Key.from_file(self.key_path, xmlsec.KeyFormat.PEM)
        key.load_cert_from_file(self.cert_path,   xmlsec.KeyFormat.PEM)

        # Create Crypto Context and sign Signature Node
        ctx = xmlsec.SignatureContext()
        ctx.key = key
        ctx.sign(signode)

        return root

    def _fetch_token(self, request_etree):
        request_xml = etree.tostring(request_etree, method='xml',
                                                    encoding='UTF-8',
                                                    xml_declaration=True).decode('utf8')

        return self.sii_soap.service.getToken(request_xml)

    def _prepare_token_xml(self, token_xml):
        clean_xml   = re.sub(r'>\s+<', '><', token_xml)
        encoded_xml = clean_xml.encode('utf8')
        etree_xml   = etree.fromstring(encoded_xml)
        return etree_xml

    def _parse_token_xml(self, token_etree):
        """
        <SII:RESPUESTA xmlns:SII="http://www.sii.cl/XMLSchema">
            <SII:RESP_HDR>
                <ESTADO>21</ESTADO>
                <GLOSA>Error : Firmar Invalida</GLOSA>
            </SII:RESP_HDR>
        </SII:RESPUESTA>
        """
        status = token_etree.xpath('//ESTADO/text()')
        token  = token_etree.xpath('//TOKEN/text()')
        msg  = token_etree.xpath('//GLOSA/text()')

        self._status = int(status[0]) if status else None
        self._token  = token[0]       if token  else None
        self._msg    = msg[0]         if msg    else None

    @property
    def status(self):
        return self._status

    @property
    def token(self):
        return self._token

    @property
    def message(self):
        return self._msg
