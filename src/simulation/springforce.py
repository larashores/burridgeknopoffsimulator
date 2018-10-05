from simulation.blockarray import BlockArray

class SpringForce:
    def __init__(self, num_rows, num_columns, spring_constant, spring_length, mass):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.spring_constant = spring_constant
        self.spring_length = spring_length
        self.mass = mass

    def __call__(self, values):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        current = BlockArray(values, self.num_columns)
        results = BlockArray(self.num_rows, self.num_columns)

        positions = current.positions

        for i in range(0, self.num_rows):
            for j in range(0, self.num_columns):
                cur = positions[i, j]

                force = 0
                if (i - 1) >= 0:
                    force += positions[i-1, j] - cur
                if (i + 1) < self.num_rows:
                    force += positions[i+1, j] - cur
                if (j - 1) >= 0:
                    force += (positions[i, j-1] - cur + self.spring_length)
                if (j + 1) < self.num_columns:
                    force += (positions[i, j+1] - cur - self.spring_length)
                force *= (self.spring_constant / self.mass)
                results.velocities[i, j] = force
        return results.array