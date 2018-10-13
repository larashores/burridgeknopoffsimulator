from files.saveables import Data, Timeslice

def read_data(file_name):
    with open(file_name, 'rb') as file:
        data, index =  Data.from_byte_array(bytearray(file.read()))
        return data


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
