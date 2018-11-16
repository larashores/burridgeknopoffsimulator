import enum


from saveable.saveabletype import SaveableType
from saveable.saveableint import U16


def saveable_enum(enum_type, int_type=U16):
    if not issubclass(enum_type, enum.Enum):
        raise ValueError('Argument must be int enum:', enum_type)

    class SaveableEnum(SaveableType):
        def __init__(self):
            """
            Creates an instance attribute for each type in the class attribute '__ordered__'.
            """
            SaveableType.__init__(self)
            self._value = list(enum_type.__members__.values())[0]

        def get(self):
            return self._value

        def set(self, value):
            if not isinstance(value, enum_type):
                raise ValueError('Value must be enum type of {}'.format(enum_type))
            self._value = value

        def to_byte_array(self):
            position = list(enum_type.__members__.keys()).index(self._value.name)
            return int_type(position).to_byte_array()

        def load_in_place(self, byte_array, index=0):
            position, index = int_type.from_byte_array(byte_array, index)
            self._value = list(enum_type.__members__.values())[position.get()]
            return index

    return SaveableEnum


if __name__ == '__main__':
    class MyEnum(enum.Enum):
        A = 0
        B = 2

    MySaveableEnum = saveable_enum(MyEnum)
    a = MySaveableEnum()
    print(a.get())
    a.set(MyEnum.B)
    data = a.to_byte_array()
    b, index = MySaveableEnum.from_byte_array(data)
    print(b.get())