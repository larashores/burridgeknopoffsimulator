import numpy as np
import burridgeknopoff as bk


class ScaledDifferential:
    def __init__(self, num_rows, num_cols, *, scaled_spring_length, scaled_plate_velocity, alpha, l):
        self._velocity = bk.PositionUpdater(num_rows, num_cols)
        self._spring_force = bk.ScaledSpringForce(num_rows, num_cols, scaled_spring_length, l)
        self._driving_plate_force = bk.ScaledPlateForce(num_rows, num_cols, scaled_spring_length)
        self._frictional_force = bk.ScaledFrictionalForce(num_rows, num_cols, scaled_plate_velocity, alpha)
        self._rows = num_rows
        self._cols = num_cols

    def __call__(self, t, values):
        """
        The first parameter values is a vector with all the values of the system of equations. Since we are splitting a
        system of 2nd order ODEs to 1st order ODEs, values[2n]=x(n) and values[2n+1] = x'(n)

        Function should return a list of values [
        """
        net = np.zeros(self._rows * self._cols * 2)
        self._spring_force(values, net)
        self._frictional_force(values, net)
        self._driving_plate_force(values, net)
        self._velocity(values, net)
        return net