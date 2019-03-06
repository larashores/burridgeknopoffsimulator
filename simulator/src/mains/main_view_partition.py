from files import util
from src.graphing.graphing import *
import utilities
import numpy as np


def gutenburg_richter_law(magnitude, a, b):
    return np.e**(a - b * magnitude)


def gutenburg_richter_law_logarthimic(magnitude, a, b):
    return a - b * magnitude


if __name__ == '__main__':
    file = util.get_single_file_name('pdat', 'gpdat')
    print('Loading file', file)
    data = util.read_data(file)

    print('Generating Distance Data')
    magnitudes = []
    for slip_event_data in data.slip_events:
        distance = 0
        for single_slip_event in slip_event_data:
            distance += single_slip_event.distance
        if distance > 0:
            magnitudes.append(np.log(distance))

    print('Analyzing data')
    event_magnitudes = np.array(sorted(magnitudes))
    magnitude_range = np.linspace(event_magnitudes[0], event_magnitudes[-1], 200)
    events_of_at_least_magnitude = np.empty(len(magnitude_range))
    for ind, magnitude in enumerate(magnitude_range):
        events_of_at_least_magnitude[ind] = sum((lambda x: x >= magnitude)(x) for x in event_magnitudes)

    print('Making graphs')
    title = '{}x{}'.format(data.run_info.rows, data.run_info.cols)
    options = {'line_width': 2, 'plot_type': '-'}
    subplot_options = {'legend_size': 14}

    start_ind = 47
    end_ind = -105
    values, _ = utilities.fit_func(gutenburg_richter_law, limits=(start_ind, end_ind),
                                   xs=magnitude_range, ys=events_of_at_least_magnitude)
    logarithmic_values, _ = utilities.fit_func(gutenburg_richter_law_logarthimic, limits=(start_ind, end_ind),
                                               xs=magnitude_range, ys=np.log(events_of_at_least_magnitude))
    gutenburg_x = magnitude_range[start_ind:end_ind]
    gutenburg_y = gutenburg_richter_law(gutenburg_x, *values)
    gutenburg_y_logarithmic = gutenburg_richter_law_logarthimic(gutenburg_x, *logarithmic_values)
    label = 'a={:.1f} b={:.3f}'

    overlayed_law = Graph(gutenburg_x, gutenburg_y, legend_label=label.format(*values), **options)
    overlayed_law_logarithmic = Graph(gutenburg_x, gutenburg_y_logarithmic,
                                      legend_label=label.format(*logarithmic_values), **options)

    all_events_graph = Graph(event_magnitudes, list(range(len(event_magnitudes))), plot_size=3)
    linear_graph = Graph(magnitude_range, events_of_at_least_magnitude, **options)
    logarithmic_graph = Graph(magnitude_range, np.log(events_of_at_least_magnitude), **options)

    draw(SubPlot(all_events_graph, y_label='N (Sorted Event #)', x_label='M (Magnitude)',
                 **subplot_options), title=title)
    draw(SubPlot(linear_graph, overlayed_law,
                 x_label='M (Magnitude)', y_label='N (# of events where magnitude > M)',
                 **subplot_options), title=title)
    draw(SubPlot(logarithmic_graph,  overlayed_law_logarithmic,
                 x_label='M (Magnitude)', y_label='log$_{10}$(N)',
                 **subplot_options), title=title)
