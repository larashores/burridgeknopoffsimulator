from files import util
from viewers.blockviewer import view_2d

if __name__ == '__main__':
    file = util.get_file_name('dat')
    data = util.read_data(file)
    view_2d(data, util.data_desc(data))
