from files.partition import PartitionData, SlipData, SingleSlipData
from simulation.blockarray import BlockArray


class SingleSlipEvent:
    row = property(lambda self: self._row)
    col = property(lambda self: self._col)
    start_index = property(lambda self: self._start_index)
    end_index = property(lambda self: self._end_index)
    distance = property(lambda self: self._distance)

    def __init__(self, data, row, col, start_index):
        self._distance = 0
        self._data = data
        self._data = data
        self._row = row
        self._col = col
        self._start_index = start_index
        self._end_index = start_index

    def set_end(self, end_index):
        self._end_index = end_index
        start_block_array = BlockArray(self._data.values_list[self._start_index].get(), self._data.run_info.cols)
        end_block_array = BlockArray(self._data.values_list[self._end_index].get(), self._data.run_info.cols)
        self._distance = end_block_array.positions[self._row, self._col] -  \
                         start_block_array.positions[self._row, self._col]


class SlipEvent:
    start_time = property(lambda self: self._data.times[self._start_index].get())
    end_time = property(lambda self: self._data.times[self._end_index].get())
    start_index = property(lambda self: self._start_index)
    end_index = property(lambda self: self._end_index)
    slipped_blocks = property(lambda self: self._blocks_to_events.copy())

    def __init__(self, data, start_index):
        self._blocks_to_events = {}
        self._data = data
        self._start_index = start_index
        self._end_index = start_index

    def single_slip_events(self):
        return self._blocks_to_events.items()

    @property
    def distance(self):
        dist = 0
        for slip_list in self._blocks_to_events.values():
            for single_slip in slip_list:
                dist += single_slip.distance
        return dist

    def set_end(self, end_index):
        self._end_index = end_index
        for row in range(self._data.run_info.rows):
            for col in range(self._data.run_info.cols):
                slipping = False
                for ind in range(self._start_index, self._end_index + 1):
                    block_array = BlockArray(self._data.values_list[ind].get(),
                                             self._data.run_info.cols)
                    if block_array.velocities[row, col] > 0:
                        if not slipping:
                            if (row, col) not in self._blocks_to_events:
                                self._blocks_to_events[(row, col)] = []
                            self._blocks_to_events[(row, col)].append(
                                SingleSlipEvent(self._data, row, col, ind))
                            slipping = True
                    elif slipping:
                        self._blocks_to_events[(row, col)][-1].set_end(ind)
                        slipping = False


def create_events(data):
    slip_events = []
    slipping = False
    for ind, time_slice in enumerate(data.values_list):
        block_array = BlockArray(time_slice.get(), data.run_info.cols)
        slip = False
        for ind_, value in enumerate(block_array.velocities):
            if value > 0:
                slip = True
                break
        if not slipping and slip:
            event = SlipEvent(data, ind)
            slip_events.append(event)
            print('Event start at: {} ({}s)'.format(ind, event.start_time))
        elif slipping and not slip:
            event = slip_events[-1]
            event.set_end(ind)
            print('Event end at: (', round(event.start_time, 1),
                  ',', round(event.end_time, 1),
                  ') from', event.start_index,
                  'to', event.end_index,
                  ', num slipped:', len(event.slipped_blocks),
                  ', distance:', event.distance)
        slipping = slip

    return slip_events


def partition(data):
    print('Partitioning graph data')
    slip_events = create_events(data)

    print('Data partitioned. Saving Data')
    partition_data = PartitionData()
    partition_data.run_info = data.run_info
    for slip_event in slip_events:
        slip_data = SlipData()
        for coords, single_slip_event in slip_event.single_slip_events():
            single_slip_data = SingleSlipData()
            single_slip_data.start_index = slip_event.start_index
            single_slip_data.end_index = slip_event.end_index
            single_slip_data.row, single_slip_data.col = coords
            single_slip_data.distance = slip_event.distance
            slip_data.append(single_slip_data)
        partition_data.slip_events.append(slip_data)
    return partition_data
