from src.odesolver.odesolver import OdeSolver
from src.odesolver.test import test


class Heuns(OdeSolver):
    """
    Implements a solving algorithm using Heuns Method / Improved Euler Method
    """
    def _step(self):
        first_derivative = self._difeqs(self._time, self._current_values)
        second_step_values = self._current_values + (first_derivative * self._step_size)
        second_derivative = self._difeqs(self._time + self._step_size, second_step_values)
        mid_derivative = (first_derivative + second_derivative) / 2
        self._current_values += mid_derivative * self._step_size

if __name__ == '__main__':
    test(Heuns)
