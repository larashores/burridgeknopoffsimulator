from files import util
from src.graphing.graphing import *
import numpy as np


def gutenburg_richter_law(magnitude, a, b):
    return np.e**(a - b * magnitude)


def gutenburg_richter_law_logarthimic(magnitude, a, b):
    return a - b * magnitude


if __name__ == '__main__':
    filenames = util.get_all_file_names('gpdat')
    data = []
    for name in filenames:
        print(f'Loading file: {name}')
        data.append(util.read_data(name))

    num_blocks = []
    distances = []
    for datum in data:
        for slip_event in datum.slip_events:
            num_blocks.append(len(slip_event))
            distances.append(sum(single_slip_event.distance for single_slip_event in slip_event) / len(slip_event))
    graph = Graph(num_blocks, distances, plot_size=2)
    draw(SubPlot(graph, x_label='Number of Slipping Blocks', y_label='Distance Travelled per Block'))

    num_blocks.sort()
    graph = Graph(list(range(len(num_blocks))), num_blocks,  plot_size=2)
    draw(SubPlot(graph, x_label='Event number', y_label='Number of slipping blocks'))
