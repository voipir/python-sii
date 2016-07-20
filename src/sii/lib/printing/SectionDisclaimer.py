""" Disclaimer Section of the Document (you might want to subclass this one)

Contains:
    * Company Name
    * Company Rut
    * Disclaimer of the Company (subclass if you want to change this)
"""
from .TemplateElement import TemplateElement

__all__ = [
    'SectionDisclaimer',
    'SectionDisclaimerDummy'
]


class SectionDisclaimer(TemplateElement):
    """
    %%%% -----------------------------------------------------------------
    %%%% SECTION - Disclaimer
    %%%% -----------------------------------------------------------------
    \\tiny{
        %s\\ (%s) queda facultado(a) para informar y publicar en los registros
        o bancos de datos personales que operan en el país, u otras empresas con similares
        servicios, la mora o incumplimiento de las obligaciones expresadas en esta factura.
    }
    """
    def __init__(self, company_name, company_rut):
        self._company_name = company_name
        self._company_rut  = company_rut

    @property
    def carta(self):
        return self.__doc__ % (self._company_name, self._company_rut)

    @property
    def oficio(self):
        return self.__doc__ % (self._company_name, self._company_rut)

    @property
    def thermal80mm(self):
        return self.__doc__ % (self._company_name, self._company_rut)


class SectionDisclaimerDummy(TemplateElement):
    """
    %%%% -----------------------------------------------------------------
    %%%% SECTION - Disclaimer
    %%%% -----------------------------------------------------------------
    \\tiny{
        Este documento ha sido emitido por una tercera parte, siendo esta impresion en papel
        generada por el receptor para fines internos de archivacion u otros.
    }
    """
    def __init__(self):
        pass

    @property
    def carta(self):
        return self.__doc__

    @property
    def oficio(self):
        return self.__doc__

    @property
    def thermal80mm(self):
        return self.__doc__
