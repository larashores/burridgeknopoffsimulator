from simulation.blockarray import BlockArray
from simulation.onedimblockarray import OneDimBlockArray


class ScaledSpringForce:
    def __init__(self, num_rows, num_columns, scaled_spring_length, l):
        self._rows = num_rows
        self._cols = num_columns
        self._scaled_spring_length = scaled_spring_length
        self._l_squared = l**2
        if num_rows == 1 and num_columns >= 2:
            print('One dimension optimization')
            self.diff = self._one_dimension
        elif num_rows == 1 and num_columns == 1:
            print('One block optimization')
            self.diff = self._one_block
        else:
            self.diff = self._full

    def _full(self, values):
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
                force *= self._l_squared
                results.velocities[i, j] = force
        return results.array

    def _one_dimension(self, values):
        current = OneDimBlockArray(values)
        results = OneDimBlockArray(self._cols)

        pos = current.positions

        results.velocities[0] =  \
            self._l_squared * (pos[1] - pos[0] - self._scaled_spring_length)
        results.velocities[self._cols-1] =  \
            self._l_squared * (pos[self._cols-2] - pos[self._cols-1] + self._scaled_spring_length)

        for j in range(1, self._cols-1):
            results.velocities[j] = self._l_squared * (pos[j-1] + pos[j+1] - 2*pos[j])
        return results.array

    def _one_block(self, values):
        results = OneDimBlockArray(self._cols)
        return results.array