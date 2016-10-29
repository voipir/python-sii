""" XML Proxy Class (helper)

Requires External:
    * lxml
"""
import re
import sys

from lxml import etree


__all__ = [
    'create_xml',
    'read_xml',
    'load_xml',
    'wrap_xml',
    'dump_etree',
    'dump_xml',
    'print_xml',
    'write_xml'
]

XML_DECL = lambda enc: b'<?xml version="1.0" encoding="' + bytes(enc, enc) + b'"?>'


class XML(object):

    def __init__(self, node=None, name=None, text=None, namespaces=None):
        self._node = node if node is not None else etree.Element(name, nsmap=namespaces or {})

        if name:
            self._node.tag = name

        if text is not None:
            self._node.text = str(text)

        for child in self._node.getchildren():
            setattr(self, child.tag, XML(name=child.tag, node=child))

    def __repr__(self):
        text = re.sub("^[\n\r\t\s]*", "", str(self))
        text = re.sub("[\n\r\t\s]*$", "", text)
        return "<XML(name={0}, text='{1}')>".format(self.__name__, text)

    def __str__(self):
        if self._node.text is not None:
            return self._node.text
        else:
            return ''

    def __int__(self):
        if self._node.text is not None:
            return int(float(self._node.text))
        else:
            return 0

    def __float__(self):
        if self._node.text is not None:
            return float(self._node.text)
        else:
            return 0.0

    def __iter__(self):
        for sibling in self.__generation__:
            if sibling.__name__ == self.__name__:
                yield sibling

    def __setattr__(self, name, value):
        attrname = re.sub('\{.*\}', '', name)

        # private methods
        if name.startswith('_'):
            super().__setattr__(attrname, value)
            return

        # children to append
        if isinstance(value, XML):
            super().__setattr__(attrname, value)
            self._node.append(value._node)
            return

        # children to modify or create if not yet existant
        try:
            node = getattr(self, name)
            node._node.text = str(value)
        except AttributeError:
            node = XML(name=name, text=value)
            super().__setattr__(attrname, node)
            self._node.append(node._node)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__children__[key]
        return self._node.attrib[key]

    def __setitem__(self, key, value):
        self._node.attrib[key] = value

    def __remove__(self):
        parent = self._node.getparent()

        if len(parent):
            parent.remove(self._node)

    @property
    def __name__(self):
        return self._node.tag

    @property
    def __children__(self):
        return [XML(node=node) for node in self._node.getchildren()]

    @property
    def __siblings__(self):
        siblings = []

        parent = self._node.getparent()
        if parent is not None:
            siblings.extend([XML(node=node) for node in parent.getchildren() if node is not self._node])

        return siblings

    @property
    def __generation__(self):
        return self.__siblings__ + [self]

    @property
    def _etree(self):
        return self._node

    @property
    def _xml(self):
        return etree.tostring(self._node, encoding='unicode')
        # return etree.tostring(self._node)

    @property
    def _str(self):
        return str(self)

    @property
    def _int(self):
        return int(self)

    @property
    def _float(self):
        return float(self)

    @property
    def _number(self):
        value = float(self)
        if value % 1 != 0:
            return value
        else:
            return int(self)

    @property
    def _list(self):
        return list(self)

    def _has(self, name):
        return hasattr(self, name)


def create_xml(name, value=None, namespaces=None):
    node = XML(
        name       = name,
        text       = value or None,
        namespaces = namespaces or {}
    )

    return node


def read_xml(path):
    doc  = None
    root = None

    with open(path, "rb") as fh:
        doc = etree.parse(fh)

    root = doc.getroot()

    return XML(node=root)


def load_xml(xml_string):
    root = etree.fromstring(xml_string)
    return XML(node=root)


def wrap_xml(xml_etree):
    return XML(node=xml_etree)


def dump_etree(xml_node):
    return xml_node._node


def dump_xml(xml_node, **kwargs):
    if isinstance(xml_node, XML):
        xml = dump_etree(xml_node)
    else:
        xml = xml_node

    # Default encoding to UTF-8
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'UTF-8'

    if kwargs['encoding'] == 'UTF-8':
        kwargs['xml_declaration'] = True

    # Replace/Fix XML declaration/preamble
    preamble = b""
    xml_decl = kwargs.get('xml_declaration', False)
    if xml_decl:
        kwargs['xml_declaration'] = False

        preamble = XML_DECL(kwargs['encoding'])
        pretty   = kwargs.get('pretty_print', False)
        if pretty:
            preamble += b"\n"

    buff = etree.tostring(xml, **kwargs)
    buff = preamble + buff

    return buff


def print_xml(xml, file=sys.stdout.buffer, end='\n', encoding='UTF-8'):
    if isinstance(xml, XML):
        xml = dump_etree(xml)

    bytebuff = etree.tostring(
        xml,
        pretty_print    = True,
        method          = 'xml',
        encoding        = encoding,
        xml_declaration = False
    )

    encoded_end = bytes(end, encoding)
    file.write(XML_DECL(encoding) + encoded_end + bytebuff)


def write_xml(xml, fpath, end='\n', encoding='UTF-8', append=False):
    mode = ''

    if append:
        mode = 'ab'
    else:
        mode = 'wb'

    with open(fpath, mode) as fh:
        bytebuff = etree.tostring(
            xml,
            pretty_print    = True,
            method          = 'xml',
            encoding        = encoding,
            xml_declaration = False
        )

        if end != '\n':
            decoded  = str(bytebuff, encoding)
            modified = re.sub('\n', end, decoded)
            bytebuff = bytes(modified, encoding)

        fh.write(XML_DECL(encoding) + bytes(end, encoding) + bytebuff)
