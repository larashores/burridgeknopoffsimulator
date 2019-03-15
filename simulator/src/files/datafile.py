from pyserialization.union import Union
from files.data import Data
from files.partition import PartitionData


class DataFile(Union):
    data = Data
    partition = PartitionData
