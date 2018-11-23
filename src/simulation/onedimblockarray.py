import numpy as np
import enum


class OneDimBlockArray:
    columns = property(lambda self: self._cols)
    positions = property(lambda self: self._positions)
    velocities = property(lambda self: self._velocities)

    def __init__(self, arg):
        if type(arg) == np.ndarray:
            self.array = arg
        else:
            self.array = np.zeros(arg * 2)
        self._cols = len(self.array)  // 2
        self._positions = _Getter(self, self._cols, _GetterType.POSITION)
        self._velocities = _Getter(self, self._cols, _GetterType.VELOCITY)


class _GetterType(enum.IntEnum):
    POSITION = 0
    VELOCITY = 1


class _Getter:
    columns = property(lambda self: self._cols)

    def __init__(self, parent, columns, getter_type):
        self._parent = parent
        self._cols = columns
        self._offset = int(getter_type)

    def __iter__(self):
        return _BlockArrayIterator(self)

    def __getitem__(self, j):
        return self._parent.array[2*j + self._offset]

    def __setitem__(self, j, value):
        self._parent.array[2*j + self._offset] = value


class _BlockArrayIterator:
    def __init__(self, getter):
        self._getter = getter
        self._col = -1

    def __next__(self):
        self._col += 1
        if self._col >= self._getter.columns:
            raise StopIteration()
        return self._getter[self._col]
