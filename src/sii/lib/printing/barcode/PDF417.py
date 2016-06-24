""" PDF417 Barcode Generator.
"""
import os
import tempfile
import binascii

from sii.lib.lib import syscall

from .Barcode import Barcode


class PDF417(Barcode):
    """0 0 moveto <{hexdata}> ({options}) /pdf417 /uk.co.terryburton.bwipp findresource exec"""
    # % 0 -10 rmoveto (PDF417) show

    def __init__(self, data, rows=None, columns=None):
        self.data     = data
        self.data_hex = binascii.hexlify(data.encode('ISO-8859-1')).decode('utf8')
        self.rows     = rows
        self.columns  = columns

    @property
    def ps(self):
        options = []

        if self.rows:
            options.append('rows={0}'.format(self.rows))

        if self.columns:
            options.append('columns={0}'.format(self.columns))

        # We append the pdf417 call onto the read in library and return
        ps_cmd  = '\n\n'
        ps_cmd += self.__doc__.format(
            hexdata = self.data_hex,
            options = ','.join(options)
        )

        return self.__lib__ + ps_cmd

    @property
    def eps(self):
        return self._eps()

    @property
    def eps_filepath(self):
        return self._eps(return_path=True)

    def _eps(self, return_path=False):
        tmp       = tempfile.TemporaryDirectory()
        ps_fname  = os.path.join(tmp.name, 'barcode.ps')
        eps_fname = os.path.join(tmp.name, 'barcode.eps')
        result    = None

        with open(ps_fname, 'w') as fh:
            fh.write(self.ps)

        converter = syscall.Ps2Eps()
        converter.call(ps_fname)

        # from cns.lib.profiling import timeit
        # timeit("Barcode PS --> EPS Conversion", converter.call, ps_fname)

        if return_path is True:
            return eps_fname
        else:
            with open(eps_fname, 'rb') as fh:
                result = fh.read()

            tmp.cleanup()
            return result
