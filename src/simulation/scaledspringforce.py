from simulation.blockarray import BlockArray

class ScaledSpringForce:
    def __init__(self, num_rows, num_columns, scaled_spring_length, l):
        self._rows = num_rows
        self._cols = num_columns
        self._scaled_spring_length = scaled_spring_length
        self._l = l

    def __call__(self, values):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        current = BlockArray(values, self._cols)
        results = BlockArray(self._rows, self._cols)

        positions = current.positions

        for i in range(0, self._rows):
            for j in range(0, self._cols):
                cur = positions[i, j]

                force = 0
                if (i - 1) >= 0:
                    force += positions[i-1, j] - cur
                if (i + 1) < self._rows:
                    force += positions[i+1, j] - cur
                if (j - 1) >= 0:
                    force += (positions[i, j-1] - cur + self._scaled_spring_length)
                if (j + 1) < self._cols:
                    force += (positions[i, j+1] - cur - self._scaled_spring_length)
                force *= self._l**2
                results.velocities[i, j] = force
        return results.array