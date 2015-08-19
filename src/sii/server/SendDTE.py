""" Sends documents and doc collections to SII and makes sense of return messages
"""


class SendDTE(object):
    """ Sending of DTE's Protocol Object """

    STATUS_OK             = 0
    STATUS_ERR_SCHEMA     = 1
    STATUS_ERR_SIGN       = 2
    STATUS_ERR_RECIPIENT  = 3
    STATUS_ERR_DUPLICATE  = 90
    STATUS_ERR_UNREADABLE = 91
    STATUS_ERR_UNKNOWN    = 99

    def __init__(self, cert, key):
        pass


# def send_documento_tributario_electronico(dte_list: list) -> :
    # <?xml version="1.0" encoding="ISO-8859-1"?>
    # <EnvioDTE xmlns="http://www.sii.cl/SiiDte"
    # xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    # xsi:schemaLocation="http://www.sii.cl/SiiDte EnvioDTE.xsd"
    # version="1.0">
    # <SetDTE ID="SetDoc">
    # ....................................................................................
    # </EnvioDTE>


# def send_libro_compraventa():
#     pass
