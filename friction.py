from physicalconstants import g
import numpy as np


class OneDimFrictionalForce:
    def __init__(self, num_blocks, static_coefficient, kinetic_coefficient, mass):
        self.num_blocks = num_blocks
        self.kinetic_coefficient = kinetic_coefficient
        self.cutoff = static_coefficient * mass * g

    def __call__(self, values):
        results = np.zeros(self.num_blocks * 2)
        for i in range(0, self.num_blocks - 1):
            results[2*i + 1] = - 1 / (self.kinetic_coefficient * values[2*i + 1] + (1 / self.cutoff))
        return results