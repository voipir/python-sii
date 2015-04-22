""" XML Node """
from lxml import etree

from ..types import MissingValueException

__all__ = ['XMLNode']


class XMLNode(object):

    def __init__(self, optional=False, attributes=None):
        self._optional = optional

        if attributes is not None:
            if hasattr(self, '__attributes__'):
                raise AssertionError("Defining '__attributes__' twice!")
            else:
                self.__attributes__ = attributes
        elif hasattr(self, '__attributes__') and self.__attributes__ is not None:
            pass
        else:
            self.__attributes__ = {}

    def __optional__(self):
        return self._optional

    def __node_attrs__(self):
        return self.__attributes__

    def __empty__(self):
        if not len(self.__xml__(content_only=True)) > 0:
            return True
        else:
            return False

    def __xml__(self, content_only=False) -> etree.Element:
        """ Generate a etree.Element node containing/wrapping all XML generating subinstances
        """
        # used in type conditional branching
        from .XMLNodeContainers import XMLTypeContainer, XMLNodeContainer

        dirattrs = self.__attrs()
        element  = etree.Element(self.__class__.__name__.lstrip('Node'),
                                 **self.__expand_attributes(self))
        elements = []

        for attr in dirattrs:
            try:
                value = getattr(self, attr)
            except MissingValueException as e:
                if self._optional:
                    # Return a blank element (we are optional, so even mandatory fields dont apply)
                    return element
                else:
                    # Blow up because we need to be and thus the mandatory fields apply
                    raise MissingValueException(
                        "Value [{0}.{1}] missing/not optional".format(self.__class__.__name__,
                                                                      attr)
                    ) from e

            if value is None:
                continue
            elif isinstance(value, XMLTypeContainer):
                elements.extend(self.__xml_type_container(name=attr, container=value))
            elif isinstance(value, XMLNodeContainer):
                elements.extend(self.__xml_node_container(name=attr, container=value))
            elif isinstance(value, XMLNode):
                elements.extend(self.__xml_node(name=attr, node=value))
            else:
                e      = etree.Element(attr)
                e.text = str(value)
                elements.append(e)

        if content_only:
            return elements
        else:
            element.extend(elements)
            return element

    def __attrs(self):
        return [attr for attr in self.__dir__() if not attr.startswith('_')]

    def __expand_attributes(self, obj):
        d = {}
        for key, value in obj.__node_attrs__().items():
            d[key] = value.format(self=obj)

        return d

    def __xml_type_container(self, name, container):
        """ Create a XML element for each type instance in the XMLTypeContainer """
        elements = []
        for typ in container.__xml__():
            e      = etree.Element(name)
            e.text = str(typ)
            elements.append(e)

        return elements

    def __xml_node_container(self, name, container):
        """ Return Element for each Element in Container """
        elements = []
        for node in container.__xml__():
            if not node.__empty__():
                e      = etree.Element(name)
                e.extend(node.__xml__(content_only=True))
                elements.append(e)

        return elements

    def __xml_node(self, name, node):
        if not node.__empty__():
            e = etree.Element(name)
            e.extend(node.__xml__(content_only=True))
            return [e]
        else:
            return []
