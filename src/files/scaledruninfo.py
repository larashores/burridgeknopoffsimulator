from saveable.composite import Composite
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16


class ScaledRunInfo(Composite):
    rows = U16
    cols = U16
    spring_length = SaveableDouble
    plate_velocity = SaveableDouble
    alpha = SaveableDouble
    l = SaveableDouble
    time_interval = SaveableDouble
    total_time = SaveableDouble