from saveable.saveabletype import SaveableType

import enum
import struct
import numbers


def create_floating_point(num_bytes, fmt):

    class _SaveableFloatingPoint(SaveableType):
        """
        A saveable float type that can be saved as a c-type specified in struct
        """

        def __init__(self, value=0.0):
            self._value = value

        def __str__(self):
            return str(self._value)

        def __repr__(self):
            return self._value.__repr__()

        def get(self):
            return self._value

        def set(self, value):
            if not isinstance(value, numbers.Number):
                raise ValueError("Value not float! {}".format(value))
            self._value = value

        def load_in_place(self, byte_array, index=0):
            data = byte_array[index:index + num_bytes]
            self._value = struct.unpack('<'+fmt, data)[0]
            return index + num_bytes

        def to_byte_array(self):
            return bytearray(struct.pack('<'+fmt, self._value))

    return _SaveableFloatingPoint

SaveableFloat = create_floating_point(4, 'f')
SaveableDouble = create_floating_point(8, 'd')