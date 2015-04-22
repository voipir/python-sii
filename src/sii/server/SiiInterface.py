""" Sends documents and doc collections to SII and makes sense of return messages
"""
# AUTH_OK = 0

# SEND_OK             = 0
# SEND_ERR_SCHEMA     = 1
# SEND_ERR_SIGN       = 2
# SEND_ERR_RECIPIENT  = 3
# SEND_ERR_DUPLICATE  = 90
# SEND_ERR_UNREADABLE = 91
# SEND_ERR_UNKNOWN    = 99


class SIIException(Exception):
    """ Thrown at submission and return XML interpretation """
    def __init__(self, errno):
        self.errno = errno


class SiiInterface(object):

    def __init__(self, cert_path, host_url, flush=False):
        """
        :param cert_path: Path to certificate to sign off in authentication and document sends.
        :param host_url: WS URL to connect to @(Palena, Maullin, WS1, ...).
        :param flush: Send documents right away to the server. Defaults to False which means, that
                      documents are accumulated until you manually flush them to the server with
                      self.`flush`.
        """
        self._url   = host_url
        self._flush = flush

        self._cert_path = cert_path
        self._cert      = None
        self._service   = None
        self._token     = None
        self._queue     = []

        self._open_service(self._host, self._port)
        self._authenticate(self._cert)

    @property
    def _token(self):
        pass

    def _authenticate(self, cert):
        raise NotImplementedError

    def _envelope(self, docs):
        raise NotImplementedError

    def _send(self, doc):
        raise NotImplementedError

    def send_documento_factura(self, sii_documento_factura):
        if self._flush is False:
            self._send(self._envelope(sii_documento_factura))
        else:
            self._queue.append(sii_documento_factura)

    def send_documento_boleta(self, sii_documento_boleta):
        if self._flush is False:
            self._send(self._envelope(sii_documento_boleta))
        else:
            self._queue.append(sii_documento_boleta)

    def send_nota_debito(self, sii_nota_debito):
        if self._flush is False:
            self._send(self._envelope(sii_nota_debito))
        else:
            self._queue.append(sii_nota_debito)

    def send_nota_credito(self, sii_nota_credito):
        if self._flush is False:
            self._send(self._envelope(sii_nota_credito))
        else:
            self._queue.append(sii_nota_credito)

    def send_libro_compra(self, sii_libro_compra):
        if self._flush is False:
            self._send(self._envelope(sii_libro_compra))
        else:
            self._queue.append(sii_libro_compra)

    def send_libro_venta(self, sii_libro_venta):
        if self._flush is False:
            self._send(self._envelope(sii_libro_venta))
        else:
            self._queue.append(sii_libro_venta)

    def flush(self):
        """ Flush/Send all documents enqueued by `send_*` to the server in bulk/one envelope. """
        if not self._queue:
            return
        else:
            self._send(self._envelope(self._queue))
            self._queue = []
