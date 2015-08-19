""" SII Comisions Information """
from ..xml   import XMLNode
from ..types import UnsignedInteger, Enumeration, String, SiiMonto, SiiMontoPorcentaje


class NodeComisiones(XMLNode):
    """ Comisiones y otros cargos es obligatoria para Liquidaciones Factura.

    NroLinCom:    Numero Secuencial de Linea.
    TipoMovim:    (C)omisión u (O)tros cargos.
    Glosa:        Especificación de la comisión u otro cargo.
    TasaComision: Valor porcentual de la comisión u otro cargo.
    ValComNeto:   Valor Neto Comisiones y Otros Cargos.
    ValComExe:    Val. Comis. y Otros Cargos no Afectos o Exentos.
    ValComIVA:    Valor IVA Comisiones y Otros Cargos.
    """
    NroLinCom    = UnsignedInteger(min_value=1, max_value=20)
    TipoMovim    = Enumeration('C', 'O')
    Glosa        = String(max_length=60)
    TasaComision = SiiMontoPorcentaje(optional=True)
    ValComNeto   = SiiMonto()
    ValComExe    = SiiMonto()
    ValComIVA    = SiiMonto(optional=True)
