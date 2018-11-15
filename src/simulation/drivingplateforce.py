from simulation.blockarray import BlockArray


class DrivingPlateForce:
    def __init__(self, num_rows, num_cols, spring_constant, spring_length, mass):
        self._rows = num_rows
        self._cols = num_cols
        self._spring_constant = spring_constant
        self._spring_length = spring_length
        self._mass = mass

    def __call__(self, values):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        current = BlockArray(values, self._cols)
        results = BlockArray(self._rows, self._cols)

        for i in range(self._rows):
            for j in range(self._cols):
                position = current.positions[i, j]
                results.velocities[i, j] = (j * self._spring_length - position) * (self._spring_constant / self._mass)

        return results.array