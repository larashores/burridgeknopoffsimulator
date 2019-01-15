from pyserialization.composite import Composite
from pyserialization.serialfloat import SerialDouble
from pyserialization.serialint import SerialU16


class ScaledRunInfo(Composite):
    rows = SerialU16
    cols = SerialU16
    spring_length = SerialDouble
    plate_velocity = SerialDouble
    alpha = SerialDouble
    l = SerialDouble
    time_interval = SerialDouble
    total_time = SerialDouble
