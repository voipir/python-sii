""" SII Interactions Command Line Interface

Usage:
    sii test auth <key> <cert>
    sii create <yaml>... [--sign=CAF] [--outfile=FILE | --stdout] [--stdout-yml] [--pretty]
    sii send (--infile=FILE | --stdin)


Options:
"""
import docopt

from sii.cli import action_test, action_create, action_send


def main():
    args = docopt.docopt(__doc__)
    # print(args)

    if args['test']:
        return action_test(args)

    if args['create']:
        return action_create(args)

    if args['send']:
        return action_send(args)


if __name__ == '__main__':
    main()
