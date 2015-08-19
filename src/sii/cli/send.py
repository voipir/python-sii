""" Utilities for sending files to the SII Servers
"""
import sys


def action_send(args):
    if args['--infile']:
        with open(args['--infile'], 'r') as fh:
            doc_xml = fh.read()

        print(doc_xml)  # TODO

    if args['--stdin']:
        print(sys.stdin.read())  # TODO
