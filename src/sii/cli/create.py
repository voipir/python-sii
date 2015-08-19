""" Testing of stuff related with SII Document generation.
"""
import yaml
from lxml.etree import tostring

from sii.schema import NodeDocumento

from .sign import sign_document


def action_create(args):
    dte_list = []
    xml_list = []
    for yml_file in args['<yaml>']:
        with open(yml_file, 'r') as fh:
            yml = yaml.load(fh)

        doc = create_document(yml)
        dte_list.append(doc)

        if args['--sign']:
            builder = sign_document(args, doc)
            xml     = tostring(builder.__xml__(), pretty_print=args['--pretty']).decode('utf8')
            xml_list.append(xml)

        if args['--stdout-yml']:
            print(yaml.dump(yml))

    output_list = None
    if args['--sign'] :
        output_list = xml_list
    else:
        output_list = [tostring(d.__xml__(), pretty_print=args['--pretty']).decode('utf8')
                       for d
                       in dte_list]

    if args['--stdout']:
        for out in output_list:
            print(out)

    if args['--outfile']:
        with open(args['--outfile'], 'w') as fh:
            for out in output_list:
                fh.write(out)


def create_document(yml):
    doc = NodeDocumento()

    # Header
    doc.Encabezado.IdDoc.TipoDTE      = yml['Encabezado']['IdDoc']['TipoDTE']
    doc.Encabezado.IdDoc.Folio        = yml['Encabezado']['IdDoc']['Folio']
    doc.Encabezado.IdDoc.FchEmis      = yml['Encabezado']['IdDoc']['FchEmis']
    doc.Encabezado.IdDoc.TipoDespacho = yml['Encabezado']['IdDoc']['TipoDespacho']
    doc.Encabezado.IdDoc.IndServicio  = yml['Encabezado']['IdDoc']['IndServicio']
    # doc.Encabezado.IdDoc.MntBruto   = yml['Encabezado']['IdDoc']['MntBruto']
    # doc.Encabezado.IdDoc.FmaPago    = yml['Encabezado']['IdDoc']['FmaPago']
    # doc.Encabezado.IdDoc.FchPago    = yml['Encabezado']['IdDoc']['FchPago']
    # doc.Encabezado.IdDoc.MntPago    = yml['Encabezado']['IdDoc']['MntPago']
    # doc.Encabezado.IdDoc.Pago       = yml['Encabezado']['IdDoc']['Pago']
    doc.Encabezado.IdDoc.FchVenc      = yml['Encabezado']['IdDoc']['FchVenc']

    # Emitter
    doc.Encabezado.Emisor.RUTEmisor = yml['Encabezado']['Emisor']['RUTEmisor']
    doc.Encabezado.Emisor.RznSoc    = yml['Encabezado']['Emisor']['RznSoc']
    doc.Encabezado.Emisor.GiroEmis  = yml['Encabezado']['Emisor']['GiroEmis']

    for idx, acteco in enumerate(yml['Encabezado']['Emisor']['Acteco']):
        doc.Encabezado.Emisor.Acteco[idx] = acteco

    doc.Encabezado.Emisor.CdgSIISucur  = yml['Encabezado']['Emisor']['CdgSIISucur']
    doc.Encabezado.Emisor.DirOrigen    = yml['Encabezado']['Emisor']['DirOrigen']
    doc.Encabezado.Emisor.ComunaOrigen = yml['Encabezado']['Emisor']['ComunaOrigen']

    # Receiver
    doc.Encabezado.Receptor.RUTRecep    = yml['Encabezado']['Receptor']['RUTRecep']
    doc.Encabezado.Receptor.RznSocRecep = yml['Encabezado']['Receptor']['RznSocRecep']
    doc.Encabezado.Receptor.GiroRecep   = yml['Encabezado']['Receptor']['GiroRecep']
    doc.Encabezado.Receptor.DirRecep    = yml['Encabezado']['Receptor']['DirRecep']
    doc.Encabezado.Receptor.CmnaRecep   = yml['Encabezado']['Receptor']['CmnaRecep']

    # Items
    for idx, item in enumerate(yml['Detalle']):
        doc.Detalle[idx].NroLinDet    = item['NroLinDet']
        doc.Detalle[idx].IndExe       = item['IndExe']
        doc.Detalle[idx].IndAgente    = item['IndAgente']
        doc.Detalle[idx].NmbItem      = item['NmbItem']
        doc.Detalle[idx].QtyRef       = item['QtyRef']
        doc.Detalle[idx].UnmdRef      = item['UnmdRef']
        doc.Detalle[idx].PrcRef       = item['PrcRef']
        doc.Detalle[idx].QtyItem      = item['QtyItem']
        doc.Detalle[idx].UnmdItem     = item['UnmdItem']
        doc.Detalle[idx].PrcItem      = item['PrcItem']
        doc.Detalle[idx].RecargoPct   = item['RecargoPct']
        doc.Detalle[idx].RecargoMonto = item['RecargoMonto']
        doc.Detalle[idx].MontoItem    = item['MontoItem']

        for idx_b, cod_imp in enumerate(item['CodImpAdic']):
            doc.Detalle[idx].CodImpAdic[idx_b] = cod_imp

    # Totals
    doc.Encabezado.Totales.MntNeto  = yml['Encabezado']['Totales']['MntNeto']
    doc.Encabezado.Totales.MntExe   = yml['Encabezado']['Totales']['MntExe']
    doc.Encabezado.Totales.TasaIVA  = yml['Encabezado']['Totales']['TasaIVA']
    doc.Encabezado.Totales.IVA      = yml['Encabezado']['Totales']['IVA']
    doc.Encabezado.Totales.MntTotal = yml['Encabezado']['Totales']['MntTotal']

    # Totals - additional Tax
    for idx, imp_ret in enumerate(yml['Encabezado']['Totales']['ImptoReten']):
        doc.Encabezado.Totales.ImptoReten[idx].TipoImp  = imp_ret['TipoImp']
        doc.Encabezado.Totales.ImptoReten[idx].TasaImp  = imp_ret['TasaImp']
        doc.Encabezado.Totales.ImptoReten[idx].MontoImp = imp_ret['MontoImp']

    return doc
