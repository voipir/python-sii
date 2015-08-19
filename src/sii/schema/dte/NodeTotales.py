""" SII DTE Totals Information """
from ..xml   import XMLNode, XMLNodeContainer
from ..types import SiiMonto, SiiValor, SiiMontoPorcentaje, SiiMontoImpuesto

from .NodeImpuestoRetenido import NodeImpuestoRetenido
from .NodeTotalComisiones  import NodeTotalComisiones


class NodeTotales(XMLNode):
    """ Some Notes about Elements in this Structure:

    MntNeto:      Monto Neto del DTE.
    MntExe:       Monto Exento del DTE.
    MntBase:      Monto Base Faenamiento Carne.
    MntMargenCom: Monto Base de Márgenes de Comercialización. Monto informado.
    IVA:          Monto de IVA.
    IVAProp:      Monto de IVA propio.
    IVATerc:      Monto de IVA propio de terceros.
    ImptoReten:   Monto IVA retenido.
    IVANoRet:     Monto de IVA no retenido.
    CredEC:       Credito Especial Empresas Constructoras.
    GrntDep:      Garantia por Deposito de Envases o Embalajes

    MntTotal:      Monto Total del DTE.
    MontoNF:       Monto No Facturable - Corresponde a Bienes o Servicios Facturados Previamente.
    MontoPeriodo:  Total de Ventas o Servicios del Periodo.
    SaldoAnterior: Saldo Anterior - Puede ser Negativo o Positivo.
    VlrPagar:      Valor a Pagar Total del documento.
    """
    MntNeto      = SiiMonto(optional=True)
    MntExe       = SiiMonto(optional=True)
    MntBase      = SiiMonto(optional=True)
    MntMargenCom = SiiMonto(optional=True)

    TasaIVA = SiiMontoPorcentaje(optional=True)
    IVA     = SiiMonto(optional=True)
    IVAProp = SiiMonto(optional=True)
    IVATerc = SiiMonto(optional=True)

    ImptoReten = XMLNodeContainer(NodeImpuestoRetenido, min_occurs=0, max_occurs=20)
    IVANoRet   = SiiMontoImpuesto(optional=True)
    CredEC     = SiiMonto(optional=True)
    GrntDep    = SiiMonto(optional=True)
    Comisiones = NodeTotalComisiones(optional=True)

    MntTotal      = SiiMonto(optional=True)
    MontoNF       = SiiValor(optional=True)
    MontoPeriodo  = SiiValor(optional=True)
    SaldoAnterior = SiiValor(optional=True)
    VlrPagar      = SiiValor(optional=True)
