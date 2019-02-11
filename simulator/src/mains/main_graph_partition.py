from files import util
from partition.graphpartition import graph_partition
import os


if __name__ == '__main__':
    file = util.get_file_name()
    print('Loading data file: ', file)
    data = util.read_data(file)
    print('Loaded')
    partition_data = graph_partition(data)
    name, ext = os.path.splitext(file)
    new_name = name + '.gpdat'
    util.write_data(new_name, partition_data)
    print('Wrote partition to file: {}'.format(new_name))
