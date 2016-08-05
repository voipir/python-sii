""" Wrapping for all System Calls needed in this Library.

TODO:
* Break out lpstat stuff into own call.
"""
import os
import re
import tempfile
import subprocess

from .shell import which, cd


__all__ = [
    'SystemCall',

    'Ghostscript',
    'Ps2Eps',
    'PdfLaTeX',
    'LP'
]


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

        NOTE: This function should default to hiding stdout and stderr from the callable.
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

        ret, out, err = _call(cmd, timeout=5)

        if ret != 0:
            raise RuntimeError(
                "Call <{0}> failed with exit code: <{1}> and output {2}"
                .format(cmd, ret, out)
            )


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

    def call(self, filename):
        """
        :param filename: Path to TeX file to generate PDF from.

        NOTE: It has to switch directory during execution of `pdflatex`. Otherwise it will fail to
        find the resources referenced by the template.
        On a sidenote it is suggested you make a `tempdir` and copy the template and resources in
        there before running this over it.
        """
        basedir, tex = os.path.split(filename)

        cmd           = [self.executable, '--interaction batchmode', tex]
        ret, out, err = _call(cmd, timeout=5, cwd=basedir)

        if ret != 0:
            raise RuntimeError("Call \"{0}\" failed with exit code: <{1}>".format(" ".join(cmd), ret))


class LP(SystemCall):
    """ CUPS `lp` Command Line Interface.
    """

    @property
    def name(self):
        return 'lp'

    @property
    def executable(self):
        return which(self.name)

    def check(self):
        exe = which(self.name, fail=False)
        return False if exe is False else True

    def call(self, filepath, printer=None):
        """ Print a file on a printer.

        :param filepath: Path to the file to be printed.
        :param printer:  Name of the printer to print on. See `query_printers` to get a list. If None is provided
                         the system default printer will be used. If there is none available, a ValueError will be
                         thrown.
        """
        cmd = ['lp']

        if not printer:
            printer = self.query_printer_default()

            if not printer:
                raise ValueError("No printer provided and no default system printer to fallback to.")

        cmd.extend(['-d', printer])   # Specify the printer
        cmd.extend(['--', filepath])  # Specify the file

        code, output, error = _call(cmd, timeout=5)

        if not code == 0:
            raise RuntimeError("`lp` exited with non-zero: <{0}>".format(code))

    def call_buff(self, data, printer=None):
        """ Print a buffer on a printer.

        :param bytes data: Data buffer to be printed.
        :param printer:    Name of the printer to print on. See `query_printers` to get a list.
        """
        if isinstance(data, str):
            data = bytes(data, 'UTF-8')

        with tempfile.NamedTemporaryFile() as tmp:
            tmp.file.write(data)
            tmp.file.flush()

            self.call(tmp.name, printer)

    def query_printers(self, only_ready=True):
        """ Return a list of available printers.

        :param bool only_ready: Appends a '-a' for available on the `ldstat` listing.

        :return: List of printer names as to be addressed on `ld`.
        """
        printers = []
        cmd      = ['lpstat']

        if only_ready:
            cmd.append('-a')

        code, output, error = _call(cmd, timeout=5)

        if not code == 0:
            raise RuntimeError("`lpstat` exited with error code: <{0}>".format(code))

        if output:
            lines = output.split('\n')

            for line in lines:
                match = re.match('^(?P<name>\w+) accepting requests since (?P<avail_since>[\w\s]+)', line)

                if match:
                    attrs = match.groupdict()
                    printers.append(attrs['name'])

        return printers

    def query_printer_default(self):
        """ Query which printer is set as default.

        :return: String with the name as to be addressed on `ld` or `None` if none is set on the
        system.
        """
        printer = None
        cmd     = ['lpstat', '-d']

        code, output, error = _call(cmd, timeout=5)

        if not code == 0:
            raise RuntimeError("`lpstat` exited with error code: <{0}>".format(code))

        if output:
            match = re.match('^system default destination: (?P<printer>[\w-]+)$', output)

            if match:
                printer = match.groupdict()['printer']

        return printer


def _call(args, timeout, cwd=None):
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)

    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        out, err = proc.communicate()

    ret = proc.returncode
    out = str(out, 'UTF-8')
    err = str(err, 'UTF-8')

    return ret, out, err
