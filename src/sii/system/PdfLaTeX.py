""" Wrapper for `pdflatex` system call.
"""
import os
import subprocess

from .helpers   import which, cd
from .Interface import SystemCall


__all__ = ['PdfLaTeX']


class PdfLaTeX(SystemCall):

    @property
    def name(self):
        return 'pdflatex'

    @property
    def executable(self):
        return which(self.name)

    def check(self, fail=True):
        exe = which(self.name, fail=fail)
        return False if exe is False else True

    def call(self, filepath):
        """
        :param filepath: Path to latex file file to convert to pdf.

        NOTE: It has to switch directory during execution of `pdflatex`. Otherwise it will fail to
        find the resources referenced by the template.
        On a sidenote it is suggested you make a `tempdir` and copy the template and resources in
        there before running this over it.
        """
        basedir, tex = os.path.split(filepath)
        cmd          = [self.executable, '-halt-on-error', tex]

        with cd(basedir):
            ret = subprocess.call(cmd)

        if ret != 0:
            raise RuntimeError("Call <{0}> failed with exit code: <{1}>".format(cmd, ret))
