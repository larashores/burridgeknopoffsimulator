import numpy as np


class OneDimDrivingPlate:
    def __init__(self, num_blocks, spring_constant, spring_length, plate_velocity, mass):
        self.num_blocks = num_blocks
        self.spring_constant = spring_constant
        self.spring_length = spring_length
        self.plate_velocity = plate_velocity
        self.mass = mass

    def __call__(self, values, time):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        results = np.zeros(len(values))

        for i in range(0, self.num_blocks):
            position, velocity = values[2*i], values[2*i + 1]
            results[2*i + 1] = self.spring_constant * (i * self.spring_length + self.plate_velocity * time - position) \
                               * (1 / self.mass)

        return results