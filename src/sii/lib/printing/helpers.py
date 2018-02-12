# -*- coding: utf-8 -*-
""" Printing specific helpers.
"""
import re

__all__ = [
    'escape_tex'
]


def escape_tex(string):
    chars = '%|\$|&'

    return re.sub('(?<!\\\\)({0})'.format(chars), r'\\\1', string)
