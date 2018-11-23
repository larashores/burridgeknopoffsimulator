import numpy as np

from graphing.graphing import *
from simulation.blockarray import BlockArray
import burridgeknopoff as bk

epsilon = 1e-3


def _friction_force(velocity, alpha):
    v = 2*alpha*velocity
    if velocity < -epsilon:
        return - 1 / (2*alpha*velocity - 1)
    elif velocity > epsilon:
        return - 1 / (2*alpha*velocity + 1)
    else:
        y1 = - 1 / (-2*alpha*velocity*epsilon - 1)
        y2 = - 1 / (2*alpha*velocity*epsilon + 1)
        return (y2-y1)*(velocity+epsilon)/(2*epsilon) + y1


class ScaledFrictionalForce:
    def __init__(self, num_rows, num_cols, scaled_plate_velocity, alpha):
        self._rows = num_rows
        self._cols = num_cols
        self._scaled_plate_velocity = scaled_plate_velocity
        self._alpha = alpha

    def __call__(self, values):
        current = BlockArray(values, self._cols)
        results = BlockArray(self._rows, self._cols)

        for i in range(self._rows):
            for j in range(self._cols):
                results.velocities[i, j] = _friction_force(self._scaled_plate_velocity + current.velocities[i, j],
                                                           self._alpha)
        return results.array


if __name__ == '__main__':
    xs = np.linspace(-.5, .5, 1000)
    ys = np.array(list(map(lambda x: _friction_force(x, 2.5), xs)))
    graph = Graph(xs, ys, plot_type='-', legend_label=r'$\alpha$={}'.format(2.5))
    draw(SubPlot(graph, x_label='Velocity', y_label='Frictional Force'),
         title='Velocity Dependent Frictional Force')