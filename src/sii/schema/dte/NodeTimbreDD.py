""" SII Signature Document Data Information """
from ..xml   import XMLNode
from ..types import UnsignedInteger, String, XMLType
from ..types import SiiRUT, SiiDTE, SiiFolio, SiiFecha, SiiFechaHora

# from .NodeCodigoAutFolio import NodeCodigoAutFolio


class NodeTimbreDD(XMLNode):
    """ Datos Basicos de Documento.

    RE:    RUT Emisor.
    TD:    Tipo DTE.
    F:     Folio DTE.
    FE:    Fecha Emision DTE en Formato AAAA-MM-DD.
    RR:    RUT Receptor.
    RSR:   Razon Social Receptor.
    MNT:   Monto Total DTE.
    IT1:   Descripcion Primer Item de Detalle.
    CAF:   Codigo Autorizacion Folios.
    TSTED: TimeStamp de Generacion del Timbre.
    """
    RE    = SiiRUT()
    TD    = SiiDTE()
    F     = SiiFolio()
    FE    = SiiFecha()
    RR    = SiiRUT()
    RSR   = String(min_length=1, max_length=40)
    MNT   = UnsignedInteger()
    IT1   = String(min_length=1, max_length=40)
    CAF   = XMLType()
    TSTED = SiiFechaHora()
