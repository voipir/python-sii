""" PDF417 Barcode Generator.
"""
import os
import tempfile
from binascii import hexlify

from cns.pylib.sii.syscallers import Ps2Eps
from .Barcode import Barcode


class PDF417(Barcode):
    """0 0 moveto <{hexdata}> ({options}) /pdf417 /uk.co.terryburton.bwipp findresource exec"""
    # % 0 -10 rmoveto (PDF417) show
    def __init__(self, data, rows=None, columns=None):
        self.data     = data
        self.data_hex = hexlify(data.encode('utf8')).decode('utf8')
        self.rows     = rows
        self.columns  = columns

    @property
    def ps(self):
        opts  = ''
        opts += 'rows='     + self.rows    if self.rows    is not None else ''
        opts += ',columns=' + self.columns if self.columns is not None else ''

        # We append the pdf417 call onto the read in library and return
        return self.__lib__ + self.__doc__.format(hexdata=self.data_hex, options=opts)

    @property
    def eps(self):
        return self._eps()

    @property
    def eps_filepath(self):
        return self._eps(return_path=True)

    def _eps(self, return_path=False):
        tmp      = tempfile.TemporaryDirectory()
        ps_fname  = os.path.join(tmp.name, 'barcode.ps')
        eps_fname = os.path.join(tmp.name, 'barcode.eps')
        result   = None

        with open(ps_fname, 'w') as fh:
            fh.write(self.ps)

        converter = Ps2Eps()
        converter.call(ps_fname)

        if return_path is True:
            return eps_fname
        else:
            with open(eps_fname, 'r') as fh:
                result = fh.read()

            tmp.cleanup()
            return result
