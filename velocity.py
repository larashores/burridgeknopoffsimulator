import numpy as np


class OneDimVelocity:
    def __init__(self, num_blocks):
        self.num_blocks = num_blocks

    def __call__(self, values):
        results = np.zeros(self.num_blocks * 2)
        for i in range(0, self.num_blocks):
            results[2*i] = values[2*i + 1]
        return results
