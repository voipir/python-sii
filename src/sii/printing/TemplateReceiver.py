""" Receiver Section in the Document

Contains:
    * Emission Date
    * Expiration Date
    * Receiver Name
    * Receiver RUT
    * Receiver Activity (Economic Role)
    * Receiver Address
    * Receiver Comune
    * Receiver City
    * (optional)(carta/oficio only) Emitter Salesman
    * (optional)(carta/oficio only) Order Number
    * (optional)(carta/oficio only) Licence Plate
"""
from .TemplateElement import TemplateElement


class TemplateReceiver(TemplateElement):
    """
    \\begin{minipage}{0.5\\textwidth}
    \\begin{flushleft}
        \\small{\\textbf{Emisión:} %s}
    \\end{flushleft}
    \\end{minipage}%%%%
    \\begin{minipage}{0.5\\textwidth}
    \\begin{flushright}
        \\small{\\textbf{Vencimiento:} %s}
    \\end{flushright}
    \\end{minipage}

    \\begin{mdframed}[style=emitter]
        {
            \\tabulinesep=_1.0mm^1.0mm
            \\vspace{1mm}

            \\begin{tabu}{X[-1l] X[-1l] X[-1l] X[-1l]}
                \\rowfont{\\footnotesize}
                \\everyrow{\\rowfont{\\footnotesize}}
                \\textbf{SEÑOR(ES):} &  %s  &
                \\textbf{R.U.T.:}    &  %s  \\
                \\textbf{DIRECCION:} &  %s  &
                \\textbf{COMUNA:}    &  %s  \\
                \\textbf{GIRO:}      &  %s  &
                \\textbf{CIUDAD:}    &  %s  \\
                \\hline
                \\textbf{VENDEDOR:}             &  %s  &
                \\textbf{N\\textdegree PEDIDO:} &  %s  \\
                                                &      &
                \\textbf{PATENTE:}              &  %s
            \\end{tabu}
        }
    \\end{mdframed}
    """
    def __init__(self, emission_date, expiration_date,
                       receivername, receiverrut, receiveraddress,
                       receivercomune, receiveractivity, receivercity,
                       emittersalesman='', ordernumber='', licenceplate=''):
        self._emission_date    = emission_date
        self._expiration_date  = expiration_date

        self._receivername     = receivername
        self._receiverrut      = receiverrut
        self._receiveraddress  = receiveraddress
        self._receivercomune   = receivercomune
        self._receiveractivity = receiveractivity
        self._receivercity     = receivercity

        self._emittersalesman  = emittersalesman
        self._ordernumber      = ordernumber
        self._licenceplate     = licenceplate

    @property
    def carta(self):
        return self.__doc__ % (self._emission_date, self._expiration_date,
                               self._receivername, self._receiverrut,
                               self._receiveraddress, self._receivercomune,
                               self._receiveractivity, self._receivercity,
                               self._emittersalesman, self._ordernumber,
                               self._licenceplate)

    @property
    def oficio(self):
        return self.__doc__ % (self._emission_date, self._expiration_date,
                               self._receivername, self._receiverrut,
                               self._receiveraddress, self._receivercomune,
                               self._receiveractivity, self._receivercity,
                               self._emittersalesman, self._ordernumber,
                               self._licenceplate)

    @property
    def thermal80mm(self):
        tex = """
        {
            \\scriptsize
            \\tabulinesep=_1.0mm^1.0mm

            \\textbf{RAZON SOCIAL RECEPTOR:} \\
            \\begin{tabu}{@{} X[-1l] X[l] @{}}
                \\textbf{Señor(es):} &  %s  \\
                \\textbf{R.U.T.:}    &  %s  \\
                \\textbf{Giro:}      &  %s  \\
                \\textbf{Dirección:} &  %s  \\
                \\textbf{Comuna:}    &  %s  \\
                \\textbf{Ciudad:}    &  %s  \\
            \\end{tabu}
        }
        """
        return tex % (self._receivername, self._receiverrut, self._receiveractivity,
                      self._receiveraddress, self._receivercomune, self._receivercity)
