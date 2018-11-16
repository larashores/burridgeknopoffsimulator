from saveable.saveabletype import SaveableType
from saveable.saveableint import U16
from saveable.saveablestring import SaveableString
from saveable.saveablearray import array
import numpy as np
import functools
from operator import mul


class _IntArray(array(U16)):
    pass


def ndarray(shape, int_type=U16):
    """
    A saveable array type that stores numpy arrays of numeric types

    Args:
        array_type: The Saveable object type to store in the array

    Returns:
        A Saveable array type
    """

    class SaveableNdArray(SaveableType):
        def __init__(self):
            SaveableType.__init__(self)
            self._array = np.zeros(shape)

        def get(self):
            return self._array

        def set(self, value):
            if not isinstance(value, np.ndarray):
                raise ValueError('Value must be of type ndarray, not {}'.format(type(value)))
            self._array = value

        def load_in_place(self, byte_array, index=0):
            data_type, index = SaveableString.from_byte_array(byte_array, index)
            size, index = int_type.from_byte_array(byte_array, index)
            self._array, index = np.frombuffer(byte_array, data_type.get(), size.get(), index), \
                                 index + self._array.nbytes
            size_array, index = _IntArray.from_byte_array(byte_array, index)
            self._array = np.reshape(self._array, [value.get() for value in size_array])
            return index + self._array.nbytes

        def to_byte_array(self):
            _array = SaveableString(str(self._array.dtype)).to_byte_array()
            _array += int_type(functools.reduce(mul, self._array.shape, 1)).to_byte_array()
            _array += self._array.tobytes()
            size_array = _IntArray()
            for value in self._array.shape:
                size_array.append(value)
            _array += size_array.to_byte_array()
            return _array

    return SaveableNdArray


if __name__ == '__main__':
    ArrayType = ndarray((2, 10))
    a = ArrayType()
    for i in range(10):
        a.get()[0][i] = i
        a.get()[1][i] = i * 2
    print(a.get())
    b = a.to_byte_array()
    print(b)
    a.load_in_place(b)
    print(a.get())
