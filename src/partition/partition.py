import numpy as np
from src.simulation.blockarray import BlockArray
from graphing.graphing import *


class SingleSlipEvent:
    row = property(lambda self: self._row)
    col = property(lambda self: self._col)
    start_index = property(lambda self: self._start_index)
    end_index = property(lambda self: self._end_index)
    distance = property(lambda self: self._distance)

    def __init__(self, solution, num_cols, row, col, start_index):
        self._distance = 0
        self._solution = solution
        self._num_columns = num_cols
        self._row = row
        self._col = col
        self._start_index = start_index
        self._end_index = start_index

    def set_end(self, end_index):
        self._end_index = end_index
        start_block_array = BlockArray(self._solution[self._start_index], self._num_columns)
        end_block_array = BlockArray(self._solution[self._end_index], self._num_columns)
        self._distance = end_block_array.positions[self._row, self._col] -  \
                         start_block_array.positions[self._row, self._col]


class SlipEvent:
    start_time = property(lambda self: self._start_time)
    end_time = property(lambda self: self._end_time)
    start_index = property(lambda self: self._start_index)
    end_index = property(lambda self: self._end_index)
    slipped_blocks = property(lambda self: self._blocks_to_events.copy())

    def __init__(self, solution, rows, cols, time, start_index):
        self._blocks_to_events = {}
        self._solution = solution
        self._start_time = time
        self._end_time = time
        self._start_index = start_index
        self._end_index = start_index
        self._rows = rows
        self._cols = cols

    @property
    def distance(self):
        dist = 0
        for slip_list in self._blocks_to_events.values():
            for single_slip in slip_list:
                dist += single_slip.distance
        return dist

    def set_end(self, end_time, end_index):
        self._end_time = end_time
        self._end_index = end_index
        for row in range(self._rows):
            for col in range(self._cols):
                slipping = False
                for ind in range(self._start_index, self._end_index + 1):
                    block_array = BlockArray(self._solution[ind], self._cols)
                    if block_array.velocities[row, col] > 0:
                        if not slipping:
                            if (row, col) not in self._blocks_to_events:
                                self._blocks_to_events[(row, col)] = []
                            self._blocks_to_events[(row, col)].append(
                                SingleSlipEvent(self._solution, self._cols, row, col, ind))
                            slipping = True
                    elif slipping:
                        self._blocks_to_events[(row, col)][-1].set_end(ind)
                        slipping = False


def partition(data):
    solution = []
    for values in data.values_list:
        array = np.zeros(len(values))
        for i, value in enumerate(values):
            array[i] = value.get()
        solution.append(array)

    slip_events = []
    slipping = False
    for ind, time_slice in enumerate(solution):
        block_array = BlockArray(time_slice, data.cols.get())
        slip = False
        for ind_, value in enumerate(block_array.velocities):
            if value > 0:
                slip = True
                break
        if not slipping and slip:
            slip_events.append(SlipEvent(solution, data.rows.get(), data.cols.get(), data.times[ind].get(), ind))
        elif slipping and not slip:
            slip_events[-1].set_end(data.times[ind].get(), ind)
        slipping = slip

    return slip_events

def view_partition(data):
    slip_events = partition(data)
    magnitudes = []
    for event in slip_events:
        print('Event at: (', round(event.start_time, 1),
              ',', round(event.end_time, 1),
              ') from', event.start_index,
              'to', event.end_index,
              ', num slipped:', len(event.slipped_blocks),
              ', distance:', event.distance)
        magnitudes.append(np.log(event.distance))
    print(magnitudes)
    at_least = np.linspace(-1, 3, 100)
    amount = []
    for magnitude in at_least:
        amount.append(sum((lambda x: x > magnitude)(x) for x in magnitudes))

    magnitudes.sort()
    graph = Graph(list(range(len(magnitudes))), magnitudes)
    graph2 = Graph(at_least, amount, plot_type='-')
    draw(SubPlot(graph))
    draw(SubPlot(graph2))