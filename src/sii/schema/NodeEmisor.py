""" SII Document Emitter """
from .xml   import XMLNode, XMLTypeContainer
from .types import (String, UnsignedInteger,
                    SiiRUT, SiiRazonSocialLarga, SiiFono, SiiMail, SiiComuna, SiiCiudad)


class NodeEmisor(XMLNode):
    """ Some Notes about Elements in this Structure:

    Acteco:       Codigos de Actividad Economica del Emisor Relevante para el DTE
    GuiaExport:   Emisor de una Guía de despacho para Exportación
    CdgSIISucur:  Codigo de Sucursal Entregado por el SII
    CdgVendedor:  Codigo del Vendedor
    IdAdicEmisor: Identificador Adicional del Emisor
    """

    # Required Elements
    RUTEmisor    = SiiRUT()
    RznSoc       = SiiRazonSocialLarga()
    GiroEmis     = String(max_length=80)

    # Optional Elements
    CorreoEmisor = SiiMail(optional=True)
    Sucursal     = String(optional=True, max_length=20)
    CdgSIISucur  = UnsignedInteger(optional=True, max_digits=9)
    DirOrigen    = String(optional=True, max_length=70)
    CmnaOrigen   = SiiComuna(optional=True)
    CiudadOrigen = SiiCiudad(optional=True)
    CdgVendedor  = String(optional=True, max_length=60)
    IdAdicEmisor = String(optional=True, min_length=1, max_length=20)

    # Nodes
    # GuiaExport   = NodeGuiaExportacion  # TODO

    # Containers
    Telefono = XMLTypeContainer(SiiFono, max_occurs=2)
    Acteco   = XMLTypeContainer(UnsignedInteger, kwargs={'max_digits': 6}, max_occurs=4)
