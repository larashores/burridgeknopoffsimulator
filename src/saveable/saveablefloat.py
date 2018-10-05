from saveable.saveabletype import SaveableType

import enum
import struct


def create_floating_point(num_bytes, fmt):

    class _SaveableFloatingPoint(SaveableType):
        """
        A saveable float type that can be saved as a c-type specified in struct
        """

        def __init__(self, value=0.0):
            self.value = value

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return self.value.__repr__()

        def get(self):
            return self.value

        def set(self, value):
            if not isinstance(value, float):
                raise ValueError("Value not int! {}".format(value))
            self.value = value

        def load_in_place(self, byte_array, index=0):
            data = byte_array[index:index + num_bytes]
            self.value = struct.unpack('<'+fmt, data)[0]
            return index + num_bytes

        def to_byte_array(self):
            return bytearray(struct.pack('<'+fmt, self.value))

    return _SaveableFloatingPoint

SaveableFloat = create_floating_point(4, 'f')
SaveableDouble = create_floating_point(8, 'd')