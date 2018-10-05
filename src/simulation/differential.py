from src.simulation.drivingplateforce import DrivingPlateForce
from src.simulation.frictionalforce import FrictionalForce
from src.simulation.positionupdater import PositionUpdater
from src.simulation.springforce import SpringForce


class Differential:
    def __init__(self, num_rows, num_cols, *,
                 block_spring_constant, plate_spring_constant, static_friction, kinetic_friction, plate_velocity,
                 spring_length, mass):
        self.velocity = PositionUpdater(num_rows, num_cols)
        self.spring_force = SpringForce(num_rows, num_cols, block_spring_constant, spring_length, mass)
        self.frictional_force = FrictionalForce(num_rows, num_cols, static_friction, kinetic_friction, mass)
        self.driving_plate_force = DrivingPlateForce(num_rows, num_cols,  plate_spring_constant, spring_length,
                                                     plate_velocity, mass)

    def __call__(self, t, values):
        """
        The first parameter values is a vector with all the values of the system of equations. Since we are splitting a
        system of 2nd order ODEs to 1st order ODEs, values[2n]=x(n) and values[2n+1] = x'(n)

        Function should return a list of values [
        """
        spring_force = self.spring_force(values)
        friction_force = self.frictional_force(values)
        plate_force = self.driving_plate_force(values, t)
        new_positions = self.velocity(values)
        net = spring_force + new_positions + friction_force + plate_force
        return net