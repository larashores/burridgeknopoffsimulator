from src.odesolver.odesolver import OdeSolver
from src.odesolver.test import test
import burridgeknopoff as bk


class Euler(OdeSolver):
    """
    Implements a solving algorithm using the standard Euler Method
    """
    def _step(self):
        derivatives = self._difeqs(self._time, self._current_values)
        self._current_values += derivatives * self._step_size


if __name__ == '__main__':
    test(bk.Euler)
