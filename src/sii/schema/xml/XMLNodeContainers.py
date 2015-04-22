""" XML Node """
from ..types import MissingValueException, TypeProperty

from .XMLNode import XMLNode

__all__ = ['XMLTypeContainer',
           'XMLNodeContainer']


class XMLContainerBase(XMLNode):

    def __init__(self, class_template, min_occurs=None, max_occurs=None,
                       kwargs=None, attributes=None):
        self._template  = class_template
        self._instances = []
        self._kwargs    = kwargs or {}

        self._optional   = True if min_occurs == 0 else False
        self._min_occurs = min_occurs
        self._max_occurs = max_occurs

        super().__init__(attributes=attributes)

    def __getitem__(self, key):
        try:
            return self._instances[key]
        except IndexError:
            if self._max_occurs is not None and len(self._instances) < self._max_occurs:
                inst = self._template(optional=self._optional, **self._kwargs)
                self._instances.append(inst)
                return inst
            else:
                raise IndexError("Container full ({0} of {1} items)".format(len(self._instances),
                                                                            self._max_occurs))

    def __len__(self):
        return len(self._instances)

    def __check__(self):
        if self._min_occurs:
            if not len(self._instances) >= self._min_occurs:
                raise MissingValueException("Only {0} ocurrences out of required minimum "
                                            "of {1}".format(len(self._instances),
                                                            self._min_occurs))

        if self._max_occurs:
            if not len(self._instances) <= self._max_occurs:
                raise MissingValueException("Exeeding maximum of {0} allowed ocurrences "
                                            "with {1}".format(self._max_occurs,
                                                              len(self._instances)))

    def add_node(self):
        if self._max_occurs is not None and self._max_occurs < len(self._instances):
            inst = self._template(optional=self._optional, **self._kwargs)
            self._instances.append(inst)

            return inst
        else:
            KeyError("Container full ({0} of {1} items)".format(len(self._instances),
                                                                self._max_occurs))


class XMLTypeContainer(XMLContainerBase):

    def __init__(self, sii_type, min_occurs=None, max_occurs=None,
                       kwargs=None, attributes=None):
        assert issubclass(sii_type, TypeProperty), "Must be a Base or SII Type"

        super().__init__(sii_type, min_occurs, max_occurs, kwargs, attributes)

    def __getitem__(self, key):
        """ In this case we need to extract the value from the property directly """
        inst = self._instances[key]
        return inst.__get__(inst, None)

    def __setitem__(self, key, value):
        try:
            inst = self._instances[key]
        except IndexError:
            if self._max_occurs is not None and len(self._instances) < self._max_occurs:
                inst = self._template(optional=self._optional, **self._kwargs)
                self._instances.append(inst)
            else:
                raise IndexError("Container full ({0} of {1} items)".format(len(self._instances),
                                                                            self._max_occurs))

        inst.__set__(inst, value)

    def __xml__(self):
        self.__check__()

        return [inst.__get__(inst, None) for inst in self._instances]


class XMLNodeContainer(XMLContainerBase):

    def __init__(self, node_type, min_occurs=None, max_occurs=None,
                       kwargs=None, attributes=None):
        assert issubclass(node_type, XMLNode), "Must be a XMLNode derivate"

        super().__init__(node_type, min_occurs, max_occurs, kwargs, attributes)

    def __xml__(self):
        self.__check__()

        return [node for node in self._instances]
