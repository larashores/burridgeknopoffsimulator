from pyserialization.composite import Composite
from pyserialization.serialint import SerialU16, SerialU32
from pyserialization.serialfloat import SerialDouble
from pyserialization.seriallist import serial_list
from files.runinfo import RunInfo


class SingleSlipData(Composite):
    row = SerialU16
    col = SerialU16
    start_index = SerialU32
    end_index = SerialU32
    distance = SerialDouble


class SlipData(serial_list(SingleSlipData)):
    pass


class FitLimit(Composite):
    fit_start = SerialDouble
    fit_end = SerialDouble

    def __str__(self):
        return f'Start: {self.fit_start} | End: {self.fit_end}'


class FitList(serial_list(FitLimit)):
    pass


class PartitionData(Composite):
    slip_events = serial_list(SlipData)
    run_info = RunInfo
    fit_list = FitList
