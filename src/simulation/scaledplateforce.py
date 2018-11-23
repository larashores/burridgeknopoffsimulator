from simulation.blockarray import BlockArray


class ScaledPlateForce:
    def __init__(self, num_rows, num_cols, scaled_length, l):
        self._rows = num_rows
        self._cols = num_cols
        self._l = l
        self._scaled_length = scaled_length

    def __call__(self, values):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        current = BlockArray(values, self._cols)
        results = BlockArray(self._rows, self._cols)

        for i in range(self._rows):
            for j in range(self._cols):
                position = current.positions[i, j]
                results.velocities[i, j] = j * self._scaled_length - position

        return results.array