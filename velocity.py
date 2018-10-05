from util import TwoDimBlockArray


class OneDimVelocity:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols

    def __call__(self, values):
        current = TwoDimBlockArray(values, self.num_cols)
        results = TwoDimBlockArray(self.num_rows, self.num_cols)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                results.positions[i, j] = current.velocities[i, j]

        return results.array
