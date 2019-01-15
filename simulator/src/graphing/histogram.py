import numpy as np


class Histogram:
    def __init__(self, values, binwidth=None, num_bins=None):
        if binwidth is not None:
            self.bins = np.arange(min(values), max(values) + binwidth, binwidth)
        elif num_bins is not None:
            self.bins = num_bins
        else:
            self.bins = None
        self.values = values