from abc import ABCMeta
import collections
import inspect

from saveable.saveablearray import SaveableType


class CompositeMeta(ABCMeta):
    """
    Meta class that keeps track of an ordered list of class attributes to later be used by the Composite class.
    Adds all class attributes of type SaveableType to member __ordered__ of the class __dict__
    """
    @classmethod
    def __prepare__(mcs, name, bases):
        return collections.OrderedDict()

    def __new__(mcs, name, bases, classdict):
        for base in bases:
            if hasattr(base, '__ordered__'):
                for key in base.__ordered__:
                    classdict[key] = base.__dict__[key]
        classdict['__ordered__'] = [key for key in classdict.keys() if
                                    inspect.isclass(classdict[key]) and
                                    issubclass(classdict[key], SaveableType)]
        classdict['__typemap__'] = {key: classdict[key] for key in classdict['__ordered__']}

        return type.__new__(mcs, name, bases, dict(classdict))


class Composite(SaveableType, metaclass=CompositeMeta):
    """
    A Saveable Composite type. This class is meant to be subclassed to easily create new SaveableType's made up of
    other SaveableTypes. For each type the object should hold, simply add a class attribute that is equal to that type.
    Every instance created will have a value of that type. No new instances attributes can be directly added. If the
    SaveableType has a 'get' method, then accessing that attribute will return its get method. If it has a 'set' method
    then setting that attribute will call its set method. Otherwise setting is disallowed

    The bytearray representation of a composite is each bytearray representation of the composite in the order they were
    declared, one after another

    Ex.
    class Composite1(Composite):
        val1 = saveable_int('u32')
        val2 = array('saveable_int('u32'))

        Every Composite1 that is created will have a val1 and val2 attributes of the specified types. val1 = 5 will call
        val1.set(5) but val2 does not have a set so val2 = [4] will cause an Exception


    """
    RETURN_GET = True

    def __init__(self):
        """
        Creates an instance attribute for each type in the class attribute '__ordered__'.
        """
        SaveableType.__init__(self)
        for key, Type in self.__typemap__.items():
            self.__dict__[key] = Type()

    def __setattr__(self, key, value):
        """
        Catches all attribute setting. Only allows the setting if the attribute being set has a 'set' method. If it does
        calls attribute.set(value). Otherwise setting is disallowed
        """
        if key in type(self).__ordered__:
            saveable_type = self.__dict__[key]
            if not callable(getattr(saveable_type, 'set', None)):
                raise ValueError("Cannot assign directly to '{}' ({})".format(key, type(saveable_type)))
            saveable_type.set(value)
        else:
            SaveableType.__setattr__(self, key, value)

    def __getattribute__(self, item):
        """
        Catches all attribute getting. If the attribute defines a 'get' method returns that instead, otherwise just
        returns the attribute
        """
        get_attribute = lambda item: SaveableType.__getattribute__(self, item)
        _dict = get_attribute('__dict__')
        if item not in type(self).__ordered__:
            return get_attribute(item)
        saveable_type = _dict[item]
        if self.RETURN_GET:
            return saveable_type.get() if callable(getattr(saveable_type, 'get', None)) else saveable_type
        else:
            return saveable_type

    def set(self, other):
        if type(other) != type(self):
            raise ValueError('Types do not match {}, {}'.format(type(other), type(self)))
        for attr in other.__ordered__:
            self.__setattr__(attr, other.__getattribute__(attr))

    def load_in_place(self, byte_array, index=0):
        for key in self.__ordered__:
            index = self.__dict__[key].load_in_place(byte_array, index)
        return index

    def to_byte_array(self):
        array_ = bytearray()
        for key in self.__ordered__:
            array_ += self.__dict__[key].to_byte_array()
        return array_

    def __str__(self):
        string = '{'
        for key in self.__ordered__:
            string += '{}: {}, '.format(key, self.__dict__[key])
        string = string[:-1]
        string += '}'
        return string

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for var in self.__ordered__:
            yield self.__dict__[var]

if __name__ == '__main__':
    from saveable.saveableint import saveable_int
    from saveable.saveablearray import array
    from saveable.saveablestring import SaveableString
    from saveable.saveablefloat import SaveableDouble

    class Bar(Composite):
        a = saveable_int('u32')
        b = array(saveable_int('u16'))
        c = SaveableString
        d = SaveableDouble

    c = Bar()
    c.a = 43
    c.b.append(53)
    c.b.append(52)
    c.c = 'adf'
    c.d = 245.131515
    print(c)
    a = c.to_byte_array()
    print(a)
    c.load_in_place(bytes(a), 0)
    print(c)