import numpy as np

def get_1d_position(values, i):
    return values[2*i]

def get_1d_velocity(values, i):
    return values[2*i + 1]

def get_2d_position(num_columns, i, j):
    return 2*num_columns*i + 2*j

def get_2d_velocity(num_columns, i, j):
    return 2*num_columns*i + 2*j + 1

class TwoDimBlockArray:
    class _PositionGetter:
        def __init__(self, parent, rows, columns):
            self.parent = parent
            self.num_rows = rows
            self.num_columns = columns

        def __getitem__(self, item):
            i, j = item
            try:
                return self.parent.array[2*self.num_columns*i + 2*j]
            except:
                print(i, j, self.num_rows, self.num_columns)
                raise

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
