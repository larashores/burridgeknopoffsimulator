import struct

from saveable.saveabletype import SaveableType
from saveable.saveableint import U32


class SaveableString(SaveableType):
    def __init__(self, value=''):
        self._value = value

    def __str__(self):
        return self._value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

    def load_in_place(self, byte_array, index=0):
        self._value = ''
        length, index = U32.from_byte_array(byte_array, index)
        for _ in range(length.get()):
            char = struct.unpack('c', bytes((byte_array[index],)))
            self._value += char[0].decode('ascii')
            index += 1
        return index

    def to_byte_array(self):
        length = U32()
        length.set(len(self._value))
        array = length.to_byte_array()
        for char in list(self._value):
            p_char = int.from_bytes(struct.pack('c', char.encode('ascii')), byteorder='big')
            array.append(p_char)
        return array
