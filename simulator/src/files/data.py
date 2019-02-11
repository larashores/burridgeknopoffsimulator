from pyserialization.composite import Composite
from pyserialization.seriallist import serial_list
from pyserialization.serialfloat import SerialDouble
from pyserialization.serialint import SerialU16
from files.timeslice import Timeslice
from files.runinfo import RunInfo


class Data(Composite):
    VERSION = 1

    run_info = RunInfo
    times = serial_list(SerialDouble)
    values_list = serial_list(Timeslice)

    def __init__(self):
        Composite.__init__(self)
        self._version = SerialU16(Data.VERSION)

    def add_slice(self, time, values):
        self.times.append(time)
        self.values_list.append(Timeslice(values))

    def to_bytes(self):
        return self._version.to_bytes() + Composite.to_bytes(self)

    def load_in_place(self, data, index=0):
        index = self._version.load_in_place(data, index)
        if self._version.get() != Data.VERSION:
            raise TypeError("Incorrect file version: '{}'".format(self._version.get()))
        Composite.load_in_place(self, data, index)
        return index
