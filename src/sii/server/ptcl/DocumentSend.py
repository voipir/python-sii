""" Document Send Message Objects
"""
from suds.client import Client


class DocumentSend(object):

    SEND_OK             = 0
    SEND_ERR_SCHEMA     = 1
    SEND_ERR_SIGN       = 2
    SEND_ERR_RECIPIENT  = 3
    SEND_ERR_DUPLICATE  = 90
    SEND_ERR_UNREADABLE = 91
    SEND_ERR_UNKNOWN    = 99

    def __init__(self, sii_host):
        self.send_queue = []
        self.sii_host   = sii_host
        self.sii_soap   = Client(self.sii_host)

    def send_document(self, doc, flush=False):
        self.send_queue.append(doc)

        if flush:
            self.flush()

    def flush(self):
        raise NotImplementedError
