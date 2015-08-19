""" Wrapper for `gs`/`ghostscript` system call.
"""
from .helpers   import which
from .Interface import SystemCall


__all__ = ['Ghostscript']


class Ghostscript(SystemCall):

    @property
    def name(self):
        return 'ghostscript'

    @property
    def executable(self):
        return which(self.name)

    def check(self, fail=True):
        exe = which(self.name, fail=fail)
        return False if exe is False else True

    def call(self):
        raise NotImplementedError
