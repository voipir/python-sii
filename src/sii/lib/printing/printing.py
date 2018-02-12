# -*- coding: utf-8 -*-
""" SII Document Printable Template Generation and Printing
"""
import re
import base64
import datetime
import tempfile
import os.path as path

from sii.lib     import types
from sii.lib.lib import format  as fmt
from sii.lib.lib import xml     as xml
from sii.lib.lib import syscall as sys

from . import Document
from . import SectionSignature
from . import SectionPreamble
from . import SectionEmitter, SectionEmitterProvider
from . import SectionSiiPatch
from . import SectionReceiver
from . import SectionItems
from . import SectionPayments
from . import SectionTotals
from . import SectionReferences
from . import SectionBarcode
from . import SectionDisclaimer, SectionDisclaimerDummy


__all__ = [
    'list_formats',
    'list_printers',

    'create_template',
    'tex_to_pdf',

    'print_tex',
    'print_pdf',
    'print_pdf_file'
]


def list_formats():
    """ Returns the available formats the template creation can output
    """
    return [
        'tex',
        'pdf'
    ]


def list_printers():
    lp = sys.LP()
    return lp.query_printers()


def create_template(dte_xml, medium, company=None, cedible=False, draft=False):
    """ Generate TeX Template from a fully completed and stamped Document.

    :param dte_xml: Document XML to create the TeX Template from.
    :param medium:  Medium to generate TeX for; 'carta', 'oficio' or 'thermal80mm' or None in which
                    case it defaults to 'carta' on anything DTE and 'thermal80mm' on anything Boleta.
    :param company: Company, CompanyPool or None. In the first case it expects company metadata, in
                    the second a pool containing metadata for the RUTEmisor specified by the DTE. In
                    the third case the document is handled as a third party / provider document.
    :param cedible: Wether to include the "cedible" declaration formular or not.
    :param draft:   Wether to include a draft disclaimer or not.

    :type dte_xml: :class:lxml.etree.Element (<DTE/>)
    :type medium:  str
    :type company: :class:sii.types.Company or :class:sii.types.CompanyPool or None
    :type cedible: bool
    """
    dte = xml.wrap_xml(dte_xml)

    assert dte.__name__.endswith('DTE'),                 "Provided XML must root with an <DTE> tag. Expected DTE"
    assert hasattr(dte, 'Documento'),                    "Provided XML must contain <Documento>"
    assert medium in ('carta', 'oficio', 'thermal80mm'), "Unsupported medium for printing: {0}".format(medium)

    assert isinstance(company, (types.Company, types.CompanyPool, type(None))), "Invalid argument provided as 'company'"

    if isinstance(company, types.CompanyPool):  # resolve company from pool
        company = company[int(str(dte.Documento.Encabezado.Emisor.RUTEmisor)[:-2])]

    emitter    = _assemble_emitter(dte, company)
    siipatch   = _assemble_siipatch(dte, company)
    receiver   = _assemble_receiver(dte, company)
    items      = _assemble_items(dte, company, draft=draft, provider=True if company is None else False)
    payments   = _assemble_payments(dte, company)
    totals     = _assemble_totals(dte, company)
    references = _assemble_refs(dte, company)
    barcode    = _assemble_barcode(dte, company)
    disclaimer = _assemble_disclaimer(dte, company)

    signature = SectionSignature()
    preamble  = SectionPreamble()

    tex = Document(dte_xml, cedible=cedible)
    tex.set_preamble(preamble)
    tex.set_emitter(emitter)
    tex.set_sii_patch(siipatch)
    tex.set_receiver(receiver)
    tex.set_items(items)
    tex.set_payments(payments)
    tex.set_totals(totals)
    tex.set_references(references)
    tex.set_barcode(barcode)
    tex.set_signature(signature)
    tex.set_disclaimer(disclaimer)

    template = getattr(tex, medium)

    return template, tex.resources


def print_tex(tex, lp_printer):
    """ Print PDF on specified printer. This printer has to be available on `lpstat -a`.

    :param str tex:        TeX in a UTF-8 encoded string.
    :param str lp_printer: Printer to print on.
    """
    b64pdf = tex_to_pdf(tex)
    binpdf = base64.decode(b64pdf)

    print_pdf(binpdf, lp_printer)


def print_pdf(pdf, lp_printer):
    """ Print PDF on specified printer. This printer has to be available on `lpstat -a`.

    :param str pdf:        PDF binary or unicode string. No base64 encoding!
    :param str lp_printer: Printer to print on.
    """
    lp          = sys.LP()
    lp_printers = lp.query_printers()

    if lp_printer not in lp_printers:
        raise ValueError(
            "Provided printer selection <{0}> is not a valid printer on this system. "
            "Possible targets are: [{1}]"
            .format(lp_printer, ", ".join(lp_printers))
        )
    else:
        lp.call_buff(pdf, lp_printer)


def print_pdf_file(pdf_path, lp_printer):
    """ Print PDF on specified printer. This printer has to be available on `lpstat -a`.

    :param str pdf_path:   Path to PDF to be printed.
    :param str lp_printer: Printer to print on.
    """
    lp          = sys.LP()
    lp_printers = lp.query_printers()

    if lp_printer not in lp_printers:
        raise ValueError(
            "Provided printer selection <{0}> is not a valid printer on this system. "
            "Possible targets are: [{1}]"
            .format(lp_printer, ", ".join(lp_printers))
        )
    else:
        lp.call(pdf_path, lp_printer)


def tex_to_pdf(template, resources):
    """ Convert TeX Template to PDF.

    :param template:  String buffer containing the TeX Template.
    :param resources: A list of Resources as defined in `sii.printing.TemplateElement`.
    :return:          PDF string in base64 encoding.

    :type template:  str
    :type resources: list of :class:sii.printing.TemplateElement.Resource
    """
    # DEBUGGING disable tempfile context or you wont be able to see intermediate results
    # as the context will destroy everything done in the temporary directory.
    # tmpdir     = tempfile.TemporaryDirectory()
    # tmpdirname = tmpdir.name

    with tempfile.TemporaryDirectory() as tmpdirname:
        pth_template = path.join(tmpdirname, 'template.tex')
        pth_pdf      = path.join(tmpdirname, 'template.pdf')

        # Write template to temporary directory
        with open(pth_template, 'w') as fh:
            fh.write(template)

        # Write template resources right beside the .tex file
        for res in resources:
            res_path = path.join(tmpdirname, res.filename)

            with open(res_path, 'wb') as fh:
                fh.write(res.data)

        # Run pdflatex to generate pdf
        pdflatex = sys.PdfLaTeX()
        pdflatex.call(filename=pth_template)

        # Read PDF from generated file and return it
        with open(pth_pdf, 'rb') as fh:
            pdf_bin = fh.read()
            pdf_b64 = base64.b64encode(pdf_bin)
            pdf     = str(pdf_b64, 'ascii')

    return pdf


def _str_or_none(obj, name, default=None):
    if hasattr(obj, name):
        return getattr(obj, name)._str
    else:
        return ''


def _assemble_emitter(dte, company):
    if not company:
        if hasattr(dte.Documento.Encabezado.Emisor, 'Telefono'):
            phone = str(dte.Documento.Encabezado.Emisor.Telefono)
        else:
            phone = ""

        emitter = SectionEmitterProvider(
            emitter_name     = str(dte.Documento.Encabezado.Emisor.RznSoc),
            emitter_activity = str(dte.Documento.Encabezado.Emisor.GiroEmis),
            emitter_address  = "{0}, {1}".format(
                str(dte.Documento.Encabezado.Emisor.DirOrigen),
                str(dte.Documento.Encabezado.Emisor.CmnaOrigen)
            ),
            emitter_phone    = phone
        )

        return emitter
    else:
        if hasattr(dte.Documento.Encabezado.Emisor, 'Telefono'):
            emitter_phone = str(dte.Documento.Encabezado.Emisor.Telefono)
        else:
            emitter_phone = company.addr_phone

        emitter = SectionEmitter(
            emitter_name_long   = company.name_long,
            emitter_name_short  = company.name_short,
            emitter_activity    = company.name_activity,
            emitter_hq_addr     = "{0}, {1}".format(company.addr_street, company.addr_city),

            emitter_branch_addr = "{0}, {1}".format(
                str(dte.Documento.Encabezado.Emisor.DirOrigen),
                str(dte.Documento.Encabezado.Emisor.CmnaOrigen)
            ),

            emitter_phone    = emitter_phone,
            order_number     = '',
            emitter_salesman = '',
            licence_plate    = '',
            logo_path        = company.resource_logo_eps
        )

        return emitter


def _assemble_siipatch(dte, company):
    dte_type  = int(dte.Documento.Encabezado.IdDoc.TipoDTE)
    dte_folio = int(dte.Documento.Encabezado.IdDoc.Folio)

    info_rut = None
    info_sii = None

    if company:
        info_rut = fmt.rut(*company.rut_full.split('-'))
        info_sii = company.sii_office_location
    else:
        info_rut = fmt.rut(*str(dte.Documento.Encabezado.Emisor.RUTEmisor).split('-'))
        info_sii = "---------------"

    patch = SectionSiiPatch(
        rut        = info_rut,
        dte_type   = dte_type,
        dte_serial = dte_folio,
        sii_branch = info_sii,
        logo_path  = ""
    )

    return patch


def _assemble_receiver(dte, company):
    receiver = SectionReceiver(
        emission_date    = str(dte.Documento.Encabezado.IdDoc.FchEmis),
        expiration_date  = str(dte.Documento.Encabezado.IdDoc.FchVenc),
        receivername     = str(dte.Documento.Encabezado.Receptor.RznSocRecep),
        receiverrut      = fmt.rut(*str(dte.Documento.Encabezado.Receptor.RUTRecep).split('-')),
        receiveraddress  = str(dte.Documento.Encabezado.Receptor.DirRecep),
        receivercomune   = _str_or_none(dte.Documento.Encabezado.Receptor, 'CmnaRecep'),
        receiveractivity = str(dte.Documento.Encabezado.Receptor.GiroRecep),
        receivercity     = _str_or_none(dte.Documento.Encabezado.Receptor, 'CiudadRecep'),
        emittersalesman  = '',
        ordernumber      = '',
        licenceplate     = ''
    )

    return receiver


def _assemble_items(dte, company, draft, provider):
    items = SectionItems(
        column_layout = (
            {  # NroLinDet
                'name': 'Nro.',
                'align': 'left',
                'expand': False
            },
            {  # QtyItem
                'name': 'Cant.',
                'align': 'left',
                'expand': False
            },
            {  # NmbItem
                'name': 'Detalle',
                'align': 'left',
                'expand': True
            },
            {
                'name': 'Unmd.',
                'align': 'center',
                'expand': False
            },
            {
                'name': 'P.Unit.[$]',
                'align': 'right',
                'expand': False
            },
            {
                'name': 'Dscto.[$]',  # TODO complete with percentage or amount depending on the provided unit
                'align': 'right',
                'expand': False
            },
            {  # MontoItem
                'name': 'Valor[$]',
                'align': 'right',
                'expand': False
            }
        ),
        table_margins = False,
        draft         = draft,
        provider      = provider
    )

    def extract_price(detail):
        if any([det.PrcItem._float % 1 != 0 for det in dte.Documento.Detalle if hasattr(det, 'PrcItem')]):
            return float(detail.PrcItem)
        else:
            return int(detail.PrcItem)

    for detalle in dte.Documento.Detalle:
        col_number   = str(detalle.NroLinDet)                               if hasattr(detalle, 'NroLinDet')      else "-"
        col_quantity = str(detalle.QtyItem._number)                         if hasattr(detalle, 'QtyItem')        else "-"
        col_detail   = str(detalle.NmbItem)                                 if hasattr(detalle, 'NmbItem')        else "-"
        col_unit     = str(detalle.UnmdItem)                                if hasattr(detalle, 'UnmdItem')       else "-"
        col_price    = fmt.thousands(extract_price(detalle),      zero="-") if hasattr(detalle, 'PrcItem')        else "-"
        col_discount = fmt.thousands(int(detalle.DescuentoMonto), zero="-") if hasattr(detalle, 'DescuentoMonto') else "-"
        col_total    = fmt.thousands(int(detalle.MontoItem),      zero="-") if hasattr(detalle, 'MontoItem')      else "-"

        items.append_row((
            col_number,
            col_quantity,
            col_detail,
            col_unit,
            col_price,
            col_discount,
            col_total
        ))

    return items


def _assemble_payments(dte, company):
    payments = SectionPayments(
        table_margins = False
    )
    # TODO append_payment(mode, amount, detail)
    return payments


def _assemble_totals(dte, company):
    # Special Taxes
    special_taxes = {}
    if hasattr(dte.Documento.Encabezado.Totales, 'ImptoReten'):

        for tax in dte.Documento.Encabezado.Totales.ImptoReten:
            tax_code   = int(tax.TipoImp)
            tax_rate   = int(tax.TasaImp)  # FIXME is being ignored
            tax_amount = int(tax.MontoImp)

            if tax_code not in special_taxes:
                special_taxes[tax_code] = [tax_rate, 0]  # FIXME is being ignored

            special_taxes[tax_code][1] += tax_amount

    for code, detail in special_taxes.items():
        detail[1] = fmt.thousands(detail[1], True)

    totals       = dte.Documento.Encabezado.Totales
    total_net    = fmt.thousands(int(totals.MntNeto), True, zero='-') if hasattr(totals, 'MntNeto') else '-'
    total_exempt = fmt.thousands(int(totals.MntExe),  True, zero='-') if hasattr(totals, 'MntExe')  else '-'
    total_tax    = fmt.thousands(int(totals.IVA),     True, zero='-') if hasattr(totals, 'IVA')     else '-'

    # Global Discount or added Charges
    global_discount = 0
    if hasattr(dte.Documento, 'DscRcgGlobal'):
        unit   = str(dte.Documento.DscRcgGlobal.TpoValor)
        amount = int(dte.Documento.DscRcgGlobal.ValorDR)

        if unit == "%":
            neto = int(totals.MntNeto) if hasattr(totals, 'MntNeto') else 0
            fact = 1 - (amount / 100)

            global_discount = fmt.thousands(round(neto / fact) - neto, True)
        else:
            global_discount = fmt.thousands(round(amount), True)
    else:
        global_discount = '-'

    totals = SectionTotals(
        discount     = global_discount,
        net_value    = total_net,
        exempt_value = total_exempt,
        tax          = total_tax,
        special_tax  = special_taxes,
        total        = fmt.thousands(int(dte.Documento.Encabezado.Totales.MntTotal), True)
    )

    return totals


def _assemble_refs(dte, company):
    references = SectionReferences()

    if hasattr(dte.Documento, 'Referencia'):
        for ref in dte.Documento.Referencia:
            references.append_reference(
                index      = int(ref.NroLinRef),
                reason     = str(ref.RazonRef)  if hasattr(ref, 'RazonRef')    else "",
                dte_type   = int(ref.TpoDocRef) if str(ref.TpoDocRef) != "SET" else str(ref.TpoDocRef),
                dte_serial = int(ref.FolioRef),
                dte_date   = str(ref.FchRef)
            )

    return references


def _assemble_barcode(dte, company):
    bcde_xmlstr = dte.Documento.TED._xml
    bcde_clean  = re.sub('>[.*\n]<', '><', bcde_xmlstr)

    res_num  = None
    res_date = None

    if company:
        res_num  = str(company.sii_cert),
        res_date = datetime.datetime.strptime(company.sii_cert_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    else:
        res_num  = "--"
        res_date = "------------"

    barcode = SectionBarcode(
        data               = bcde_clean,
        resolution_number  = res_num,
        resolution_datestr = res_date
    )

    return barcode


def _assemble_disclaimer(dte, company):
    if not company:
        return SectionDisclaimerDummy()
    else:
        disclaimer = SectionDisclaimer(
            company_name = company.name_short,
            company_rut  = fmt.rut(*company.rut_full.split('-'))
        )

        return disclaimer
