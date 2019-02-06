import sys
import os
sys.path.append(os.getcwd())

from files import util
from partition.graphpartition import partition

if __name__ == '__main__':
    file = util.get_file_name()
    print('Loading data file: ', file)
    data = util.read_data(file)
    print('Loaded')
    partition_data = partition(data)
    name, ext = os.path.splitext(file)
    new_name = name +'.pdat'
    util.write_data(new_name, partition_data)
    print('Wrote parition to file: {}'.format(new_name))
