import numpy as np
from files.partition import Partition
from simulation.blockarray import BlockArray
import math


class SingleSlipEvent:
    start_index = property(lambda self: self._start_index)
    end_index = property(lambda self: self._end_index)

    def __init__(self, current_index):
        self._start_index = current_index
        self._end_index = current_index

    def slip_event(self, index):
        self._start_index = min(self._start_index, index)
        self._end_index = max(self._end_index, index)


class SlipEvent:
    def __init__(self, data, coord):
        self._data = data
        self._slip_events = {}
        self._start_index = coord[0]
        self._end_index = coord[0]
        self.add_block(*coord)

    def add_block(self, index, row, col):
        coords = (row, col)
        if coords not in self._slip_events:
            self._slip_events[coords] = SingleSlipEvent(index)
            return
        self._slip_events[coords].slip_event(index)
        self._start_index = min(self._start_index, index)
        self._end_index = max(self._end_index, index)

    @property
    def distance(self):
        columns = self._data.run_info.cols
        values = self._data.values_list
        dist = 0
        for (row, col), event in self._slip_events.items():
            start_block_array = BlockArray(values[event.start_index].get(), columns)
            end_block_array = BlockArray(values[event.end_index].get(), columns)
            dist += end_block_array.positions[row, col] - start_block_array.positions[row, col]
        return dist

    def __str__(self):
        return f'Start:{self._start_index}, End: {self._end_index}, distance: {self.distance} '  \
               f'{sorted(list(self._slip_events.keys()))}'


class GraphParitioner:
    def __init__(self, data):
        self._data = data
        self._connected_components = None

    def partition(self):
        if self._connected_components is None:
            self._connected_components = self._calculate_connected()
        return self._connected_components

    def _calculate_connected(self):
        components = []
        slipped_blocks = self._slipped_blocks()
        while len(slipped_blocks) > 0:
            coord = slipped_blocks.pop()
            slip_event = SlipEvent(self._data, coord)
            self._depth_first_search(slip_event, slipped_blocks, coord)
            components.append(slip_event)
        return components

    def _slipped_blocks(self):
        slipped = []
        rows = self._data.run_info.rows
        cols = self._data.run_info.cols
        for ind, timeslice in enumerate(self._data.values_list):
            block_array = BlockArray(timeslice.get(), cols)
            for row in range(rows):
                for col in range(cols):
                    if block_array.velocities[row, col] > 0:
                        slipped.append((ind, row, col))
        slipped.reverse()
        return slipped

    def _depth_first_search(self, slip_event, slipped_blocks, coord):
        for neighbor in self._neighbors(*coord):
            if neighbor in slipped_blocks:
                slip_event.add_block(*neighbor)
                slipped_blocks.remove(neighbor)
                self._depth_first_search(slip_event, slipped_blocks, neighbor)

    @staticmethod
    def _neighbors(time, row, col):
        yield time, row, col + 1
        yield time, row, col - 1
        yield time, row + 1, col
        yield time, row - 1, col
        yield time + 1, row, col
        yield time - 1, row, col


def partition(data):
    print('Searching for events')
    partitioner = GraphParitioner(data)
    partitions = partitioner.partition()

    for partition in partitions:
        print(partition)

    # file = Partition()
    # file.run_info = data.run_info
    # file.event_magnitudes = np.array(sorted(magnitudes))
    # file.magnitudes_of_at_least = np.linspace(-15, 5, 100)
    # file.amount_of_at_least = np.zeros(len(file.magnitudes_of_at_least))
    # for ind, magnitude in enumerate(file.magnitudes_of_at_least):
    #     file.amount_of_at_least[ind] = sum((lambda x: x > magnitude)(x) for x in magnitudes)
    # return file
