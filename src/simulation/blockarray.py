import numpy as np
import enum


class BlockArray:
    rows = property(lambda self: self._rows)
    columns = property(lambda self: self._cols)
    positions = property(lambda self: self._positions)
    velocities = property(lambda self: self._velocities)

    def __init__(self, arg1, cols):
        if type(arg1) == np.ndarray:
            self.array = arg1
        else:
            self.array = np.zeros(arg1 * cols * 2)
        self._rows = len(self.array)  // (2 * cols)
        self._cols = cols
        self._positions = _Getter(self, self._rows, self._cols, _GetterType.POSITION)
        self._velocities = _Getter(self, self._rows, self._cols, _GetterType.VELOCITY)


class _GetterType(enum.IntEnum):
    POSITION = 0
    VELOCITY = 1


class _Getter:
    rows = property(lambda self: self._rows)
    columns = property(lambda self: self._cols)

    def __init__(self, parent, rows, columns, getter_type):
        self._parent = parent
        self._rows = rows
        self._cols = columns
        self._offset = int(getter_type)

    def __iter__(self):
        return _BlockArrayIterator(self)

    def __getitem__(self, item):
        i, j = item
        return self._parent.array[2*self._cols*i + 2*j + self._offset]

    def __setitem__(self, key, value):
        i, j = key
        self._parent.array[2*self._cols*i + 2*j + self._offset] = value


class _BlockArrayIterator:
    def __init__(self, getter):
        self._getter = getter
        self._row = -1
        self._col = -1

    def __next__(self):
        self._row = (self._row + 1) % self._getter.rows
        if self._row == 0:
            self._col += 1
        if self._col >= self._getter.columns:
            raise StopIteration()
        return self._getter[self._row, self._col]
