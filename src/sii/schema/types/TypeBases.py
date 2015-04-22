""" Base Types to Implement the SII Types.
"""
import re
import datetime
# import base64


# What you will find here...
__all__ = ['MissingValueException',
           'TypeProperty',
           'String',
           'Integer',
           'UnsignedInteger',
           'Decimal',
           'UnsignedDecimal',
           'Enumeration',
           'Date',
           'DateTime']
           # 'Base64Binary']


class MissingValueException(Exception):
    pass


class TypeProperty(object):

    def __init__(self, default=None, optional=False):
        """ Global Properties of derived Types """
        # Yes... very inefficient context switch but in this case good enough.
        self.__values   = {}
        self.__default  = default
        self.__optional = optional

    def __get__(self, inst, owner):
        value = self.__values.get(inst, None)

        if value is None and self.__default is not None:
            value = self.__default

        if not self.__optional and value is None:
            raise MissingValueException("This property is not optional")

        return self.format(value)

    def __set__(self, inst, value):
        self.validate(value)
        self.__values[inst] = value

    def __delete__(self, inst):
        raise RuntimeError("No deletion of this property is allowed")

    def validate(self, value):
        """ (REQUIRED) Validate the value before storing it.
        """
        raise NotImplementedError("Missing concrete Implemtentation")

    def format(self, value):
        """ (OPTIONAL) Takes the stored value and formats it before returning it. Remember that
        it has to be able to deal with 'None' in case so far no value has been yet stored.

        Defaults to pass-through.

        TODO (implement on types)
        """
        return value


class String(TypeProperty):

    def __init__(self, min_length=None, max_length=None, regex=None,
                       default=None, optional=False):
        super().__init__(default=default,
                         optional=optional)

        self.min_length = min_length
        self.max_length = max_length
        self.regex      = regex

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError("Value must be of type string (str)!")

        length = len(value)
        if self.min_length is not None:
            if not length >= self.min_length:
                raise ValueError("String to short ({0} of {1})".format(length, self.min_length))

        if self.max_length is not None:
            if not length <= self.max_length:
                raise ValueError("String to long ({0} over {1})".format(length, self.max_length))

        if self.regex is not None:
            if not re.match(self.regex, value):
                raise ValueError("String '{0}' does not match regex '{1}'".format(value,
                                                                                  self.regex))


class Integer(TypeProperty):

    def __init__(self, min_digits=None, max_digits=None,
                       min_value=None, max_value=None,
                       default=None, optional=False):
        super().__init__(default=default,
                         optional=optional)

        self.min_digits = min_digits
        self.max_digits = max_digits
        self.min_value  = min_value
        self.max_value  = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError("Value must be of type integer (int)!")

        if self.min_digits is not None:
            length = len(str(value))
            if not length >= self.min_digits:
                raise ValueError("Only supplied {0} of {1} "
                                 "minimum required digits".format(length, self.min_digits))

        if self.max_digits is not None:
            length = len(str(value))
            if not length <= self.max_digits:
                raise ValueError("Exceeded maximum allowable digits. Supplied {0} of {1} maximum"
                                 "minimum required digits".format(length, self.max_digits))

        if self.min_value is not None:
            if not value >= self.min_value:
                raise ValueError("Value out of required bounds [{0},{1}]".format(self.min_value,
                                                                                 self.max_value))

        if self.max_value is not None:
            if not value <= self.max_value:
                raise ValueError("Value out of required bounds [{0},{1}]".format(self.min_value,
                                                                                 self.max_value))


class UnsignedInteger(Integer):
    """ Spinoff Integer with additional 'N > 0' check """

    def __init__(self, min_digits=None, max_digits=None,
                       min_value=0, max_value=None,
                       default=None, optional=False):
        if min_value < 0:
            raise ValueError("Minimum value cannot be set below 0, I'm an 'UnsignedInteger' "
                             "remember?")
        super().__init__(min_digits, max_digits, min_value, max_value,
                         default=default, optional=optional)


class Decimal(TypeProperty):

    def __init__(self, min_digits=None, max_digits=None,
                       min_decimals=None, max_decimals=None,
                       min_value=None, max_value=None,
                       default=None, optional=False):
        super().__init__(default=default,
                         optional=optional)

        self.min_digits   = min_digits
        self.max_digits   = max_digits
        self.min_decimals = min_decimals
        self.max_decimals = max_decimals
        self.min_value    = min_value
        self.max_value    = max_value

    def validate(self, value):
        if not isinstance(value, float):
            raise TypeError("Value must be of type decimal/float (float)!")

        digits, decimals = str(value).split('.')
        digits, decimals = len(digits), len(decimals)

        if self.min_digits is not None:
            if not digits >= self.min_digits:
                raise ValueError("Only supplied {0} of {1} "
                                 "minimum required digits".format(digits, self.min_digits))

        if self.max_digits is not None:
            if not digits <= self.max_digits:
                raise ValueError("Exceeded maximum allowable digits. Supplied {0} over {1}"
                                 "digits".format(digits, self.max_digits))

        if self.min_decimals is not None:
            if not decimals >= self.min_decimals:
                raise ValueError("Only supplied {0} of {1} "
                                 "minimum required decimals".format(decimals, self.min_decimals))

        if self.max_decimals is not None:
            if not decimals <= self.max_decimals:
                raise ValueError("Exceeded maximum allowable decimals. Supplied {0} over {1}"
                                 "decimals".format(decimals, self.max_decimals))

        if self.min_value is not None:
            if not value >= self.min_value:
                raise ValueError("Value out of required bounds [{0},{1}]".format(self.min_value,
                                                                                 self.max_value))

        if self.max_value is not None:
            if not value <= self.max_value:
                raise ValueError("Value out of required bounds [{0},{1}]".format(self.min_value,
                                                                                 self.max_value))


class UnsignedDecimal(Decimal):
    """ Spinoff Decimal with additional 'N > 0.0' check """

    def __init__(self, min_digits=None, max_digits=None,
                       min_decimals=None, max_decimals=None,
                       min_value=0, max_value=None,
                       default=None, optional=False):
        if not min_value >= 0:
            raise ValueError("Minimum value cannot be set below 0.0, I'm an 'UnsignedDecimal' "
                             "remember?")
        super().__init__(min_digits, max_digits,
                         min_decimals, max_decimals,
                         min_value, max_value,
                         default=default,
                         optional=optional)


class Enumeration(TypeProperty):

    def __init__(self, *args,
                       default=None, optional=False):
        super().__init__(default=default,
                         optional=optional)

        self.allowed = args

    def validate(self, value):
        if value is not None and value not in self.allowed:
            raise ValueError("Given Value: \"{0}\" "
                             "is not amongst the available options".format(value))


class Date(TypeProperty):

    def __init__(self, min_date=None, max_date=None, formatting=None,
                       default=None, optional=False):
        super().__init__(default=default,
                         optional=optional)

        self.min_date   = min_date
        self.max_date   = max_date
        self.formatting = formatting

    def validate(self, date):
        if not isinstance(date, datetime.date):
            raise TypeError("Value must be of type datetime.date (stdlib)!")

        if self.min_date is not None:
            if not date >= self.min_date:
                raise ValueError("Date out of bounds: {0} below oldest "
                                 "permissible {1}".format(date, self.min_date))

        if self.max_date is not None:
            if not date <= self.max_date:
                raise ValueError("Date out of bounds: {0} above latest "
                                 "permissible {1}".format(date, self.max_date))

    def format(self, date):
        if date is not None:
            if self.format is not None:
                return date.strftime(self.formatting)
            else:
                return str(date)


class DateTime(TypeProperty):

    def __init__(self, min_datetime=None, max_datetime=None, formatting=None,
                       default=None, optional=False):
        super().__init__(default=default,
                         optional=optional)

        self.min_datetime = min_datetime
        self.max_datetime = max_datetime
        self.formatting   = formatting

    def validate(self, datetime):
        if not isinstance(datetime, datetime.datetime):
            raise TypeError("Value must be of type datetime.date (stdlib)!")

        if self.min_datetime is not None:
            if not datetime >= self.min_datetime:
                raise ValueError("DateTime out of bounds: {0} below oldest "
                                 "permissible {1}".format(datetime, self.min_datetime))

        if self.max_datetime is not None:
            if not datetime <= self.max_datetime:
                raise ValueError("DateTime out of bounds: {0} above latest "
                                 "permissible {1}".format(datetime, self.max_datetime))

    def format(self, datetime):
        if datetime is not None:
            if self.format is not None:
                return datetime.strftime(self.formatting)
            else:
                return str(datetime)


# class RawXML(TypeProperty):

#     def __init__(self, xml=None, optional=False):
#         super().__init__(default=xml,
#                          optional=optional)


# class Base64Binary(TypeProperty):

#     def validate(self, bytestr):
#         if not isinstance(bytestr, bytes):
#             raise TypeError("Argument must be of type 'bytes'")

#     def format(self, bytestr):
#         return base64.encode(bytestr)


# class XMLSignatureSHA1withRSA(Base64Binary):

#     __attributes__ = {'algoritmo': 'SHA1withRSA'}
