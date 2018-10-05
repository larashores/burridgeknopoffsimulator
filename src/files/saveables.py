from saveable.composite import Composite
from saveable.saveablearray import array
from saveable.saveablefloat import SaveableDouble
from saveable.saveableint import U16

class Timeslice(array(SaveableDouble)):
    pass

class Data(Composite):
    times = array(SaveableDouble)
    values_list = array(Timeslice)
    rows = U16
    cols = U16
