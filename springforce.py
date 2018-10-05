import numpy as np

from util import TwoDimBlockArray


class OneDimSpringForce:
    def __init__(self, num_blocks, spring_constant, spring_length, mass):
        self.num_blocks = num_blocks
        self.spring_constant = spring_constant
        self.spring_length = spring_length
        self.mass = mass

    def __call__(self, values):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        results = np.zeros(len(values))

        for i in range(1, self.num_blocks - 1):
            pos_minus = values[2*i - 2]
            pos = values[2*i]
            pos_plus = values[2*i + 2]
            results[2*i + 1] = self.spring_constant * (pos_plus + pos_minus - 2*pos) * (1 / self.mass)


        # Left Boundary Condition
        results[1] = self.spring_constant * (values[2] - values[0] - self.spring_length)

        # Right Boundary Condition
        end = values[2*self.num_blocks - 2]
        end_minus_one = values[2*self.num_blocks - 4]
        results[2*self.num_blocks - 1] = self.spring_constant * (end_minus_one - end + self.spring_length)

        return results


class TwoDimSpringForce:
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
        current = TwoDimBlockArray(values, self.num_columns)
        results = TwoDimBlockArray(self.num_rows, self.num_columns)

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