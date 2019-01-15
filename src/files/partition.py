from pyserialization.composite import Composite
from pyserialization.serialndarray import SerialNdArray
from files.scaledata import ScaledRunInfo


class Partition(Composite):
    run_info = ScaledRunInfo
    event_magnitudes = SerialNdArray
    magnitudes_of_at_least = SerialNdArray
    amount_of_at_least = SerialNdArray
