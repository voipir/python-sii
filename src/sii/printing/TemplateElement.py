""" Common Interface expected to be implemented by the different TeX Sections (not to be
confused with \section's in actual TeX).
"""


class TemplateElement(object):

    @property
    def carta(self) -> str:
        raise NotImplementedError

    @property
    def oficio(self) -> str:
        raise NotImplementedError

    @property
    def thermal80mm(self) -> str:
        raise NotImplementedError
