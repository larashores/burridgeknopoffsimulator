import glob
import os
import sys

from files.data import Data

def read_data(file_name):
    with open(file_name, 'rb') as file:
        data, index =  Data.from_byte_array(bytearray(file.read()))
        return data

def write_data(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data.to_byte_array())

def get_file_name():
    if len(sys.argv) == 1:
        files = glob.iglob('data/*')
        return max(files, key=os.path.getctime)
    elif len(sys.argv) == 2:
        return os.path.join('data', sys.argv[1])
    else:
        raise TypeError('Usage: [filename]')

def data_desc(data):
        return ('rows: {}\n' +
               'cols: {}\n' +
               'm:    {}\n' +
               'v:    {}\n' +
               'l:    {}\n' +
               'k_b:  {}\n' +
               'k_p:  {}\n' +
               'u_s:  {}\n' +
               'u_k:  {}\n' +
               'dt:   {}').format(data.rows, data.cols, data.mass,
                               data.plate_velocity,
                               data.spring_length,
                               data.spring_constant, data.plate_spring_constant,
                               data.static_friction, data.kinetic_friction,
                               data.time_interval)
def scaled_data_desc(data):
        return ('rows: {}\n' +
                'cols: {}\n' +
                'L:    {}\n' +
                'v:    {}\n' +
                'a:    {}\n' +
                'l:    {}\n' +
                'dt:   {}').format(data.rows, data.cols,
                                   data.spring_length,
                                   data.plate_velocity,
                                   data.alpha,
                                   data.l,
                                   data.time_interval)