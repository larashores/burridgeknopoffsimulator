from files import util
from graphing.graphing import *
import numpy as np
import bisect
import utilities
from dataclasses import dataclass, field
from typing import Sequence
from numbers import Real


def gutenburg_richter_law(magnitude, a, b):
    return np.e**(a - b * magnitude)


def gutenburg_richter_law_logarthimic(magnitude, a, b):
    return a - b * magnitude


@dataclass
class PartitionAnalysisData:
    event_magnitudes: np.ndarray = None
    events_of_at_least_magnitude: np.ndarray = None
    log_events_of_at_least_magnitude: np.ndarray = None
    b_values: Sequence[Real] = field(default_factory=list)


def make_data(partition):
    data = PartitionAnalysisData()
    magnitudes = []
    for slip_event in partition.slip_events:
        distance = sum(single_slip_event.distance for single_slip_event in slip_event)
        if distance > 0 and len(slip_event) < (partition.run_info.rows * partition.run_info.cols):
            magnitudes.append(np.log(distance))
    data.event_magnitudes = np.array(sorted(magnitudes))
    magnitude_range = np.linspace(data.event_magnitudes[0], data.event_magnitudes[-1], 100)
    data.events_of_at_least_magnitude = np.empty(len(magnitude_range))
    for ind, magnitude in enumerate(magnitude_range):
        data.events_of_at_least_magnitude[ind] = sum((lambda x: x >= magnitude)(x) for x in data.event_magnitudes)
    data.log_events_of_at_least_magnitude = np.log(data.events_of_at_least_magnitude)
    for fit in partition.fit_list:
        start_ind = bisect.bisect_left(magnitude_range, fit.fit_start)
        end_ind = bisect.bisect_right(magnitude_range, fit.fit_end)
        fit_range = slice(start_ind, end_ind)
        try:
            linear_values, _ = utilities.fit_func(gutenburg_richter_law, magnitude_range,
                                                  data.events_of_at_least_magnitude, limits=fit_range)
            log_values, _ = utilities.fit_func(gutenburg_richter_law_logarthimic, magnitude_range,
                                               data.log_events_of_at_least_magnitude, limits=fit_range)
            data.b_values.append(log_values[1])
        except TypeError:
            continue
    return data


if __name__ == '__main__':
    filenames = util.get_all_file_names('gpdat')
    data = []
    for name in filenames:
        print(f'Loading file: {name}')
        data.append(util.read_data(name))

    num_cols = []
    num_cols2 = []
    b_values = []
    num_blocks = []
    fraction_blocks = []
    distances = []
    for datum in data:
        for slip_event in datum.slip_events:
            if not len(slip_event):
                continue
            is_edge = any(sse.col == 0 or sse.col == datum.run_info.cols - 1 for sse in slip_event)
            if is_edge:
                continue
            num_cols2.append(datum.run_info.cols)
            num_blocks.append(len(slip_event))
            fraction_blocks.append(len(slip_event) / (datum.run_info.rows * datum.run_info.cols))
            distances.append(sum(single_slip_event.distance for single_slip_event in slip_event) / len(slip_event))
        analysis_data = make_data(datum)
        num_cols.extend(datum.run_info.cols for _ in range(len(analysis_data.b_values)))
        b_values.extend(analysis_data.b_values)
        print(f'Cols: {datum.run_info.cols} bs: {analysis_data.b_values}')
    graph = Graph(fraction_blocks, distances, plot_size=2)
    draw(SubPlot(graph, x_label='Fraction of Slipping Blocks', y_label='Distance Travelled per Block'))

    fraction_blocks.sort()
    graph = Graph(list(range(len(fraction_blocks))), fraction_blocks, plot_size=2)
    draw(SubPlot(graph, x_label='Event number', y_label='Fraction of Slipping Blocks'))

    fraction_blocks.sort()
    graph = Graph(num_cols2, num_blocks, plot_size=2)
    draw(SubPlot(graph, x_label='Number of columns', y_label='Number of Slipping Blocks'))

    graph = Graph(num_cols, b_values, plot_size=2)
    draw(SubPlot(graph, x_label='Number of Columns', y_label='B-value'))
