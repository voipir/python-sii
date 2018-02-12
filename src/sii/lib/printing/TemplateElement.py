""" Common Interface expected to be implemented by the different TeX Sections (not to be
confused with \section's in actual TeX).
"""
from collections import namedtuple

Resource = namedtuple(
    'Resource',
    [
        'filename',
        'data'
    ]
)


class TemplateElement(object):

    @property
    def resources(self):
        """ Requires the return of a list of `Resource` object providing
        the filename the template is going to expect, and the data that
        should be inside of it.

        In case of none, return an empty list.
        """
        return []

    @property
    def carta(self):
        """ Create TeX Template for printable medium: "US Letter"
        """
        raise NotImplementedError

    @property
    def oficio(self):
        """ Create TeX Template for printable medium: "American Foolscap"
        """
        raise NotImplementedError

    @property
    def thermal80mm(self):
        """ Create TeX Template for printable medium: "Thermal endless 80mm width"
        """
        raise NotImplementedError
