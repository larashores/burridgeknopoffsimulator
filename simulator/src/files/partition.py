from pyserialization.composite import Composite
from pyserialization.serialndarray import SerialNdArray
from pyserialization.serialint import SerialU16, SerialU32
from pyserialization.serialfloat import SerialDouble
from pyserialization.seriallist import serial_list
from files.scaledata import ScaledRunInfo


class SingleSlipData(Composite):
    row = SerialU16
    col = SerialU16
    start_index = SerialU32
    end_index = SerialU32
    distance = SerialDouble


class SlipData(serial_list(SingleSlipData)):
    pass


class PartitionData(Composite):
    slip_events = serial_list(SlipData)
    run_info = ScaledRunInfo


class Partition(Composite):
    run_info = ScaledRunInfo
    event_magnitudes = SerialNdArray
    magnitudes_of_at_least = SerialNdArray
    amount_of_at_least = SerialNdArray
