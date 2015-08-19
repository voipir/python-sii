"""
"""
from ..xml   import XMLNode, XMLTypeContainer
from ..types import Integer, UnsignedInteger, Enumeration
from ..types import SiiDoctoType, SiiValor, SiiMonto, SiiMontoPorcentaje

from .NodeTotIVANoRec        import NodeTotIVANoRec
from .NodeTotOtrosImpPeriodo import NodeTotOtrosImpPeriodo
from .NodeTotLiquidaciones   import NodeTotLiquidaciones


class NodeTotalesPeriodo(XMLNode):
    """ Totales de Control, por Tipo de Documento, Para el Periodo Tributario """

    # Specific to both Libro de Compra and Libro de Venta (General)
    TpoDoc = SiiDoctoType()  # Tipo de Documento Resumido

    TotDoc           = UnsignedInteger()  # Numero de Documentos del Tipo Incluidos en el Libro Electronico
    TotAnulado       = UnsignedInteger()  # Numero de Documentos Anulados
    TotOpExe         = UnsignedInteger()  # Numero de Operaciones Exentas
    TotMntExe        = SiiValor()         # Total de los Montos Exentos
    TotMntNeto       = SiiValor()         # Total de los Montos Netos
    TotMntIVA        = SiiValor()         # Total de los Montos de IVA
    TotLey18211      = SiiMonto()         # Total Ley 18211
    TotMntTotal      = SiiValor()         # Total de los Montos Tot
    TotIVANoRetenido = SiiMonto()         # Total IVA No Ret

    TotOtrosImp = XMLTypeContainer(NodeTotOtrosImpPeriodo, min_ocurrs=0, max_ocurrs=20)  # Totales de Otros Impuestos

    # Specific to Libro de Compra
    TpoImp = Enumeration(  # Tipo de Impuesto Resumido (LC)
        1,  # IVA
        2   # Ley 18.211
    )
    TotOpIVARec         = UnsignedInteger()     # Total de Operaciones con IVA Recuperable (LC)
    TotOpActivoFijo     = UnsignedInteger()     # Numero de Operaciones  de Activo Fijo (LC)
    TotMntActivoFijo    = SiiMonto()            # Total Monto Neto de Activo Fijo (LC)
    TotMntIVAActivoFijo = SiiMonto()            # Total del IVA de las Operaciones de Activo Fijo (LC)
    TotOpIVAUsoComun    = UnsignedInteger()     # Numero de Opraciones con IVA Uso Comun (LC)
    TotIVAUsoComun      = SiiMonto()            # Total IVA Uso Comun (LC)
    FctProp             = SiiMontoPorcentaje()  # Factor Proporcionalidad IVA (LC)
    TotCredIVAUsoComun  = SiiMonto()            # Total Credito IVA Uso Comun (LC)
    TotImpSinCredito    = SiiMonto()            # Total  de Impuestos Sin Derecho a Credito (LC)
    TotTabPuros         = SiiMonto()            # Total Tabaco -Puros (LC)
    TotTabCigarrillos   = SiiMonto()            # Total Tabaco - Cigarrillos (LC)
    TotTabElaborado     = SiiMonto()            # Total Tabaco - Elaborado (LC)
    TotImpVehiculo      = SiiMonto()            # Total Impuesto Vehiculos (LC)

    TotIVANoRec = XMLTypeContainer(NodeTotIVANoRec, min_ocurrs=0, max_ocurrs=5)  # Tabla de IVA No Recuperable (LC)

    # Specific to Libro de Venta
    TotIVAFueraPlazo   = SiiMonto()         # Total IVA Fuera de Plazo (LV)
    TotIVAPropio       = SiiValor()         # Total de IVA Propio en Operaciones a Cuenta de Terceros (LV)
    TotIVATerceros     = SiiValor()         # Total de IVA a Cuenta de Terceros (LV)
    TotOpIVARetTotal   = UnsignedInteger()  # Numero de Operaciones con IVA Retenido Total (LV)
    TotIVARetTotal     = SiiMonto()         # Total IVA Retenido Total (LV)
    TotOpIVARetParcial = UnsignedInteger()  # Numero de Operaciones con IVA Retenido Parcial (LV)
    TotIVARetParcial   = SiiMonto()         # Total IVA Retenido Parcial (LV)
    TotCredEC          = SiiMonto()         # Total Credito Empresa Constructore (LV)
    TotDepEnvase       = SiiMonto()         # Total Deposito Envase (LV)
    TotOpIVANoRetenido = UnsignedInteger()  # Numero de Operaciones con IVA No Retenido (LV)
    TotMntNoFact       = SiiValor()         # Total Monto No Facturable (LV)
    TotMntPeriodo      = SiiValor()         # Total Monto Periodo (LV)
    TotPsjNac          = SiiMonto()         # Total Venta PasajeNacional (LV)
    TotPsjInt          = SiiMonto()         # Total Venta Pasaje Internacional (LV)

    TotLiquidaciones = XMLTypeContainer(NodeTotLiquidaciones, min_ocurrs=0)  # Info. Elect. de Venta (LV)
