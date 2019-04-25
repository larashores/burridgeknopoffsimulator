from files import util
from viewers.partitionviewer import view_partition


if __name__ == '__main__':
    file = util.get_single_file_name('gpdat')
    data = util.read_data(file)
    view_partition(data, file)
