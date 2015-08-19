"""
"""
from ..xml   import XMLNode
from ..types import Date, UnsignedInteger, Enumeration, String, SiiRUT


class NodeCaratula(XMLNode):
    """ Identificacion del Envio del Libro Electronico. """

    RutEmisorLibro    = SiiRUT()
    RutEnvia          = SiiRUT()
    PeriodoTributario = Date(formatting='%Y-%m')
    FchResol          = Date()
    NroResol          = UnsignedInteger()
    TipoOperacion     = Enumeration('COMPRA', 'VENTA')
    TipoLibro         = Enumeration('MENSUAL', 'ESPECIAL', 'RECTIFICA')

    TipoEnvio = Enumeration(
        'PARCIAL',  # Indica que es un Envio Parcial del Libro y que Faltan Otros para Completar el Libro.
        'FINAL',    # Indica que es el Ultimo Envio Parcial. Con Esto se Completa el Libro.
        'TOTAL',    # Indica que es el Unico Envio que Compone el Libro
        'AJUSTE'    # Indica que es un Envio con Informacion para Corregir un Libro Previamente Enviado.
    )

    NroSegmento       = UnsignedInteger()      # Correlativo del Segmento de Libro
    FolioNotificacion = UnsignedInteger()      # Folio de la Notificacion con que se Solicita el Libro Especial
    CodAutRec         = String(max_length=10)  # Codigo de Autorización de Rectificación
