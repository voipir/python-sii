""" SII Common Library.
"""
from setuptools import setup, find_packages


cfg = {
    'name'               : 'python-sii',
    'long_description'   : __doc__,
    'version'            : '1.0.3',
    'packages'           : find_packages('src'),
    'package_dir'        : {'': 'src'},

    'namespace_packages': ['sii'],

    'install_requires' : [
        'lxml       >= 3.4.0',
        'PyYAML     >= 3.11',
        'pycrypto   >= 2.6.1',
        'xmlsec     >= 0.3.1',
        'suds-jurko >= 0.7.dev0',
        'requests   >= 2.8.1'

        # Additionally requires LaTex if you pretend to use printing.
        # See debian/control for that. Possibly unavailable under Windows.
    ],

    'include_package_data' : True,
    'package_data'         : {
        'sii.lib.printing.barcode': ['*.ps']
    },

    'dependency_links' : [],
    'zip_safe'         : True
}


if __name__ == '__main__':
    setup(**cfg)
