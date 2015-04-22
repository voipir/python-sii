""" SII Package Information """
from .xml   import XMLNode
from .types import String, UnsignedInteger


class NodeBultos(XMLNode):
    """ Some Notes about Elements in this Structure:

    Marcas:      Identificación de marcas, cuando es distinto de contenedor.
    IdContainer: Se utiliza cuando el tipo de bulto es contenedor
    Sello:       Sello contenedor. Con digito verificador
    EmisorSello: Nombre emisor sello.
    """
    CodTpoBultos = UnsignedInteger(optional=True, min_digits=3, max_digits=3)
    CantBultos   = UnsignedInteger(optional=True, min_digits=10, max_digits=10)
    Marcas       = String(optional=True, max_length=255)
    IdContainer  = String(optional=True, max_length=25)
    Sello        = String(optional=True, max_length=20)
    EmisorSello  = String(optional=True, max_length=70)
