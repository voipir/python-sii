"""
"""
from ..xml   import XMLNode
from ..types import Enumeration, Integer, SiiValor


class NodeTotIvaNoRec(XMLNode):
    """ Totales de IVA No Recuperable (LC) """

    CodIVANoRec = Enumeration(  # Totales de IVA No Recuperable (LC)
        1,  # Compras destinadas a Generar Operaciones No Gravadas o Exentas
        2,  # Facturas Registradas Fuera de Plazo.
        3,  # Gastos Rechazados.
        4,  # Entrega Gratuita.
        9,  # Otros.
    )

    TotOpIVANoRec  = Integer()   # Numero de Operaciones con IVA No Recuperable.
    TotMntIVANoRec = SiiValor()  # Total de IVA No Recuperable.
