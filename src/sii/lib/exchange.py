# -*- coding: utf-8 -*-
""" Document Exchange Tooling

TODO  missing parametrizability
FIXME outdated docstrings
"""
import datetime

from .lib import xml

from . import validation as valid
from . import signature  as sig


__all__ = [
    'create_exchange_response',  # <RecepcionEnvio/>
    'create_document_approval',  # <RecepcionDTE/>
    'create_merchandise_receipt'
]

SII_NSMAP = {
    None:  'http://www.sii.cl/SiiDte',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

ENVIO_STATES = {
    0  : 'Envio Recibido Conforme',
    1  : 'Envio Rechazado - Error de Schema',
    2  : 'Envio Rechazado - Error de Firma',
    3  : 'Envio Rechazado - RUT Receptor No Corresponde',
    90 : 'Envio Rechazado - Archivo Repetido',
    91 : 'Envio Rechazado - Archivo Ilegible',
    99 : 'Envio Rechazado - Otros'
}

ENVIO_DTE_STATES = {
    0  : 'DTE Recibido OK',
    1  : 'DTE No Recibido - Error de Firma',
    2  : 'DTE No Recibido - Error en RUT Emisor',
    3  : 'DTE No Recibido - Error en RUT Receptor',
    4  : 'DTE No Recibido - DTE Repetido',
    99 : 'DTE No Recibido - Otros'
}

ACCEPT_DTE_STATES = {
    0 : 'DTE Aceptado OK',
    1 : 'DTE Aceptado con Discrepancias',
    2 : 'DTE Rechazado'
}

MERCH_DECL = (
    "El acuse de recibo que se declara en este acto, de acuerdo a lo dispuesto en la letra b) del Art. 4, y"
    " la letra c) del Art. 5 de la Ley 19.983, acredita que la entrega de mercaderias o servicio(s) "
    "prestado(s) ha(n) sido recibido(s)."
)

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
ftime_parse = lambda string: datetime.datetime.strptime(string, TIME_FORMAT)
ftime_now   = lambda: datetime.datetime.now().strftime(TIME_FORMAT)
ftime_id    = lambda dt, uid: dt.strftime('%Y%m%d{id:02}').format(id=uid)
ftime_uri   = lambda dt, uid: dt.strftime('F%Y%m%dE{id:02}').format(id=uid)


def create_exchange_response(envio_xml):
    """ Create a "Respuesta a Envío" <RecepcionEnvio>

    This XML reports the ACK of the receival of a specific document/DTE provided by a provider.

    Schema: RespuestaEnvioDTE_v10.xs requiring tags [<RespuestaDTE>, <Resultado>, <RecepcionEnvio>]

    :param list dte_list: List containing :class:etree.Element's of <DTE> documents.
    :return:              :class:etree.Element of containing the reponse XML.
    """
    rut_provider = None
    doc_id       = ftime_id(datetime.datetime.now(),  0)  # TODO parametrize

    envio_dte = xml.wrap_xml(envio_xml)
    set_dte   = envio_dte.SetDTE

    # <RecepcionEnvio>
    received = xml.create_xml(name='RecepcionEnvio')
    received.NmbEnvio    = 'ENVIO_DTE_510527.xml'  # TODO parametrize
    received.FchRecep    = ftime_now()
    received.CodEnvio    = doc_id
    received.EnvioDTEID  = set_dte['ID']
    received.Digest      = str(envio_dte.Signature.SignedInfo.Reference.DigestValue)
    received.RutEmisor   = str(set_dte.Caratula.RutEmisor)
    received.RutReceptor = str(set_dte.Caratula.RutReceptor)

    code, desc = _check_envio_state(envio_xml)
    received.EstadoRecepEnv = code
    received.RecepEnvGlosa  = desc

    received.NroDTE = sum([int(count.NroDTE) for count in set_dte.Caratula.SubTotDTE])
    # </RecepcionEnvio>

    # <RecepcionDTE...>
    for dte in set_dte.DTE:
        header   = dte.Documento.Encabezado.IdDoc
        emitter  = dte.Documento.Encabezado.Emisor
        receiver = dte.Documento.Encabezado.Receptor
        totals   = dte.Documento.Encabezado.Totales

        if rut_provider is None:
            rut_provider = str(emitter.RUTEmisor)

        # All docs must have the same provider!
        if not str(emitter.RUTEmisor) == rut_provider:
            raise AssertionError("Response has to target a unique Provider")

        # <RecepcionDTE>
        item = xml.create_xml(name='RecepcionDTE')

        item.TipoDTE   = int(header.TipoDTE)
        item.Folio     = int(header.Folio)
        item.FchEmis   = str(header.FchEmis)
        item.RUTEmisor = str(emitter.RUTEmisor)
        item.RUTRecep  = str(receiver.RUTRecep)
        item.MntTotal  = int(totals.MntTotal)

        code, desc = _check_incoming_dte_validity(dte)
        item.EstadoRecepDTE = code
        item.RecepDTEGlosa  = desc

        received.RecepcionDTE = item
        # </RecepcionDTE>
    # </RecepcionDTE>

    return _create_respuesta_dte(envio_xml, [received])


def create_document_approval(envio_xml):
    """ Create a "Resultado Aprobación Comercial de Documento" <RecepcionDTE>

    This XML reports the semantic/content ACK of a specific document/DTE provided by a provider. This one
    goes after a `create_exchange_response` for the document has been created and uploaded, since you have
    to have first received the document before being able to ratify its contents.

    Schema: RespuestaEnvioDTE_v10.xs requiring tags [<RespuestaDTE>, <Resultado>, <ResultadoDTE>]

    :param list dte_list: List containing `etree.Element`'s of <DTE> documents.
    :ret: `etree.Element` of containing the approval XML.
    """
    envio_dte = xml.wrap_xml(envio_xml)
    set_dte   = envio_dte.SetDTE

    accepted = []
    # <ResultadoDTE>, ...
    for dte in set_dte.DTE:
        dte_head = dte.Documento.Encabezado

        accept = xml.create_xml(name='ResultadoDTE')
        accept.TipoDTE        = int(dte_head.IdDoc.TipoDTE)
        accept.Folio          = int(dte_head.IdDoc.Folio)
        accept.FchEmis        = str(dte_head.IdDoc.FchEmis)
        accept.RUTEmisor      = str(dte_head.Emisor.RUTEmisor)
        accept.RUTRecep       = str(dte_head.Receptor.RUTRecep)
        accept.MntTotal       = int(dte_head.Totales.MntTotal)
        accept.CodEnvio       = ftime_id(datetime.datetime.now(),  0)  # TODO parametrize

        code, desc = _check_dte_acceptability(dte)
        accept.EstadoDTE      = code
        accept.EstadoDTEGlosa = desc

        accept.CodRchDsc = -1

        accepted.append(accept)
    # ..., </ResultadoDTE>

    return _create_respuesta_dte(envio_xml, accepted)


def _create_respuesta_dte(tree, resp_envio_o_dte_list):
    """ Create envelope for the <RespuestaDTE> XML document family.

    :param tree:                  Original EnvioDTE we are ACK'ing.
    :param resp_envio_o_dte_list: Either a <RecepcionEnvio> or <RecepcionDTE> list of XML's.

    :type tree:                  :class:lxml.etree.Element
    :type resp_envio_o_dte_list: :class:sii.lib.xml.XML
    """
    doc_uri = ftime_uri(datetime.datetime.now(), 0)  # TODO parametrize

    response = xml.create_xml(name='RespuestaDTE', namespaces=SII_NSMAP)
    result   = xml.create_xml(name='Resultado')
    caratula = xml.create_xml(name='Caratula')

    dte = xml.wrap_xml(tree)

    # <Caratula>
    caratula.RutResponde   = str(dte.SetDTE.Caratula.RutReceptor)
    caratula.RutRecibe     = str(dte.SetDTE.Caratula.RutEmisor)
    caratula.IdRespuesta   = int(ftime_parse(str(dte.SetDTE.Caratula.TmstFirmaEnv)).timestamp())
    caratula.NroDetalles   = 0
    # caratula.NmbContacto   # Optional
    # caratula.FonoContacto  # Optional
    # caratula.MailContacto  # Optional
    caratula.TmstFirmaResp = ftime_now()
    # </Caratula>

    # Create Signature Template
    result['ID'] = doc_uri
    signature    = xml.wrap_xml(sig.build_template(xml.dump_etree(response), "#" + doc_uri))

    # Assemble
    result.Caratula = caratula

    for ack in resp_envio_o_dte_list:
        setattr(result, ack.__name__, ack)

        caratula.NroDetalles = int(caratula.NroDetalles) + 1  # increment the entry count

    response.Resultado = result
    response.Signature = signature

    # Set Namespaces
    response_tree = xml.dump_etree(response)
    response_tree.set(
        '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
        'http://www.sii.cl/SiiDte RespuestaEnvioDTE_v10.xsd'
    )

    response['version'] = "1.0"
    caratula['version'] = "1.0"

    return response_tree


def create_merchandise_receipt(envio_xml):
    """ Create a "Recibo de Mercaderías" <EnvioRecibos>

    This XML reports ACK for the Wares provided in a specific Document/DTE provided by a provider.

    Schema: EnvioRecibos_v10.xsd

    :param list dte_list: List containing `etree.Element`'s of <DTE> documents.
    :ret: `etree.Element` of containing the ware receipt XML.
    """
    doc_uri = ftime_uri(datetime.datetime.now(), 0)  # TODO parametrize

    response = xml.create_xml(name='EnvioRecibos', namespaces=SII_NSMAP)
    recv_set = xml.create_xml(name='SetRecibos')
    caratula = xml.create_xml(name='Caratula')

    envio = xml.wrap_xml(envio_xml)

    # <Caratula>
    caratula.RutResponde  = str(envio.SetDTE.Caratula.RutReceptor)
    caratula.RutRecibe    = str(envio.SetDTE.Caratula.RutEmisor)
    # caratula.NmbContacto  = Optional
    # caratula.FonoContacto = Optional
    # caratula.MailContacto = Optional
    caratula.TmstFirmaEnv = ftime_now()
    # </Caratula>

    response.SetRecibos = recv_set
    recv_set.Caratula   = caratula

    # <Recibo>, ...
    for dte in envio.SetDTE.DTE:
        recibo     = xml.create_xml(name='Recibo')
        recibo_doc = xml.create_xml(name='DocumentoRecibo')

        encabezado = dte.Documento.Encabezado

        # <DocumentoRecibo>
        recibo_doc.TipoDoc         = int(encabezado.IdDoc.TipoDTE)
        recibo_doc.Folio           = int(encabezado.IdDoc.Folio)
        recibo_doc.FchEmis         = str(encabezado.IdDoc.FchEmis)
        recibo_doc.RUTEmisor       = str(encabezado.Emisor.RUTEmisor)
        recibo_doc.RUTRecep        = str(encabezado.Receptor.RUTRecep)
        recibo_doc.MntTotal        = int(encabezado.Totales.MntTotal)
        recibo_doc.Recinto         = str(encabezado.Receptor.DirRecep)
        recibo_doc.RutFirma        = "16871943-4"  # TODO parametrize
        recibo_doc.Declaracion     = MERCH_DECL
        recibo_doc.TmstFirmaRecibo = ftime_now()
        # </DocumentoRecibo>

        recibo_uri = "F{folio}T{tipo}".format(
            folio = int(encabezado.IdDoc.Folio),
            tipo  = int(encabezado.IdDoc.TipoDTE)
        )

        recibo_doc['ID']  = recibo_uri
        recibo['version'] = "1.0"

        recibo.DocumentoRecibo = recibo_doc
        recibo.Signature       = xml.wrap_xml(sig.build_template(xml.dump_etree(recibo), "#" + recibo_uri))
        recv_set.Recibo        = recibo
    # ..., </Recibo>

    recv_set['ID']      = doc_uri
    caratula['version'] = "1.0"
    response['version'] = "1.0"

    response.Signature = xml.wrap_xml(sig.build_template(xml.dump_etree(response), "#" + doc_uri))

    return xml.dump_etree(response)


def _check_envio_state(envio_xml):
    """ Run checks on the validity of an incoming SetDTE.

    :param envio_xml: `etree.Element` of the original EnvioDTE we are ACK'ing.

    :return: Tuple of (Integer status code according to `ENVIO_STATES`, Descriptor corresponding to the Code)
    """
    envio = xml.wrap_xml(envio_xml)

    # CHECK 1  : 'Envio Rechazado - Error de Schema'
    if not valid.validate_schema(envio_xml):
        return 1, 'Envio Rechazado - Error de Schema'

    # CHECK 2  : 'Envio Rechazado - Error de Firma'
    if not valid.validate_signatures(envio_xml):
        return 2, 'Envio Rechazado - Error de Firma'

    # CHECK 3  : 'Envio Rechazado - RUT Receptor No Corresponde'
    if str(envio.SetDTE.Caratula.RutReceptor) not in ('80203400-8', '89747000-4'):
        return 3, 'Envio Rechazado - RUT Receptor No Corresponde'

    # CHECK 90 : 'Envio Rechazado - Archivo Repetido'
    # TODO

    # CHECK 91 : 'Envio Rechazado - Archivo Ilegible'
    # TODO

    # CHECK 99 : 'Envio Rechazado - Otros'
    # TODO

    # DEFAULT 0  : 'Envio Recibido Conforme'
    return 0, 'Envio Recibido Conforme'


def _check_incoming_dte_validity(dte):
    """ Run checks on the validity of an incoming DTE.

    :param dte: `cns.lib.xml.XML` of the original DTE we are ACK'ing.

    :return: Tuple of (Integer status code according to `ENVIO_DTE_STATES`, Descriptor corresponding to the Code)
    """
    # CHECK 1  : 'DTE No Recibido - Error de Firma'
    if not valid.validate_signatures(xml.dump_etree(dte)):
        return 1, 'DTE No Recibido - Error de Firma'

    # CHECK 2  : 'DTE No Recibido - Error en RUT Emisor'
    # TODO

    # CHECK 3  : 'DTE No Recibido - Error en RUT Receptor'
    if not str(dte.Documento.Encabezado.Receptor.RUTRecep) in ('80203400-8', '89747000-4'):
        return 3, 'DTE No Recibido - Error en RUT Receptor'

    # CHECK 4  : 'DTE No Recibido - DTE Repetido'
    # TODO

    # CHECK 99 : 'DTE No Recibido - Otros'
    # TODO

    # DEFAULT 0  : 'DTE Recibido OK'
    return 0, 'DTE Recibido OK'


def _check_dte_acceptability(dte):
    """ Run checks on the DTE's semantic validity.

    :param dte: `cns.lib.xml.XML` of the original DTE we are ACK'ing.

    :return: Tuple of (Integer status code according to `ACCEPT_DTE_STATES`, Descriptor corresponding to the Code)
    """
    # CHECK 1 : 'DTE Aceptado con Discrepancias'
    # TODO

    # CHECK 2 : 'DTE Rechazado'
    # TODO

    # DEFAULT 0 : 'DTE Aceptado OK'
    return 0, 'DTE Aceptado OK'
