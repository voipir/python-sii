# -*- coding: utf-8 -*-
""" SII Protocol Objects.
"""
from .Seed  import Seed
from .Token import Token


__all__ = [
    'Seed',
    'Token'
]


# Shut up SUDS
import logging
logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('suds.client').setLevel(logging.ERROR)
logging.getLogger('suds.transport').setLevel(logging.ERROR)
logging.getLogger('suds.resolver').setLevel(logging.ERROR)
logging.getLogger('suds.wsdl').setLevel(logging.ERROR)
logging.getLogger('suds.xsd.schema').setLevel(logging.ERROR)
logging.getLogger('suds.xsd.query').setLevel(logging.ERROR)
logging.getLogger('suds.xsd.basic').setLevel(logging.ERROR)
logging.getLogger('suds.binding.marshaller').setLevel(logging.ERROR)
