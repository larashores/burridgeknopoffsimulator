from physicalconstants import g
import numpy as np


def linear_kinetic_friction(spring_force, static_coefficient, kinetic_coefficient, mass):
    cutoff = static_coefficient * mass * g
    friction = kinetic_coefficient * mass * g
    if spring_force >= cutoff:
        return -friction
    elif spring_force <= -cutoff:
        return friction
    else:
        return 0


def velocity_dependent_friction(velocity, static_coefficient, kinetic_coefficient, mass):
    cutoff = static_coefficient * mass * g
    return -1 / (kinetic_coefficient * velocity + (1 / cutoff))


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