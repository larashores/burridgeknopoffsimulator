from pyserialization.composite import Composite
from pyserialization.serialfloat import SerialDouble
from pyserialization.serialint import SerialU16


class RunInfo(Composite):
    rows = SerialU16
    cols = SerialU16
    spring_length = SerialDouble
    mass = SerialDouble
    spring_constant = SerialDouble
    static_friction = SerialDouble
    kinetic_friction = SerialDouble
    plate_velocity = SerialDouble
    plate_spring_constant = SerialDouble
    time_interval = SerialDouble
    total_time = SerialDouble
