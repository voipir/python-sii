""" Barcode Section of the Document

Contains:
    * Barcode (PDF417)
    * Resolution Number
    * Resolution Date
"""
from .TemplateElement import TemplateElement
from .barcode         import PDF417


class TemplateBarcode(TemplateElement):
    """
    \\begin{center}
        \\includegraphics[width={%s}\\textwidth]{{%s}} \\\\
        \\scriptsize{
            Timbre Electrónico SII \\\\
            Res. %d del %s - Verifique documento: www.sii.cl
        }
    \\end{center}
    """
    def __init__(self, data, resolution_number, resolution_datestr):
        self._data        = data
        self._res_number  = resolution_number
        self._res_datestr = resolution_datestr

        self._barcode = None

    @property
    def carta(self):
        return self.__doc__ % (0.8, self.eps_path, self._res_number, self.resolution_datestr)

    @property
    def oficio(self):
        return self.__doc__ % (0.8, self.eps_path, self._res_number, self.resolution_datestr)

    @property
    def thermal80mm(self):
        return self.__doc__ % (1.0, self.eps_path, self._res_number, self.resolution_datestr)

    @property
    def eps_path(self):
        if not self._barcode:
            pdf417 = PDF417(self._data)
            self._barcode = pdf417.eps_filepath
        else:
            return self._barcode
