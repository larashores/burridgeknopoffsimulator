import struct

from saveable.saveabletype import SaveableType


class SaveableChar(SaveableType):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return self.value

    def set(self, value):
        if len(value) != 1:
            raise ValueError('Cannot set char to more than one character')
        self.value = value

    def get(self):
        return self.value

    def load_in_place(self, byte_array):
        self.value = ''
        char = struct.unpack('c', bytes((byte_array[0],)))
        self.value += char[0].decode('ascii')
        byte_array.pop(0)

    def to_byte_array(self):
        array = bytearray()
        p_char = int.from_bytes(struct.pack('c', self.value[0].encode('ascii')), byteorder='big')
        array.append(p_char)
        return array
