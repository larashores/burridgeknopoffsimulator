from saveable.saveabletype import SaveableType
import struct


def saveable_int(int_type):
    """
    Returns a class type for a saveable object of an integer of a specific c-type

    Args:
        int_type: The type of integer. Can be u8, s8, u16, s16, u32, s32

    Returns:
        A Saveable class type
    """
    str_to_type = {'u8': (8, False), 's8': (8, True),
                   'u16': (16, False), 's16': (16, True),
                   'u32': (32, False), 's32': (32, True)}
    str_to_range = {'u8': (0, 255), 's8': (-128, 127),
                    'u16': (0, 65535), 's16': (-32768, 32767),
                    'u32': (0, 429496729), 's32': (-2147483648, 2147483647)}
    if int_type not in str_to_type.keys():
        raise ValueError('Not a valid string type: ' + str(int_type))

    class SaveableInt(SaveableType):
        """
        A saveable int type that can be saved as a c-type specified in struct
        """

        def __init__(self, value=0):
            self.value = value

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return self.value.__repr__()

        def get(self):
            return self.value

        def set(self, value):
            if not isinstance(value, int):
                raise ValueError("Value not int! {}".format(value))
            _min, _max = str_to_range[int_type]
            if value < _min:
                raise ValueError("Int {} is too small. Min={}".format(value, _min))
            if value > _max:
                raise ValueError("Int {} is too large. Max={}".format(value, _max))
            self.value = value

        def load_in_place(self, byte_array):
            self.value = unpack_integer(byte_array, *str_to_type[int_type])

        def to_byte_array(self):
            array = bytearray()
            pack_integer(array, self.value, *str_to_type[int_type])
            return array

    return SaveableInt


def unpack_integer(data, size, signed):
    """
    Purpose: Returns a int of size 'size' from front of packed data. Will strip
             off the int from the data
    Inputs:
        data:   (bytearray) Packed binary data with a u32 type in front
        size:   (int)    Integer size in bits
        signed: (bool)   True if signed, False if unsigned
    Output:
        (int)   The integer
        (bytes) New data with integer stripped off
    """
    if size == 32:
        fmt = 'I'
    elif size == 16:
        fmt = 'H'
    elif size == 8:
        fmt = 'B'
    else:
        raise ValueError('Size Invalid')
    if signed:
        fmt = fmt.lower()
    b_int = data[:(size//8)]
    for x in range(size//8):
        data.pop(0)
    _int = struct.unpack('<'+fmt, b_int)[0]
    return _int


def pack_integer(data, _int, size, signed):
    """
    Purpose: Packs an integer as binary data
    Inputs:
        data:   (bytearray) Bytearray that may or may not already have data
                            packed
        _int:   (int)       The integer to be packed
        size:   (int)       Integer size in bits
        signed: (bool)      True if signed, False if unsigned
    """
    if size == 32:
        fmt = 'I'
    elif size == 16:
        fmt = 'H'
    elif size == 8:
        fmt = 'B'
    else:
        raise ValueError('Size Invalid')
    if signed:
        fmt = fmt.lower()
    p_int = bytearray(struct.pack('<'+fmt, _int))
    for byte in p_int:
        data.append(byte)


U8 = saveable_int('u8')
U16 = saveable_int('u16')
U32 = saveable_int('u32')
S8 = saveable_int('s8')
S16 = saveable_int('s16')
S32 = saveable_int('s32')