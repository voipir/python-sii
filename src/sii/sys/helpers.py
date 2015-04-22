""" Miscellaneus Helper Utils
"""
import os
import traceback

__all__ = ['which', 'cd']


def which(program, fail=True):
    """ Sort of replicates the `which` utility.
    """
    is_exe    = lambda fp: os.path.isfile(fp) and os.access(fp, os.X_OK)
    locations = [os.path.join(path, program) for path in os.environ["PATH"].split(os.pathsep)]
    found     = [loc for loc in locations if is_exe(loc)]

    if not found:
        if not fail:
            return False
        else:
            raise RuntimeError("Did not find program: <{0}>".format(program))
    elif len(found) > 1:
        if not fail:
            return False
        else:
            raise RuntimeError("Found more than one instance of the program:\n"
                               "{0}".format('\n'.join(found)))
    else:
        return found[0]


class cd(object):
    """ Directory Context Switcher.

    Switches directory within the guards, switching back when leaving them.
    """
    def __init__(self, dir):
        self.dir    = dir
        self.olddir = None

    def __enter__(self):
        self._olddir = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, etype, evalue, etraceback):
        if any([etype, evalue, etraceback]):
            traceback.print_exception(etype, evalue, etraceback)
        os.chdir(self._olddir)
