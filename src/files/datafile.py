from saveable.composite import Composite
from saveable.saveableenum import saveable_enum
from saveable.union import Union
from files.data import Data
from files.scaledata import ScaledData
import enum


class DataTypes(enum.Enum):
    data = Data
    scaled_data = ScaledData


class DataFile(Union):
    data = Data
    scaled_data = ScaledData
