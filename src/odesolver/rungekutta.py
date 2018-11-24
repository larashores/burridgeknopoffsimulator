from src.odesolver.odesolver import OdeSolver
from src.odesolver.test import test
from abc import ABC, abstractmethod
import numpy as np


class RungeKuttaMethod(OdeSolver, ABC):
    """
    Base class used to create a solver for any RungeKuttaMethod. The subclass must define two sequences, STEP_WEIGHTS,
    where the step size at each iteration is weighted (0 would put the step at the current time) and WEIGHT_COEFFICIENTS
    where the successive estimates are weighted by that amount in the average.
    """
    STEP_WEIGHTS = property(classmethod(abstractmethod(lambda cls: NotImplementedError)))
    WEIGHT_COEFFICIENTS = property(classmethod(abstractmethod(lambda cls: NotImplementedError)))

    def __init__(self, *args, **kwargs):
        """
        Initializes a new Runge-Kutta method. Sets up all the arrays that are used in the calculation
        """
        OdeSolver.__init__(self, *args, **kwargs)
        self._weight_array = np.array([0] + list(self.WEIGHT_COEFFICIENTS))
        self._step_array = np.array(self.STEP_WEIGHTS) * self._step_size

    def _step(self):
        results = [0]
        for i in range(len(self.WEIGHT_COEFFICIENTS)):
            results.append(self._difeqs(self._time + self._step_array[i],
                                        self._current_values + results[i]*self._step_array[i]))

        average_derivative = np.average(results, weights=self._weight_array, axis=0)
        return self._current_values + (average_derivative * self._step_size)


class RungeKutta4(RungeKuttaMethod):
    """
    Implements a solving algorithm using the Runge-Kutta 4th Order method
    """
    STEP_WEIGHTS = [0, .5, .5, 1]
    WEIGHT_COEFFICIENTS = [1, 2, 2, 1]
    DEFAULT_STEP_SIZE = .01


if __name__ == '__main__':
    test(RungeKutta4)
