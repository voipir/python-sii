""" LaTeX document configuration preamble
"""
import sys

from .TemplateElement import TemplateElement


class TemplatePreamble(TemplateElement):
    """
    \\documentclass[{options}]{article}

    \\usepackage[paperwidth={width}mm,%
                paperheight={height}mm,%
                top={top}mm,%
                bottom={bottom}mm,%
                left={left}mm,%
                right={right}mm]{geometry}
    \\usepackage[utf8]{inputenc}
    \\usepackage[spanish]{babel}
    \\usepackage[parfill]{parskip}
    \\usepackage{setspace}
    \\usepackage{textcomp}
    \\usepackage{mdframed}
    \\usepackage{longtable}
    \\usepackage{tabu}
    \\usepackage{graphicx}

    \\pagestyle{empty}
    """

    def __init__(self, size=10, draft=False):
        self.size  = size
        self.draft = draft

    @property
    def carta(self):
        tex  = self.__doc__ % (self._doc_options(), 216, 279, 8, 8, 10, 10)
        tex += """
        \\mdfdefinestyle{siipatch}{nobreak=true          ,%
                                   userdefinedwidth=8cm  ,%
                                   align=center          ,%
                                   linewidth=0.8mm       ,%
                                   innerleftmargin=0.5cm ,%
                                   innerrightmargin=0.5cm}

        \\mdfdefinestyle{emitter}{nobreak=true            ,%
                                  leftline=false          ,%
                                  rightline=false         ,%
                                  linewidth=0.5mm         ,%
                                  skipabove=1mm           ,%
                                  innertopmargin=0mm      ,%
                                  innerbottommargin=1.0mm ,%
                                  innerleftmargin=0cm     ,%
                                  innerrightmargin=0cm}

        \\mdfdefinestyle{items}{nobreak=true          ,%
                                leftline=false        ,%
                                rightline=false       ,%
                                linewidth=0.5mm       ,%
                                innertopmargin=0mm    ,%
                                innerbottommargin=0mm ,%
                                innerleftmargin=0cm   ,%
                                innerrightmargin=0cm}

        \\mdfdefinestyle{signature}{nobreak=true    ,%
                                    linewidth=0.5mm ,%
                                    innertopmargin=0.5cm}
        """
        return tex

    @property
    def oficio(self):
        tex  = self.__doc__ % (self._doc_options(), 216, 279, 8, 8, 10, 10)
        tex += """
        \\mdfdefinestyle{siipatch}{nobreak=true          ,%
                                   userdefinedwidth=8cm  ,%
                                   align=center          ,%
                                   linewidth=0.8mm       ,%
                                   innerleftmargin=0.5cm ,%
                                   innerrightmargin=0.5cm}

        \\mdfdefinestyle{emitter}{nobreak=true            ,%
                                  leftline=false          ,%
                                  rightline=false         ,%
                                  linewidth=0.5mm         ,%
                                  skipabove=1mm           ,%
                                  innertopmargin=0mm      ,%
                                  innerbottommargin=1.0mm ,%
                                  innerleftmargin=0cm     ,%
                                  innerrightmargin=0cm}

        \\mdfdefinestyle{items}{nobreak=true          ,%
                                leftline=false        ,%
                                rightline=false       ,%
                                linewidth=0.5mm       ,%
                                innertopmargin=0mm    ,%
                                innerbottommargin=0mm ,%
                                innerleftmargin=0cm   ,%
                                innerrightmargin=0cm}

        \\mdfdefinestyle{signature}{nobreak=true    ,%
                                    linewidth=0.5mm ,%
                                    innertopmargin=0.5cm}
        """
        return tex

    @property
    def thermal(self):
        # XXX we have a problem with properly controlling the rasterization of EPSON T-88V printers
        # thus we have to cheat like this. (TODO: do properly, this is to generic. Not all printers
        # and drivers under CUPS have the same problem)
        if sys.platform in ('linux2', 'darwin'):
            left, right = 0, 16
        else:
            left = right = 5

        tex  = self.__doc__ % (self._doc_options(), 80, 297, 0, 0, left, right)
        tex += """
        \\mdfdefinestyle{siipatch}{nobreak=true          ,%
                                   align=center          ,%
                                   linewidth=0.8mm       ,%
                                   innerleftmargin=0.5cm ,%
                                   innerrightmargin=0.5cm}

        \\mdfdefinestyle{signature}{nobreak=true         ,%
                                    linewidth=0.3mm      ,%
                                    skipabove=1mm        ,%
                                    innertopmargin=0.3cm ,%
                                    innerleftmargin=1mm  ,%
                                    innerrightmargin=1mm}
        """
        return tex

    def _doc_options(self):
        s  = '{size}pt'.format(self.size)
        s += ',draft' if self.draft is True else ''

        return s
