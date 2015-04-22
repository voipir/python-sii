""" SII Document References Information """
from .xml   import XMLNode
from .types import (UnsignedInteger, String, Enumeration,
                    SiiFolioReferencia, SiiRUT, SiiFecha)


class NodeReferencia(XMLNode):
    """ Some Notes about Elements in this Structure:

    NroLinRef: Numero Secuencial de Linea de Referencia.
    TpoDocRef: Tipo de Documento de Referencia.
    IndGlobal: Indica que se esta Referenciando un Conjunto de Documentos.
    FolioRef:  Folio del Documento de Referencia.
    RUTOtr:    RUT Otro Contribuyente.
    FchRef:    Fecha de la Referencia.
    CodRef:    Tipo de Uso de la Referencia
    RazonRef:  Razon Explicita por la que se Referencia el Documento.
    """
    NroLinRef = UnsignedInteger(max_value=99)
    TpoDocRef = String(min_length=1, max_length=3)
    IndGlobal = Enumeration(1)  # El Documento hace Referencia a un Conjunto de Documentos
                                # Tributarios del Mismo Tipo.
    FolioRef  = SiiFolioReferencia()
    RUTOtr    = SiiRUT()
    FchRef    = SiiFecha()
    CodRef    = Enumeration(1,  # Anula Documento de Referencia.
                            2,  # Corrige Texto del Documento de Referencia
                            3)  # Corrige Montos
    RazonRef  = String(max_length=90)
