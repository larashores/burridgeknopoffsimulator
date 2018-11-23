from saveable.composite import Composite
from saveable.saveablearray import array
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16
from saveable.saveablearray import array

from files.saveables import Data, Timeslice
import numpy as np

class TimesliceOld(array(SaveableDouble)):
    pass


class DataOld(Composite):
    VERSION = 2

    rows = U16
    cols = U16
    spring_length = SaveableDouble
    mass = SaveableDouble
    spring_constant = SaveableDouble
    static_friction = SaveableDouble
    kinetic_friction = SaveableDouble
    plate_velocity = SaveableDouble
    plate_spring_constant = SaveableDouble
    time_interval = SaveableDouble
    total_time = SaveableDouble
    times = array(SaveableDouble)
    values_list = array(TimesliceOld)

    def __init__(self):
        Composite.__init__(self)
        self._version = U16(DataOld.VERSION)

    def add_slice(self, time, values):
        self.times.append(time)
        self.values_list.append(Timeslice(values))

    def to_byte_array(self):
        byte_array = self._version.to_byte_array()
        byte_array += Composite.to_byte_array(self)
        return byte_array

    def load_in_place(self, byte_array, index=0):
        index = self._version.load_in_place(byte_array, index)
        if self._version.get() != DataOld.VERSION:
            raise TypeError("Incorrect file version: '{}'".format(self._version.get()))
        Composite.load_in_place(self, byte_array, index)


def convert_2_to_3(old):
    new = Data()
    new.rows = old.rows.get()
    new.cols = old.cols.get()
    new.spring_length = old.spring_length.get()
    new.mass = old.mass.get()
    new.spring_constant = old.spring_constant.get()
    new.static_friction = old.static_friction.get()
    new.kinetic_friction = old.kinetic_friction.get()
    new.plate_velocity = old.plate_velocity.get()
    new.plate_spring_constant = old.plate_spring_constant.get()
    new.time_interval = old.time_interval.get()
    new.total_time = old.total_time.get()
    for time in old.times:
        new.times.append(time.get())
    for time_slice in old.values_list:
        new.values_list.append(Timeslice(np.array([value.get() for value in time_slice])))
    return new


if __name__ == '__main__':
    directory = r'E:\Users\Vincent\Documents\Capstone\Capstone 1\simulator\data'
    import os
    for file_name in os.listdir(directory):
        print('Trying:', file_name)
        try:
            with open(os.path.join(directory, file_name), 'rb') as file:
                try:
                    old, index = DataOld.from_byte_array(file.read())
                    new = convert_2_to_3(old)
                    new_name = file_name[:-5] + '3.dat'
                    with open(os.path.join(directory, new_name), 'wb') as file2:
                        file2.write(new.to_byte_array())
                    print('new name', new_name)
                except TypeError:
                    print('Wrong version')
                    continue
            os.remove(os.path.join(directory, file_name))
        except OSError:
            print('Error opening file')