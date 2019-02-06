from pyserialization.union import Union
from files.data import Data
from files.scaledata import ScaledData
from files.partition import Partition
from files.graphpartition import GraphPartitionData


class DataFile(Union):
    data = Data
    scaled_data = ScaledData
    partition = Partition
    graph_partition = GraphPartitionData

