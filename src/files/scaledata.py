from saveable.composite import Composite
from saveable.saveablearray import array
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16, U32
from files.timeslice import Timeslice
from files.scaledruninfo import ScaledRunInfo


class ScaledData(Composite):
    VERSION = 1

    run_info = ScaledRunInfo
    times = array(SaveableDouble, U32)
    values_list = array(Timeslice, U32)

    def __init__(self):
        Composite.__init__(self)
        self._version = U16(ScaledData.VERSION)

    def add_slice(self, time, values):
        self.times.append(time)
        self.values_list.append(Timeslice(values))

    def to_byte_array(self):
        byte_array = self._version.to_byte_array()
        byte_array += Composite.to_byte_array(self)
        return byte_array

    def load_in_place(self, byte_array, index=0):
        index = self._version.load_in_place(byte_array, index)
        if self._version.get() != ScaledData.VERSION:
            raise TypeError("Incorrect file version: '{}'".format(self._version.get()))
        Composite.load_in_place(self, byte_array, index)
        return index
