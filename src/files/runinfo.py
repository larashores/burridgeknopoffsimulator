from saveable.composite import Composite
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16


class RunInfo(Composite):
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