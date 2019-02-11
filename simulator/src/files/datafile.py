from pyserialization.union import Union
from files.data import Data
from files.scaledata import ScaledData
from files.partition import PartitionData


class DataFile(Union):
    data = Data
    scaled_data = ScaledData
    graph_partition = PartitionData

