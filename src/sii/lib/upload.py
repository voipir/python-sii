""" SII Documents Upload Utilities
"""
import datetime
import collections

import requests
from lxml import etree

from . import lib
from . import ptcl

from .validation import validate_schema, validate_signatures

xml = lib.xml

__all__ = [
    'test_connection',
    'upload_document'
]

HOST_TESTING    = 'https://maullin.sii.cl'
HOST_PRODUCTION = 'https://palena.sii.cl'

STATUS_DESC = {
    "0"  : None,
    "1"  : "El Sender no tiene permiso para enviar",
    "2"  : "Error en tamaño del archivo (muy grande o muy chico)",
    "3"  : "Archivo cortado (tamaño <> al parámetro size)",
    "5"  : "No está autenticado",
    "6"  : "Empresa no autorizada a enviar archivos",
    "7"  : "Esquema Invalido",
    "8"  : "Firma del Documento",
    "9"  : "Sistema Bloqueado",
    "99" : "Error Interno."
}

UploadResponse = collections.namedtuple('UploadResponse',
    [
        'trackid',
        'timestamp'
    ]
)


def test_connection(key_pth, cert_pth, server):
    try:
        token = connect_webservice(key_pth, cert_pth, server)
    except Exception as exc:
        return str(exc)

    if token.status == 0:
        return True
    else:
        return token.status


def upload_document(document, key_pth, cert_pth, server=HOST_PRODUCTION, dryrun=False, verify=True):
    """ Upload a ready and signed <EnvioDTE>.
    """
    # Verify Signature and Schema
    validate_signatures(document)
    validate_schema(document)

    # Prepare payload
    xmlbuff = etree.tostring(
        document,
        pretty_print    = True,
        method          = 'xml',
        encoding        = 'ISO-8859-1',
        xml_declaration = False
    )
    xmlbuff = b'<?xml version="1.0" encoding="ISO-8859-1"?>\n' + xmlbuff

    envio = xml.wrap_xml(document)
    if envio.__name__ == '{http://www.sii.cl/SiiDte}EnvioDTE':
        rut_company, dv_company = str(envio.SetDTE.Caratula.RutEmisor).split('-')
        rut_sender,  dv_sender  = str(envio.SetDTE.Caratula.RutEnvia).split('-')
    elif envio.__name__ == '{http://www.sii.cl/SiiDte}LibroCompraVenta':
        rut_company, dv_company = str(envio.EnvioLibro.Caratula.RutEmisorLibro).split('-')
        rut_sender,  dv_sender  = str(envio.EnvioLibro.Caratula.RutEnvia).split('-')
    elif envio.__name__ == '{http://www.sii.cl/SiiDte}LibroGuia':
        rut_company, dv_company = str(envio.EnvioLibro.Caratula.RutEmisorLibro).split('-')
        rut_sender,  dv_sender  = str(envio.EnvioLibro.Caratula.RutEnvia).split('-')
    else:
        raise TypeError(
            "Document upload for '{0}' not available or not yet implemented"
            .format(envio.__name__)
        )

    # Create HTML Request and Upload
    req = requests.Request()

    req.method   = 'POST'
    req.url      = server + '/cgi_dte/UPL/DTEUpload'
    req.encoding = 'ISO-8859-1'

    req.headers['Referer']    = "http://www.voipir.cl"
    req.headers['User-Agent'] = "Mozilla/4.0 (compatible; PROG 1.0; Windows NT 5.0; YComp 5.0.2.4)"

    req.files.extend([
        ('rutSender',  ('', rut_sender)),
        ('dvSender',   ('', dv_sender)),
        ('rutCompany', ('', rut_company)),
        ('dvCompany',  ('', dv_company)),
        ('file',       ('upload.xml', xmlbuff, 'text/xml; charset=ISO-8859-1'))
    ])

    # Get Session ptcl.Token
    token = connect_webservice(key_pth, cert_pth, server)
    if not token.status == 0:
        raise RuntimeError("Could not connect to {0}".format(server))
    req.headers['Cookie'] = "TOKEN={0}".format(token.token)

    # Get and interpret (TODO) response
    prepared = req.prepare()

    if dryrun:
        dummy = """
            <RECEPCIONDTE>
                <RUTSENDER>9-9</RUTSENDER>
                <RUTCOMPANY>9-9</RUTCOMPANY>
                <FILE>somebullshit</FILE>
                <TIMESTAMP>2016-09-09 09:09:09</TIMESTAMP>
                <STATUS>0</STATUS>
                <TRACKID>999</TRACKID>
            </RECEPCIONDTE>
        """

        dummy = etree.fromstring(dummy)
        return _parse_upload_return(dummy)
    else:
        sess = requests.Session()
        resp = sess.send(prepared, verify=verify)

        resp_xml = etree.fromstring(resp.text)
        return _parse_upload_return(resp_xml)


def connect_webservice(key_pth, cert_pth, server):
    ws_url_seed  = server + '/DTEWS/CrSeed.jws?wsdl'
    ws_url_token = server + '/DTEWS/GetTokenFromSeed.jws?wsdl'

    auth_seed  = ptcl.Seed(sii_host=ws_url_seed)
    auth_token = ptcl.Token(auth_seed, key_pth, cert_pth, sii_host=ws_url_token)

    return auth_token


def _parse_upload_return(tree):
    ret = xml.wrap_xml(tree)

    status = str(ret.STATUS)
    if status == "0":
        return UploadResponse(
            trackid   = int(ret.TRACKID),
            timestamp = datetime.datetime.strptime(str(ret.TIMESTAMP), '%Y-%m-%d %H:%M:%S')
        )
    else:
        raise RuntimeError("SII: '{0}'".format(STATUS_DESC[status]))
