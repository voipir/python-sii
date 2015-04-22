""" Wrapping for all System Calls needed in this Library.
"""
import os
import subprocess

# from helpers import which, cd
from .helpers import which, cd


__all__ = ['Ghostscript', 'Ps2Eps', 'PdfLaTeX']


class SystemCall(object):

    @property
    def name(self):
        """ Name of the Executable.. """
        raise NotImplementedError

    @property
    def executable(self):
        """ Path to the Executable. """
        raise NotImplementedError

    def check(self):
        """ Check if the Executable can be found and run. This is the point we have to
        fail if the program can not be found and/or is presumably not installed on the system.
        """
        raise NotImplementedError

    def call(self):
        """ Call the executable to do something. Here the parameters and behaviours are
        implementation specific.
        """
        raise NotImplementedError


class Ghostscript(SystemCall):

    @property
    def name(self):
        return 'ghostscript'

    @property
    def executable(self):
        return which(self.name)

    def check(self):
        exe = which(self.name, fail=False)
        return False if exe is False else True

    def call(self):
        raise NotImplementedError


class Ps2Eps(SystemCall):

    @property
    def name(self):
        return 'ps2eps'

    @property
    def executable(self):
        return which(self.name)

    def check(self):
        exe = which(self.name, fail=False)
        return False if exe is False else True

    def call(self, filepath, force=False):
        """
        :param filepath: Path to postscript file to convert to encapsulated postscript.
        :param force:    Force overwrite if "eps" file does already exist.
        """
        cmd = [self.executable, filepath]
        if force is True:
            cmd.insert(1, '-f')

        ret = subprocess.call(cmd)
        if ret != 0:
            raise RuntimeError("Call <{0}> failed with exit code: <{1}>".format(cmd, ret))


class PdfLaTeX(SystemCall):

    @property
    def name(self):
        return 'pdflatex'

    @property
    def executable(self):
        return which(self.name)

    def check(self):
        exe = which(self.name, fail=False)
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
