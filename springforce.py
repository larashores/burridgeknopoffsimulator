import numpy as np

from util import get_2d_position, get_2d_velocity


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
            pos, velocity = values[2*i], values[2*i + 1]
            pos_plus = values[2*i + 2]
            results[2*i + 1] = self.spring_constant * (pos_plus + pos_minus - 2*pos) * (1 / self.mass)


        # Left Boundary Condition
        results[1] = self.spring_constant * (values[2] - values[0] - self.spring_length)

        # Right Boundary Condition
        end = values[2*self.num_blocks - 2]
        end_minus_one = values[2*self.num_blocks - 4]
        results[2*self.num_blocks - 1] = self.spring_constant * (end_minus_one - end + self.spring_length)

        return results