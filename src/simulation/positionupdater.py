from simulation.blockarray import BlockArray


class PositionUpdater:
    def __init__(self, num_rows, num_cols):
        self._rows = num_rows
        self._cols = num_cols

    def __call__(self, values):
        current = BlockArray(values, self._cols)
        results = BlockArray(self._rows, self._cols)

        for i in range(self._rows):
            for j in range(self._cols):
                results.positions[i, j] = current.velocities[i, j]

        return results.array
