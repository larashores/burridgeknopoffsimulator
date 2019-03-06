from files.datafile import DataFile

import glob
import os
import sys


def read_data(file_name):
    with open(file_name, 'rb') as file:
        data, index = DataFile.from_bytes(bytearray(file.read()))
        return data.get()


def write_data(file_name, data):
    data_file = DataFile()
    data_file.set(type(data), data)
    with open(file_name, 'wb') as file:
        file.write(data_file.to_bytes())


def get_single_file_name(*extensions):
    if len(sys.argv) == 1:
        files = []
        for ext in extensions:
            files.extend(glob.iglob('data/*.'+ext))
        return max(files, key=os.path.getctime)
    elif len(sys.argv) == 2:
        return os.path.join('data', sys.argv[1])
    else:
        raise TypeError('Usage: [filename]')


def get_all_file_names(*extensions):
    if len(sys.argv) == 1:
        files = []
        for ext in extensions:
            files.extend(glob.iglob('data/*.' + ext))
        return files


def data_desc(data):
    info = data.run_info
    return (f'rows: {info.rows}\n' +
            f'cols: {info.cols}\n' +
            f'L:    {info.spring_length}\n' +
            f'v:    {info.plate_velocity}\n' +
            f'a:    {info.alpha}\n' +
            f'l:    {info.l}\n' +
            f'dt:   {info.time_interval}')
