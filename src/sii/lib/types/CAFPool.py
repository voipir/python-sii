""" Wrapper around CAF File.

This is currently only a proxy to an internal object from cns.lib.sii.
"""
import os
import collections

from lxml import etree

from ..lib import xml

from .CAF import CAF

__all__ = [
    "CAFPool"
]

read_rut = lambda raw: int(raw.split('-')[0])


class CAFPool(object):

    def __init__(self, dirpath):
        self._path   = os.path.abspath(os.path.expanduser(dirpath))
        self._fnames = [fname for fname in os.listdir(self._path) if os.path.splitext(fname)[-1] == ".xml"]
        self._fpaths = [os.path.join(self._path, fname) for fname in self._fnames]
        self._trees  = [_read_caf(fname) for fname in self._fpaths]
        self._cafs   = [CAF(tree) for tree in self._trees]

        self._idx_company = collections.defaultdict(lambda: list())
        for caf in self._cafs:
            rut = read_rut(caf.company_rut)
            self._idx_company[rut].append(caf)

    def resolve(self, rut, dte_type, dte_id):
        """ Returns CAF if available for given <company, dte_type, dte_id> information. """
        cafs  = self._idx_company[rut]
        typed = [caf for caf in cafs if caf.dte_type == dte_type]

        for caf in typed:
            if caf.dte_id_from <= dte_id <= caf.dte_id_until:
                return caf

        raise RuntimeError(
            "Could not find CAF for document <company={0}, type={1}, id={2}>".format(rut, dte_type, dte_id)
        )

    def resolve_document(self, dte):
        """ Returns CAF if available for given DTE inner <Documento>. """
        dte = xml.wrap_xml(dte)

        dte_type = int(dte.Encabezado.IdDoc.TipoDTE)
        dte_id   = int(dte.Encabezado.IdDoc.Folio)
        rut_full = str(dte.Encabezado.Emisor.RUTEmisor)

        rut = read_rut(rut_full)

        return self.resolve_company(rut, dte_type, dte_id)


def _read_caf(path):
    with open(path, "rb") as fh:
        xml = etree.parse(fh)

    return xml.getroot()
