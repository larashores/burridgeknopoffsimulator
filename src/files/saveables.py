from saveable.composite import Composite
from saveable.saveablearray import array
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16
from saveable.saveablendarray import ndarray


class Timeslice(ndarray()):
    pass


class Data(Composite):
    VERSION = 3

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
    values_list = array(Timeslice)

    def __init__(self):
        Composite.__init__(self)
        self._version = U16(Data.VERSION)

    def add_slice(self, time, values):
        self.times.append(time)
        self.values_list.append(Timeslice(values))

    def to_byte_array(self):
        byte_array = self._version.to_byte_array()
        byte_array += Composite.to_byte_array(self)
        return byte_array

    def load_in_place(self, byte_array, index=0):
        index = self._version.load_in_place(byte_array, index)
        if self._version.get() != Data.VERSION:
            raise TypeError("Incorrect file version: '{}'".format(self._version.get()))
        Composite.load_in_place(self, byte_array, index)