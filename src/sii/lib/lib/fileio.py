"""
Input/Output Functions.
"""
import os
import shutil

__all__ = [
    'read',
    'read_create',
    'write',
    'write_safe'
]


def read(path, encoding=None):
    """ Normal read from file after path user expansion.

    :param str path:     Path of file from which from read contents.
    :param str encoding: Encoding with which to interpret the contents of the file.
    :returns:            String with the files contents, decoded appropriately.
    """
    path = os.path.abspath(os.path.expanduser(path))

    with open(path, 'r', encoding=encoding) as fh:
        return fh.read()


def read_create(path, templ_path, encoding=None):
    """ Reads file from path after expanding its user and location. If path is non-existant a copy
    of templ_path is copied over, and its contents returned instead.

    :param str path:       Path to file to read from.
    :param str templ_path: Path to template file to copy onto path if path does not exist.
    :returns:              String with the content of the file or templ_path file in the latter case.
    """
    path = os.path.abspath(os.path.expanduser(path))

    if not os.path.isfile(path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        try:
            shutil.copyfile(templ_path, path)
        except IOError as exc:
            raise IOError(
                "Read/Create could not find or read template file at {0}".format(
                    templ_path)
            )

    with open(path, 'r', encoding=encoding) as fh:
        return fh.read()


def write(buff, path, encoding=None):
    """ Normal write to file after path user expansion.

    :param str buff:     Unicode string with the contents to be written.
    :param str path:     Path to file into which to write/create
    :param str encoding: Encoding of the buffer with which to write into file.
    """
    path = os.path.abspath(os.path.expanduser(path))

    with open(path, 'wb') as fh:
        fh.write(buff.encode(encoding))


def write_safe(buff, path):
    """ Writes to file in a safe manner, ensuring all or nothing thus barring
    from corruption.

    :param buff: Unicode encoded string.
    :param path: Path to write to
    """
    tmp_fdir, tmp_fpath = os.path.split(path)
    tmp_fpath = ".{0}.new".format(tmp_fpath)
    tmp_fpath = os.path.join(tmp_fdir, tmp_fpath)

    with open(tmp_fpath, 'w') as fh:
        fh.write(buff)

    shutil.move(tmp_fpath, path)  # swap files
