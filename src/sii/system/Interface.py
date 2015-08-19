""" Interface for all System Call Wrappers needed in this Library.
"""


__all__ = ['SystemCall']


class SystemCall(object):

    @property
    def name(self):
        """ Name of the Executable.. """
        raise NotImplementedError

    @property
    def executable(self):
        """ Path to the Executable. """
        raise NotImplementedError

    def check(self, fail=True):
        """ Check if the Executable can be found and run. This is the point we have to
        fail if the program can not be found and/or is presumably not installed on the system.

        If fail is set to True, it will raise an exception if not available, else just return
        False.
        """
        raise NotImplementedError

    def call(self):
        """ Call the executable to do something. Here the parameters and behaviours are
        implementation specific.
        """
        raise NotImplementedError
