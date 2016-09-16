""" Schema Providers.
"""
from datetime import datetime

from . import lib
from . import types

from .stamping  import build_digital_stamp
from .signature import build_template

xml = lib.xml

__all__ = [
    'resolve_schema',
    'bundle_dte',
    'bundle_enviodte',
    'unbundle_enviodte'
]

SCHEMA_FILES = {
    'DTE':
        '/var/lib/sii/schema/doc_dte/DTE_v10.xsd',
    '{http://www.sii.cl/SiiDte}EnvioDTE':
        '/var/lib/sii/schema/doc_dte/EnvioDTE_v10.xsd',
    '{http://www.sii.cl/SiiDte}LibroCompraVenta':
        '/var/lib/sii/schema/doc_info_elec_compra_venta/LibroCV_v10.xsd',
    '{http://www.sii.cl/SiiDte}LibroGuia':
        '/var/lib/sii/schema/doc_libro_guia_despacho/LibroGuia_v10.xsd',
    '{http://www.sii.cl/SiiDte}AEC':
        '/var/lib/sii/schema/doc_cesion/AEC_v10.xsd',
    '{http://www.sii.cl/SiiDte}RespuestaDTE':
        '/var/lib/sii/schema/ptcl_respuesta_envio/RespuestaEnvioDTE_v10.xsd',
    '{http://www.sii.cl/SiiDte}EnvioRecibos':
        '/var/lib/sii/schema/ptcl_recibo_comercial/EnvioRecibos_v10.xsd'
}

SII_NSMAP = {
    None:  'http://www.sii.cl/SiiDte',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}


def resolve_schema(xml):
    """ Resolves the schema based on the root node's tag

    :param `etree.Element` tag_name: The root node of the XML in question.

    :return: A string containing the path to the correponding schema for validation.
    """
    if hasattr(xml, 'getroot'):
        root = xml.getroot()
    else:
        root = xml.getroottree().getroot()

    try:
        path = SCHEMA_FILES[root.tag]
    except KeyError as exc:
        raise KeyError("Could not find schema for root tag '{0}'".format(root.tag)) from exc
    else:
        return path


def bundle_dte(doc_xml, caf):
    """ Takes a <Documento> node and creates the corresponding DTE envelope with the
    corresponding <TED> node and <Signature> templates.

    :param doc_xml: The <Documento> to build the <DTE> envelope for.
    :param caf:     CAF object to use for signature. Alternatively a CAFPool to resolve the
                    apropriate CAF from.
    :return:        <DTE> enveloped <Documento> (only missing signing)

    :type doc_xml: :class:lxml.etree.Element
    :type caf:     :class:sii.types.CAF or :class:sii.types.CAFPool
    :rtype:        :class:lxml.etree.Element
    """
    assert doc_xml.tag == 'Documento', "Expected a <Documento> as input root"

    doc = xml.wrap_xml(doc_xml)

    doc_rut    = int(str(doc.Encabezado.Emisor.RUTEmisor).split('-')[0])
    doc_type   = int(doc.Encabezado.IdDoc.TipoDTE)
    doc_serial = int(doc.Encabezado.IdDoc.Folio)

    if isinstance(caf, types.CAFPool):
        caf = caf.resolve(doc_rut, doc_type, doc_serial)

    assert isinstance(caf, types.CAF), "Expected `CAF` or `CAFPool` as company argument!"

    # Create TED
    doc.TED       = xml.wrap_xml(build_digital_stamp(doc_xml, caf.xml))  # Add SII digital stamp
    doc.TmstFirma = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # Create DTE
    # HACK, SII rips this part out for distributed validation disregarding namespace inheritance.
    # this causes the signature validity to be voided.
    # dte          = xml.create_xml(name='DTE', namespaces=SII_NSMAP)
    dte            = xml.create_xml(name='DTE')
    dte_tree       = xml.dump_etree(dte)
    dte['version'] = "1.0"
    dte.Documento  = doc

    # Create Signature Template
    uri = "#F{0}T{1}".format(
        doc.Encabezado.IdDoc.Folio._int,
        doc.Encabezado.IdDoc.TipoDTE._str
    )

    sig = xml.wrap_xml(build_template(dte_tree, uri))
    dte.Signature = sig

    return xml.dump_etree(dte)


def bundle_enviodte(dte_list, company, to_sii):
    """ Takes a List of DTE's and envelopes it in a <EnvioDTE> containig a DTE bundle <SetDTE> and
    a <ds:Signature> template (ready to be signed).

    :param list dte_list: List containing `etree.Element`'s of <DTE> documents

    :return: 'etree.Element' of generated EnvioDTE
    """
    rut_emitter  = None
    rut_receiver = None

    # Build <Caratula>
    count = {}  # doctype: count
    for dte in dte_list:
        dte = xml.wrap_xml(dte)

        # Check if emitter is still the same
        if not rut_emitter:
            rut_emitter = str(dte.Documento.Encabezado.Emisor.RUTEmisor)
        else:
            if rut_emitter != str(dte.Documento.Encabezado.Emisor.RUTEmisor):
                raise ValueError("Cannot bundle DTE's from different emitters in one upload")

        if not to_sii:
            if rut_receiver is None:
                rut_receiver = str(dte.Documento.Encabezado.Receptor.RUTRecep)
            else:
                if not rut_receiver == str(dte.Documento.Encabezado.Receptor.RUTRecep):
                    raise AssertionError("Can only send to one RUT if receiver is not the SII")

        # Add to document type count
        doc_type = dte.Documento.Encabezado.IdDoc.TipoDTE._int
        if doc_type not in count:
            count[doc_type] = 1
        else:
            count[doc_type] += 1

    company_rut = int(rut_emitter.split('-')[0])

    if isinstance(company, types.CompanyPool):
        company = company[company_rut]

    assert isinstance(company, types.Company), "Expected `Company` as company argument!"

    if not company:
        raise RuntimeError(
            "Could not find company: <{0}>, cannot continue without company context information."
            .format(company_rut)
        )

    caratula              = xml.create_xml(name='Caratula')
    caratula['version']   = "1.0"
    caratula.RutEmisor    = company.rut_full
    caratula.RutEnvia     = company.sii_emitter

    if to_sii:
        caratula.RutReceptor = "60803000-K"
    else:
        caratula.RutReceptor = rut_receiver

    caratula.FchResol     = company.sii_cert_date
    caratula.NroResol     = company.sii_cert
    caratula.TmstFirmaEnv = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    for doc_type, doc_count in count.items():
        entry = xml.create_xml(name='SubTotDTE')

        entry.TpoDTE = doc_type
        entry.NroDTE = doc_count

        caratula.SubTotDTE = entry  # implicit append

    # Build EnvioDTE
    envio      = xml.create_xml(name='EnvioDTE', namespaces=SII_NSMAP)
    envio_tree = xml.dump_etree(envio)
    envio_tree.set(
        '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
        'http://www.sii.cl/SiiDte EnvioDTE_v10.xsd'
    )
    envio['version'] = "1.0"

    envio.SetDTE          = xml.create_xml(name='SetDTE')
    envio.SetDTE['ID']    = "SetDoc"
    envio.SetDTE.Caratula = caratula

    for dte in dte_list:
        dte = xml.wrap_xml(dte)
        envio.SetDTE.DTE = dte

    # Append <ds:Signature>
    signode = xml.wrap_xml(build_template(envio_tree, "#SetDoc"))
    envio.Signature = signode

    return envio_tree


def bundle_libro_ventas(dte_list, company):
    """ Bundle list of <DTE>...</DTE> documents into a <LibroCompraVenta>.

    :param dte_list: List with the <DTE> documents.
    :param company:  Company metadata or CompanyPool to get the Company from.
    :returns:        Handle on <LibroCompraVenta>...</LibroCompraVenta>.

    :type dte_list: [:class:lxml.etree.Element, ...]
    :type company:  :class:sii.types.Company | :class:sii.types.CompanyPool
    :rtype:         :class:lxml.etree.Element
    """
    libro_venta = xml.create_xml(name='LibroCompraVenta', namespaces=SII_NSMAP)
    envio_libro = xml.create_xml(name='EnvioLibro')

    libro_venta_tree = xml.dump_etree(libro_venta)
    libro_venta_tree.set(
        '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
        'http://www.sii.cl/SiiDte LibroCV_v10.xsd'
    )
    libro_venta['version'] = "1.0"

    # Assemble and summarize information
    rut_emitter = None
    doc_month   = None
    summaries   = {}  # doctype: summaries

    for dte in dte_list:
        dte      = xml.wrap_xml(dte)
        dte_head = dte.Documento.Encabezado

        # Check if the document type is allowed in Libro Venta
        if dte_head.IdDoc.TipoDTE._int not in (33, 56, 61):
            raise ValueError(
                "Document type <{0}> does not correspond to Libro Venta reporting"
                .format(dte_head.IdDoc.TipoDTE._int)
            )

        # Check if emitter is still the same
        if not rut_emitter:
            rut_emitter = dte_head.Emisor.RUTEmisor._str
        else:
            if rut_emitter != dte_head.Emisor.RUTEmisor._str:
                raise ValueError("Cannot bundle DTE's from different emitters in one upload")

        # Get the documents month and ensure it stays the same
        if not doc_month:
            doc_date = datetime.strptime(
                dte_head.IdDoc.FchEmis._str,
                '%Y-%m-%d'
            )
            doc_month = (doc_date.year, doc_date.month)
        else:
            doc_date = datetime.strptime(
                dte_head.IdDoc.FchEmis._str,
                '%Y-%m-%d'
            )

            if (doc_date.year, doc_date.month) != doc_month:
                raise ValueError("Cannot bundle DTE's from different taxation periods at the same time")

        # Add to document type summaries
        doc_type = dte_head.IdDoc.TipoDTE._int
        if doc_type not in summaries:
            summaries[doc_type] = {
                'doc_count':        0,  # Document count
                'doc_total_exempt': 0,  # Sum of tax exempt amount
                'doc_total_net':    0,  # Sumatory amount without tax
                'doc_total_tax':    0,  # Sumatory amount of tax
                'doc_total_final':  0,
                'doc_other_tax':    {}   # Other special taxations {tax_code: tax_amount}
            }

        doc_totals = dte_head.Totales

        summary                      = summaries[doc_type]
        summary['doc_count']        += 1
        summary['doc_total_exempt'] += doc_totals.MntExe._int
        summary['doc_total_net']    += doc_totals.MntNeto._int
        summary['doc_total_tax']    += doc_totals.IVA._int
        summary['doc_total_final']  += doc_totals.MntTotal._int

        # Resumen Impuestos Retenidos
        if hasattr(doc_totals, 'ImptoReten'):
            other_tax = summary['doc_other_tax']

            for retencion in doc_totals.ImptoReten:
                tax_type = retencion.TipoImp._int

                if tax_type not in other_tax:
                    other_tax[tax_type] = 0
                other_tax[tax_type] += retencion.MontoImp._int

    company_rut = int(rut_emitter.split('-')[0])

    if isinstance(company, types.CompanyPool):
        company = company[company_rut]

    assert isinstance(company, types.Company), "Expected `Company` as company argument!"

    if not company:
        raise RuntimeError(
            "Could not find company: <{0}>, cannot continue without company context information."
            .format(company_rut)
        )

    # <Caratula>
    caratula                   = xml.create_xml(name='Caratula')
    caratula.RutEmisorLibro    = company.rut_full
    caratula.RutEnvia          = company.sii_emitter
    caratula.PeriodoTributario = "{0}-{1:02}".format(*doc_month)
    caratula.FchResol          = company.sii_cert_date
    caratula.NroResol          = company.sii_cert
    caratula.TipoOperacion     = "VENTA"
    caratula.TipoLibro         = "MENSUAL"
    caratula.TipoEnvio         = "TOTAL"
    # caratula.TipoLibro         = "ESPECIAL"  # Certification only
    # caratula.FolioNotificacion = 1           # Certification only

    envio_libro.Caratula = caratula
    # </Caratula>

    # <ResumenPeriodo>
    resumen = xml.create_xml(name='ResumenPeriodo')
    for doc_type, summary in summaries.items():
        # <TotalesPeriodo>
        totales            = xml.create_xml(name='TotalesPeriodo')
        totales.TpoDoc     = doc_type
        totales.TotDoc     = summary['doc_count']
        totales.TotMntExe  = summary['doc_total_exempt']
        totales.TotMntNeto = summary['doc_total_net']
        totales.TotMntIVA  = summary['doc_total_tax']

        # <TotOtrosImp>
        if 'doc_other_tax' in summary:
            for tax_code, tax_amount in summary['doc_other_tax'].items():
                special_tax = xml.create_xml(name='TotOtrosImp')

                special_tax.CodImp    = tax_code
                special_tax.TotMntImp = tax_amount

                totales.TotOtrosImp = special_tax

        totales.TotMntTotal    = summary['doc_total_final']
        resumen.TotalesPeriodo = totales

    envio_libro.ResumenPeriodo = resumen
    # </ResumenPeriodo>

    # <Detalle>
    for dte in dte_list:
        dte      = xml.wrap_xml(dte)
        dte_head = dte.Documento.Encabezado

        detalle         = xml.create_xml(name='Detalle')
        detalle.TpoDoc  = dte_head.IdDoc.TipoDTE._int
        detalle.NroDoc  = dte_head.IdDoc.Folio._int
        detalle.TasaImp = dte_head.Totales.TasaIVA._float
        detalle.FchDoc  = dte_head.IdDoc.FchEmis._str
        detalle.RUTDoc  = dte_head.Receptor.RUTRecep._str
        detalle.RznSoc  = dte_head.Receptor.RznSocRecep._str
        detalle.MntExe  = dte_head.Totales.MntExe._int
        detalle.MntNeto = dte_head.Totales.MntNeto._int
        detalle.MntIVA  = dte_head.Totales.IVA._int

        # <Detalle><OtrosImp>
        if hasattr(dte_head.Totales, 'ImptoReten'):
            for retencion in dte_head.Totales.ImptoReten:
                otro_imp         = xml.create_xml(name='OtrosImp')
                otro_imp.CodImp  = retencion.TipoImp._int
                otro_imp.TasaImp = retencion.TasaImp._int
                otro_imp.MntImp  = retencion.MontoImp._int

                detalle.OtrosImp = otro_imp

        detalle.MntTotal = dte_head.Totales.MntTotal._int

        envio_libro.Detalle = detalle
    # </Detalle>

    doc_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    doc_uri       = "LV-{0}-{1}".format(*doc_month)

    envio_libro.TmstFirma  = doc_timestamp

    libro_venta.EnvioLibro = envio_libro

    # Append <ds:Signature>
    envio_libro['ID']     = doc_uri
    signode               = xml.wrap_xml(build_template(libro_venta_tree, "#{0}".format(doc_uri)))
    libro_venta.Signature = signode

    return libro_venta_tree


def unbundle_enviodte(xml_enviodte):
    """ Unpacks a <EnvioDTE> returning a list with the contained <DTE>'s

    :param xml_enviodte: XML with <EnvioDTE> as root node.
    :return:             List of XML's with <DTE> as root node.

    :type xml_enviodte: :class:lxml.etree.Element
    :rtype:             :class:lxml.etree.Element
    """
    dte_envio = xml.wrap_xml(xml_enviodte)
    dte_set   = dte_envio.SetDTE

    dte_lst = []
    for dte in dte_set.DTE:
        tree = xml.dump_etree(dte)
        dte_lst.append(tree)

    return dte_lst
