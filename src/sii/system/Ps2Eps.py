""" Wrapper for `ps2eps` system call.
"""
import subprocess

from .helpers import which
from .Interface import SystemCall


__all__ = ['Ps2Eps']


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
