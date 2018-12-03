from src.saveable.composite import Composite
from src.saveable.saveablendarray import ndarray
from files.scaledata import ScaledRunInfo


class Partition(Composite):
    run_info = ScaledRunInfo
    event_magnitudes = ndarray()
    magnitudes_of_at_least = ndarray()
    amount_of_at_least = ndarray()