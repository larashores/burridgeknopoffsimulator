import numpy as np

class BlockArray:
    class _PositionGetter:
        def __init__(self, parent, rows, columns):
            self.parent = parent
            self.num_rows = rows
            self.num_columns = columns

        def __getitem__(self, item):
            i, j = item
            return self.parent.array[2*self.num_columns*i + 2*j]

        def __setitem__(self, key, value):
            i, j = key
            self.parent.array[2*self.num_columns*i + 2*j] = value

    class _VelocityGetter:
        def __init__(self, parent, rows, columns):
            self.parent = parent
            self.num_rows = rows
            self.num_columns = columns

        def __getitem__(self, item):
            i, j = item
            return self.parent.array[2*self.num_columns*i + 2*j + 1]

        def __setitem__(self, key, value):
            i, j = key
            self.parent.array[2*self.num_columns*i + 2*j + 1] = value

    def __init__(self, arg1, cols):
        if type(arg1) == np.ndarray:
            self.array = arg1
        else:
            self.array = np.zeros(arg1 * cols * 2)
        self.rows = len(self.array)  // (2 * cols)
        self.cols = cols
        self.positions = self._PositionGetter(self, self.rows, self.cols)
        self.velocities = self._VelocityGetter(self, self.rows, self.cols)
