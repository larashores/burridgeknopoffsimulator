from files import util
from src.graphing.graphing import *
import utilities
import numpy as np


if __name__ == '__main__':
    file = util.get_file_name('pdat')
    data = util.read_data(file)

    start = 26
    end = -32
    print(data.magnitudes_of_at_least[start], data.magnitudes_of_at_least[end])
    at_least = data.magnitudes_of_at_least
    log_amount = np.log10(data.amount_of_at_least)

    gutenburg = lambda magnitude, a, b: 10**(a - b * magnitude)
    linear_gutenburg = lambda magnitude, a, b: a - b * magnitude
    values, _ = utilities.fit_func(gutenburg, limits=(start, end),
                                   xs=at_least, ys=data.amount_of_at_least)
    linear_values, _ = utilities.fit_func(linear_gutenburg, limits=(start, end),
                                          xs=at_least, ys=log_amount)
    gutenburg_x = np.linspace(at_least[start], at_least[end], 100)
    gutenburg_y = gutenburg(gutenburg_x, *values)
    gutenburg_y_linear = linear_gutenburg(gutenburg_x, *linear_values)
    label = 'a={:.1f} b={:.3f}'

    title = '{}x{}'.format(data.run_info.rows, data.run_info.cols)

    options = {'line_width': 2, 'plot_type': '-'}
    subplot_options = {'legend_size': 14}

    overlayed_law = Graph(gutenburg_x, gutenburg_y, legend_label=label.format(*values), **options)
    overlayed_law_linear = Graph(gutenburg_x, gutenburg_y_linear, legend_label=label.format(*linear_values), **options)

    all_events = Graph(data.event_magnitudes, list(range(len(data.event_magnitudes))), plot_size=3)
    magnitudes_at_least = Graph(data.magnitudes_of_at_least, data.amount_of_at_least, **options)
    log_magnitdes_at_least = Graph(data.magnitudes_of_at_least, log_amount, **options)

    draw(SubPlot(all_events, y_label='N (Sorted Event #)', x_label='M (Magnitude)',
                 **subplot_options), title=title)
    draw(SubPlot(magnitudes_at_least, overlayed_law,
                 x_label='M (Magnitude)', y_label='N (# of events where magnitude > M)',
                 **subplot_options), title=title)
    draw(SubPlot(log_magnitdes_at_least, overlayed_law_linear,
                 x_label='M (Magnitude)', y_label='log$_{10}$(N)',
                 **subplot_options), title=title)

