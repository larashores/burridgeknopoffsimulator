import numpy as np
from files.partition import Partition
from simulation.blockarray import BlockArray
import math


def neighbors(row, col):
    yield row, col + 1
    yield row, col - 1
    yield row + 1, col
    yield row - 1, col


def get_slipped_blocks(block_array):
    slipped = set()
    for row in range(block_array.rows):
        for col in range(block_array.columns):
            if block_array.velocities[row, col] > 0:
                slipped.add((row, col))
    return slipped


def depth_first_search(num_rows, num_cols, slipped_blocks, coord):
    print('searching coord', coord)
    for neighbor in neighbors(*coord):
        print('got neighbor', neighbor, neighbor in slipped_blocks)
        if neighbor in slipped_blocks:
            yield neighbor
            depth_first_search(num_rows, num_cols, slipped_blocks, coord)


def connected_components(block_array):
    components = []
    slipped_blocks = get_slipped_blocks(block_array)
    print('slipped', sorted(list(slipped_blocks)))
    while len(slipped_blocks) > 0:
        coord = slipped_blocks.pop()
        slice = set()
        slice.add(coord)
        for block in depth_first_search(block_array.rows, block_array.columns, slipped_blocks, coord):
            slice.add(block)
            slipped_blocks.remove(block)
        components.append(slice)
    return components


def create_events(data):
    print('values', [vel for vel in data.values_list[0].get()])
    for ind, time_slice in enumerate(data.values_list):
        print('loop')
        block_array = BlockArray(time_slice.get(), data.run_info.cols)
        connected = connected_components(block_array)
        if len(connected) != 0:
            return connected


def partition(data):
    print('Searching for events')
    slip_events = create_events(data)
    for connected in slip_events:
        print(connected)

    # file = Partition()
    # file.run_info = data.run_info
    # file.event_magnitudes = np.array(sorted(magnitudes))
    # file.magnitudes_of_at_least = np.linspace(-15, 5, 100)
    # file.amount_of_at_least = np.zeros(len(file.magnitudes_of_at_least))
    # for ind, magnitude in enumerate(file.magnitudes_of_at_least):
    #     file.amount_of_at_least[ind] = sum((lambda x: x > magnitude)(x) for x in magnitudes)
    # return file
