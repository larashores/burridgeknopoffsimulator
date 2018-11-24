from src.odesolver.odesolver import OdeSolver
from src.odesolver.test import test


class Midpoint(OdeSolver):
    """
    Implements a solving algorithm using the Midpoint Method
    """
    def _step(self):
        first_derivative = self._difeqs(self._time, self._current_values)
        half_step_values = self._current_values + (first_derivative * (self._step_size / 2))
        half_step_derivative = self._difeqs(self._time + (self._step_size / 2), half_step_values)
        return self._current_values + (half_step_derivative * self._step_size)

if __name__ == '__main__':
    test(Midpoint)
