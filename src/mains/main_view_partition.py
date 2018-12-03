from files import util
from src.graphing.graphing import *


if __name__ == '__main__':
    file = util.get_file_name('pdat')
    data = util.read_data(file)

    title = '{}x{}'.format(data.run_info.rows, data.run_info.cols)
    graph = Graph(list(range(len(data.event_magnitudes))), data.event_magnitudes, plot_type='-')
    graph2 = Graph(data.magnitudes_of_at_least, data.amount_of_at_least, plot_type='-')
    draw(SubPlot(graph, x_label='Event # (Sorted)', y_label='Magnitude'), title=title)
    draw(SubPlot(graph2, x_label='Magnitude', y_label='# of Events'), title=title)

