from pyserialization.union import Union
from files.data import Data
from files.scaledata import ScaledData
from files.partition import Partition


class DataFile(Union):
    data = Data
    scaled_data = ScaledData
    partition = Partition

