from src.odesolver.odesolver import OdeSolver
from src.odesolver.test import test


class Euler(OdeSolver):
    """
    Implements a solving algorithm using the standard Euler Method
    """
    def _step(self):
        derivatives = self._difeqs(self._time, self._current_values)
        return self._current_values + (derivatives * self._step_size)


if __name__ == '__main__':
    test(Euler)
