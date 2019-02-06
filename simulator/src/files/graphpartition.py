from pyserialization.composite import Composite
from pyserialization.serialint import SerialU16, SerialU32
from pyserialization.seriallist import serial_list


class SingleSlipData(Composite):
    row = SerialU16
    col = SerialU16
    start_index = SerialU32
    end_index = SerialU32


class SlipData(serial_list(SingleSlipData)):
    pass


class GraphPartitionData(serial_list(SlipData)):
    pass
