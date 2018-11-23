from simulation.scaledplateforce import ScaledPlateForce
from simulation.scaledfrictionforce import ScaledFrictionalForce
from simulation.positionupdater import PositionUpdater
from simulation.scaledspringforce import ScaledSpringForce


class ScaledDifferential:
    def __init__(self, num_rows, num_cols, *, scaled_spring_length, scaled_plate_velocity, alpha, l):
        self._velocity = PositionUpdater(num_rows, num_cols)
        self._spring_force = ScaledSpringForce(num_rows, num_cols, scaled_spring_length, l)
        self._driving_plate_force = ScaledPlateForce(num_rows, num_cols, scaled_spring_length)
        self._frictional_force = ScaledFrictionalForce(num_rows, num_cols, scaled_plate_velocity, alpha)

    def __call__(self, t, values):
        """
        The first parameter values is a vector with all the values of the system of equations. Since we are splitting a
        system of 2nd order ODEs to 1st order ODEs, values[2n]=x(n) and values[2n+1] = x'(n)

        Function should return a list of values [
        """
        spring_force = self._spring_force.diff(values)
        friction_force = self._frictional_force(values)
        plate_force = self._driving_plate_force(values)
        new_positions = self._velocity(values)
        net = spring_force + new_positions + friction_force + plate_force
        return net