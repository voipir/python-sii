# -*- coding: utf-8 -*-
""" Barcode Creation (PDF417)
"""
import os

basedir = os.path.split(__file__)[0]
bcdelib = os.path.join(basedir, 'psbcdelib.ps')


class Barcode(object):

    __lib__ = open(bcdelib, 'r').read()

    @property
    def ps(self):
        raise NotImplementedError

    @property
    def eps(self):
        raise NotImplementedError
