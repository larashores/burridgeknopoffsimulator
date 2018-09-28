from physicalconstants import g
import numpy as np

from src.graphing.graphing import *

epsilon = 1e-2


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



class OneDimFrictionalForce:
    def __init__(self, num_blocks, static_coefficient, kinetic_coefficient, mass):
        self.num_blocks = num_blocks
        self.static_coefficient = static_coefficient
        self.kinetic_coefficient = kinetic_coefficient
        self.mass = mass

    def __call__(self, values):
        results = np.zeros(self.num_blocks * 2)
        for i in range(0, self.num_blocks):
            results[2*i + 1] = _friction_force(values[2*i + 1],
                                               self.static_coefficient, self.kinetic_coefficient, self.mass) * (1 / self.mass)
        return results


if __name__ == '__main__':
    xs = np.linspace(-5, 5, 1000)
    ys = np.array(list(map(lambda x: _friction_force(x, 0.03, 10, 1), xs)))
    graph = Graph(xs, ys, plot_type='-', legend_label='$k $m$={}, $\mu_s={}, $\mu_k={}'.format(1, 1, 1))
    draw(SubPlot(graph, x_label='Velocity', y_label='Frictional Force'),
         title='Velocity Dependent Frictional Force')
