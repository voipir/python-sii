"""
"""
from ..xml   import XMLNode, XMLTypeContainer
from ..types import Integer, UnsignedInteger, Enumeration, SiiDoctoType, SiiValor

from .NodeTotIVANoRec      import NodeTotIVANoRec
from .NodeTotOtrosImp      import NodeTotOtrosImp
from .NodeTotLiquidaciones import NodeTotLiquidaciones


class NodeTotalesSegmento(XMLNode):
    """ Totales de Control, por Tipo de Documento, Para el Segmento """

    # Specific to both Libro de Compra and Libro de Venta (General)
    TpoDoc = SiiDoctoType()  # Tipo de Documento

    TotDoc           = UnsignedInteger()  # Numero de Documentos del Tipo Incluidos en el Libro Electronico
    TotAnulado       = UnsignedInteger()  # Numero de Documentos Anulados
    TotOpExe         = UnsignedInteger()  # Numero de Operaciones Exentas
    TotMntExe        = SiiValor()  # Total de los Montos Exentos
    TotMntNeto       = SiiValor()  # Total de los Montos Netos
    TotMntTotal      = SiiValor()  # Total de los Montos Totales
    TotIVANoRetenido = SiiValor()  # Total IVA No Retenido
    TotMntIVA        = SiiValor()  # Total de los Montos de IVA (LV) o IVA Recuperable (LC)

    # Specific to Libro de Compra
    TpoImp = Enumeration(  # Tipo de Impuesto Resumido (LC)
        1,  # IVA
        2   # Ley 18.211
    )
    TotOpIVARec         = Integer()   # Total de Operaciones con IVA Recuperable (LC)
    TotOpActivoFijo     = Integer()   # Numero de Operaciones de Activo Fijo (LC)
    TotMntActivoFijo    = SiiValor()  # Total Monto Neto de las Operaciones de Activo Fijo (LC)
    TotMntIVAActivoFijo = SiiValor()  # Total del IVA de las Operaciones de Activo Fijo (LC)
    TotOpIVAUsoComun    = Integer()   # Numero de Operaciones con IVA Uso Comun (LC)
    TotIVAUsoComun      = SiiValor()  # Total IVA Uso Comun (LC)
    TotImpSinCredito    = SiiValor()  # Total  de Impuestos Sin Derecho a Credito (LC)
    TotTabPuros         = SiiValor()  # Total Tabacos - Puros (LC)
    TotTabCigarrillos   = SiiValor()  # Total Tabacos - Cigarrillos (LC)
    TotTabElaborado     = SiiValor()  # Total Tabacos - Elaborados (LC)

    # Specific to Libro de Venta
    TotIVAFueraPlazo   = SiiValor()  # Total IVA Fuera de Plazo (LV)
    TotIVAPropio       = SiiValor()  # Total de IVA Propio en Operaciones a Cuenta de Terceros (LV)
    TotIVATerceros     = SiiValor()  # Total de IVA a Cuenta de Terceros (LV)
    TotLey18211        = SiiValor()  # Total Ley 18.211 (LV)
    TotOpIVARetTotal   = SiiValor()  # Numero de Operaciones con IVA Retenido Total (LV)
    TotIVARetTotal     = SiiValor()  # Total de IVA Retenido Total (LV)
    TotOpIVARetParcial = Integer()   # Numero de Operaciones con IVA Retenido Parcial (LV)
    TotIVARetParcial   = SiiValor()  # Total de IVA Retenido Parcial (LV)
    TotCredEC          = SiiValor()  # Total Credito Empresa Constructora (LV)
    TotDepEnvase       = SiiValor()  # Total de los Depositos por Envase (LV)
    TotOpIVANoRetenido = Integer()   # Numero de Operaciones con IVA No Retenido (LV)
    TotMntNoFact       = SiiValor()  # Total MOnto No Facturable (LV)
    TotMntPeriodo      = SiiValor()  # Total Monto Periodo (LV)
    TotPsjNac          = SiiValor()  # Total Venta Pasaje Nacional (LV)
    TotPsjInt          = SiiValor()  # Total Venta Pasaje Internacional (LV)

    TotIVANoRec      = XMLTypeContainer(NodeTotIVANoRec,      min_ocurrs=0, max_ocurrs=5)
    TotOtrosImp      = XMLTypeContainer(NodeTotOtrosImp,      min_ocurrs=0, max_ocurrs=20)
    TotLiquidaciones = XMLTypeContainer(NodeTotLiquidaciones, min_ocurrs=0)
