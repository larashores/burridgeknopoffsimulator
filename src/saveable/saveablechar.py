import struct

from saveable.saveabletype import SaveableType


class SaveableChar(SaveableType):
    def __init__(self, value=''):
        self._value = value

    def __str__(self):
        return self._value

    def set(self, value):
        if len(value) != 1:
            raise ValueError('Cannot set char to more than one character')
        self._value = value

    def get(self):
        return self._value

    def load_in_place(self, byte_array, index=0):
        self._value = ''
        char = struct.unpack('c', bytes((byte_array[index],)))
        self._value += char[0].decode('ascii')
        return index + 1

    def to_byte_array(self):
        array = bytearray()
        p_char = int.from_bytes(struct.pack('c', self._value[0].encode('ascii')), byteorder='big')
        array.append(p_char)
        return array
