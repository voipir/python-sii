# -*- coding: utf-8 -*-
""" SII Document Templating and Printing Submodule.
"""
from .Document import Document

from .SectionPreamble   import SectionPreamble
from .SectionEmitter    import SectionEmitter, SectionEmitterProvider
from .SectionSiiPatch   import SectionSiiPatch
from .SectionReceiver   import SectionReceiver
from .SectionItems      import SectionItems
from .SectionPayments   import SectionPayments
from .SectionTotals     import SectionTotals
from .SectionReferences import SectionReferences
from .SectionBarcode    import SectionBarcode
from .SectionSignature  import SectionSignature
from .SectionDisclaimer import SectionDisclaimer, SectionDisclaimerDummy

from .printing import list_formats, list_printers
from .printing import create_template, tex_to_pdf
from .printing import print_tex, print_pdf, print_pdf_file


__all__ = [
    'list_formats',
    'list_printers',

    'create_template',
    'tex_to_pdf',

    'print_tex',
    'print_pdf',
    'print_pdf_file',

    'Document',

    'SectionPreamble',
    'SectionEmitter',
    'SectionEmitterProvider',
    'SectionSiiPatch',
    'SectionReceiver',
    'SectionItems',
    'SectionPayments',
    'SectionTotals',
    'SectionReferences',
    'SectionBarcode',
    'SectionSignature',
    'SectionDisclaimer',
    'SectionDisclaimerDummy'
]
