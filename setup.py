""" Chilean Tax Revenue Office (SII) interaction Library.

Implements:
- Document Schema.
- XML handling and signing.
- XML uploading and downloading.
- Document Printing.
"""
from setuptools import setup, find_packages


cfg = {
    'name'               : 'python-sii',
    'long_description'   : __doc__,
    'version'            : '0.1.0.dev2015051500',
    'packages'           : find_packages('src'),
    'package_dir'        : {'': 'src'},
    'namespace_packages' : [],
    'install_requires'   : [
        'jinja2     >= 2.7.3',
        'lxml       >= 3.4.0',
        'xmlsec     >= 0.1.2',
        'suds-jurko >= 0.7.dev0'
    ],
    'dependency_links'   : [],
    'entry_points'       : {},
    'zip_safe'           : False
}


if __name__ == '__main__':
    setup(**cfg)
