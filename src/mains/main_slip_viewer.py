from files import util
from viewers.slipviewer import view_slip

if __name__ == '__main__':
    file = util.get_file_name()
    data = util.read_data(file)
    view_slip(data, util.data_desc(data))
