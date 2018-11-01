import numpy as np

from physicalconstants import g
from graphing.graphing import *
from simulation.blockarray import BlockArray
import burridgeknopoff as bk

epsilon = 1e-3


def _friction_force(velocity, static_coefficient, kinetic_coefficient, mass):
    cutoff = static_coefficient * mass * g
    if velocity > epsilon:
        return - 1 / (kinetic_coefficient * velocity + (1 / cutoff))
    elif velocity < -epsilon:
        return - 1 / (kinetic_coefficient * velocity - (1 / cutoff))
    else:
        y1 =   1 / (kinetic_coefficient * epsilon + (1 / cutoff))
        y2 = - 1 / (kinetic_coefficient * epsilon + (1 / cutoff))
        return (y2-y1)*(velocity+epsilon)/(2*epsilon) + y1


class FrictionalForce:
    def __init__(self, num_rows, num_cols, static_coefficient, kinetic_coefficient, plate_velocity, mass):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.static_coefficient = static_coefficient
        self.kinetic_coefficient = kinetic_coefficient
        self.plate_velocity = plate_velocity
        self.mass = mass

    def __call__(self, values):
        current = BlockArray(values, self.num_cols)
        results = BlockArray(self.num_rows, self.num_cols)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                results.velocities[i, j] = bk.friction_force(self.plate_velocity + current.velocities[i, j],
                                                             self.static_coefficient,
                                                             self.kinetic_coefficient,
                                                             self.mass) * (1 / self.mass)
        return results.array


if __name__ == '__main__':
    xs = np.linspace(-.05, .05, 1000)
    ys = np.array(list(map(lambda x: _friction_force(x, 1.0 / g, 50, 1), xs)))
    graph = Graph(xs, ys, plot_type='-', legend_label='$k $m$={}, $\mu_s={}, $\mu_k={}'.format(1, 1, 1))
    draw(SubPlot(graph, x_label='Velocity', y_label='Frictional Force'),
         title='Velocity Dependent Frictional Force')
