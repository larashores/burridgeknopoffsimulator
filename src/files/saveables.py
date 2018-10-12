from saveable.composite import Composite
from saveable.saveablearray import array
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16

class Timeslice(array(SaveableDouble)):
    pass

class Data(Composite):
    VERSION = 1

    rows = U16
    cols = U16
    spring_length = SaveableDouble
    mass = SaveableDouble
    spring_constant = SaveableDouble
    static_friction = SaveableDouble
    kinetic_friction = SaveableDouble
    plate_velocity = SaveableDouble
    plate_spring_constant = SaveableDouble
    total_time = SaveableDouble
    times = array(SaveableDouble)
    values_list = array(Timeslice)

    def __init__(self):
        Composite.__init__(self)
        self.version = U16(Data.VERSION)

    def to_byte_array(self):
        byte_array = self.version.to_byte_array()
        byte_array += Composite.to_byte_array(self)
        return byte_array

    def load_in_place(self, byte_array, index=0):
        index = self.version.load_in_place(byte_array, index)
        if self.version.get() != Data.VERSION:
            raise TypeError("Incorrect file version: '{}'".format(self.version.get()))
        Composite.load_in_place(self, byte_array, index)