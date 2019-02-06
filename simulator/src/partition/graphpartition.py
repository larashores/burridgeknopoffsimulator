import numpy as np
from files.partition import Partition
from simulation.blockarray import BlockArray
import math


class SlipEvent:
    def __init__(self, coord):
        self._start_time, row, col = coord
        self._end_time = None
        self._blocks = [coord]

    def add_block(self, time, row, col):
        self._blocks.append((time, row, col))
        self._end_time = time

    def __str__(self):
        return f'Start:{self._start_time}, End: {self._end_time}, {sorted(self._blocks)}'


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
            slip_event = SlipEvent(coord)
            self._depth_first_search(slip_event, slipped_blocks, coord)
            components.append(slip_event)
        components.sort(key=lambda slip: slip._start_time)
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
