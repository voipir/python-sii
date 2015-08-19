"""
"""
from ..xml   import XMLNode
from ..types import Enumeration, SiiMonto


class NodeIVANoRec(XMLNode):
    """ Tabla de IVA No Recuperable (LC) """

    CodIVANoRec = Enumeration(  #
        1,  # Compras destinadas a Generar Operaciones No Gravadas o Exentas.
        2,  # Facturas Registradas Fuera de Plazo.
        3,  # Gastos Rechazados.
        4,  # Entrega Gratuita.
        9   # Otros.
    )

    MntIVANoRec = SiiMonto()  # Monto de IVA No Recuperable
