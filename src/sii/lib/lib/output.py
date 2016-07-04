""" Common Output and Printing Utilities
"""
from itertools import zip_longest

__all__ = [
    'print_tabular',

    'yellow',
    'red',
    'green',
    'cyan',
    'clear'
]


def print_tabular(table, none_char="-"):
    """ Takes a OrderedDict and prints an ASCII (UTF-8 Encoded) Table with it like so:

    +------------------+------------+-----------------+..+
    |  Column 1        |  Column2   |  Column N       |
    +------------------+------------+-----------------+..+
    | Big Value        | Stuff      | -               |
    | Looooooong Value | -          | -               |
    .                  .            .                 .
    .                  .            .                 .
    +------------------+------------+-----------------+..+
    """
    widths = _compute_widths(table)   # Widest value per column

    # print header
    _print_widthed_delim(widths)
    _print_widthed_row(table.keys(), widths, none_char)
    _print_widthed_delim(widths)

    # print row by row
    for row in zip_longest(*table.values()):
        _print_widthed_row(row, widths, none_char)

    _print_widthed_delim(widths)  # print closing hline


def _compute_widths(table):
    widths = []

    for column, value_list in table.items():
        widest = len(str(column))

        for value in value_list:
            if len(str(value)) > widest:
                widest = len(str(value))

        widths.append(widest)

    return widths


def _print_widthed_delim(widths, padding=2):
    row_str = "+" + "+".join(["-" * (width + padding) for width in widths]) + "+"

    print(row_str)


def _print_widthed_row(row, widths, none_char):
    assert len(row) == len(widths), "You need one width per column to print this row"

    string = lambda pair: str(pair[0]) if pair[0] is not None else none_char

    row_str = " | ".join(["{0:<{1}}".format(string(pair), str(pair[1])) for pair in zip(row, widths)])

    print("| ",    end="")
    print(row_str, end="")
    print(" |",    end="\n")


STYLE_HEADER    = chr(27) + '[95m'
STYLE_CYAN      = chr(27) + '[1;36m'
STYLE_GREEN     = chr(27) + '[1;32m'
STYLE_WARNING   = chr(27) + '[1;33m'
STYLE_FAIL      = chr(27) + '[1;31m'
STYLE_BOLD      = chr(27) + '[1m'
STYLE_UNDERLINE = chr(27) + '[4m'
STYLE_END       = chr(27) + '[0m'


def yellow(text):
    return "{0}{1}{2}".format(STYLE_WARNING, text, STYLE_END)


def red(text):
    return "{0}{1}{2}".format(STYLE_FAIL, text, STYLE_END)


def green(text):
    return "{0}{1}{2}".format(STYLE_GREEN, text, STYLE_END)


def cyan(text):
    return "{0}{1}{2}".format(STYLE_CYAN, text, STYLE_END)


def clear():
    print(chr(27) + "[2J")
    print(chr(27) + "[H")
