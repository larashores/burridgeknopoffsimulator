from files import util
from partition.partition import view_partition

if __name__ == '__main__':
    file = util.get_file_name()
    data = util.read_data(file)
    view_partition(data)
