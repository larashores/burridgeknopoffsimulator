from src.simulation.blockarray import BlockArray


class DrivingPlateForce:
    def __init__(self, num_rows, num_cols, spring_constant, spring_length, plate_velocity, mass):
        self.num_rows = num_rows
        self.num_columns = num_cols
        self.spring_constant = spring_constant
        self.spring_length = spring_length
        self.plate_velocity = plate_velocity
        self.mass = mass

    def __call__(self, values, time):
        """
        values in form [x0, v0, x1, v1, ..., xN, vN]
        """
        current = BlockArray(values, self.num_columns)
        results = BlockArray(self.num_rows, self.num_columns)

        for i in range(self.num_rows):
            for j in range(self.num_columns):
                position = current.positions[i, j]
                results.velocities[i, j] = (j * self.spring_length + self.plate_velocity * time - position) \
                                           * (self.spring_constant / self.mass)

        return results.array