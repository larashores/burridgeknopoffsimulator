from files.saveables import Data, Timeslice
import numpy as np

def read_data(file_name):
    with open(file_name, 'rb') as file:
        data, index =  Data.from_byte_array(bytearray(file.read()))
        values_list = []
        for values in data.values_list:
            array = np.zeros(len(values))
            for i, value in enumerate(values):
                array[i] = value.get()
            values_list.append(array)
        times = []
        for time in data.times:
            times.append(time.get())
        return data.rows.get(), data.cols.get(), times, values_list


def write_data(file_name, data, times, values_list):
    for time in times:
        data.times.append(time)
    for values in values_list:
        timeslice = Timeslice()
        for value in values:
            timeslice.append(value)
        data.values_list.append(timeslice)

    with open(file_name, 'wb') as file:
        file.write(data.to_byte_array())
