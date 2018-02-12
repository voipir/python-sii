# -*- coding: utf-8 -*-
""" Barcode Section of the Document

Contains:
    * Barcode (PDF417)
    * Resolution Number
    * Resolution Date
"""
from .TemplateElement import TemplateElement, Resource
from .barcode         import PDF417


class SectionBarcode(TemplateElement):
    """
    %% -----------------------------------------------------------------
    %% SECTION - Barcode
    %% -----------------------------------------------------------------
    \\begin{center}
        \\includegraphics[width=%s\\textwidth]{barcode.eps} \\\\
        \\scriptsize{
            Timbre Electrónico SII \\\\
            Res. %s del %s - Verifique documento: www.sii.cl
        }
    \\end{center}
    """
    def __init__(self, data, resolution_number, resolution_datestr):
        self._data        = data
        self._res_number  = resolution_number
        self._res_datestr = resolution_datestr

        self._barcode = None

    @property
    def resources(self):
        ress = []
        ress.append(Resource('barcode.eps', self._eps))

        return ress

    @property
    def carta(self):
        tex = self.__doc__ % (
            0.9,
            self._res_number,
            self._res_datestr
        )
        return tex

    @property
    def oficio(self):
        tex = self.__doc__ % (
            0.9,
            self._res_number,
            self._res_datestr
        )
        return tex

    @property
    def thermal80mm(self):
        tex = self.__doc__ % (
            1.0,
            self._res_number,
            self._res_datestr
        )
        return tex

    @property
    def _eps(self):
        if not self._barcode:
            pdf417        = PDF417(self._data)
            self._barcode = pdf417.eps
        return self._barcode
