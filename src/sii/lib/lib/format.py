""" Data Formatters and related Utilities.
"""
import locale


__all__ = [
    'thousands',
    'rut'
]


def thousands(value, monetary=False, zero='0'):
    string = ''

    if value == 0:
        string = str(zero)
    else:
        locale.setlocale(locale.LC_ALL, 'es_CL.utf8')  # Hardset locale to Chile

        if isinstance(value, int):
            string = locale.format('%d', value, True, monetary)
        elif isinstance(value, float):
            string = locale.format('%.2f', value, True, monetary)
        else:
            raise TypeError("Don't know how to thousands format type: ".format(type(value)))

    return string


def rut(base, ckdgt):
    """ Formats Chilean R.U.T. thousands separated and with the dash + modulo 11 checksum char.
    """
    basenum = thousands(int(base))
    result  = '{0}-{1}'.format(basenum, ckdgt)

    return result
