from abc import abstractmethod, ABC
import numpy as np


class OdeSolver(ABC):
    """
    Will numerically a system of differential equations. This is a base class used by all solving methods

    Attributes:
        all_times: A list of time that the difeq was calculated at for each point
        all_values: A list of n-dimensional arrays that contain the values for each timestep
        difeqs: The system of differential equations to solve
        start_time: The original value of the independent variable to start at when solving this equation
        _original_step_size: The original step size to start calculating with
        _step_size: The current value of the step size
        _next_step_size: The step size to use at the next iteration
        _time: The current time (value of independent variable) of the last iteration

    Properties:a
        original_step_size: The original step_size to solve with
        step_size: The current value of the step size
        time: The current value of the time that was solved
        current_values: Read only property to get the current values. To set this use set_current_values
    """

    DEFAULT_STEP_SIZE = .002

    t = property(lambda self: self._time)

    def __init__(self, ode_system, *, start_time=0, initial_values=None, step_size=None):
        """
        Initializes a new Solver. Should be called by subclasses and not used directly.
        To solve a differential equation solve_until_time or solve_until_termination should be used. The
        initial conditions should be set with set_current_values(self, values)

        Args:
            odeSystem: The system of differential equations to solve
            start_time: The initial value of the independent variable to solve with
            initial_values: A sequence of initial values for the dependent variables
            step_size: The initial step size to solve with
        """
        self._difeqs = ode_system
        self._time = start_time
        self._current_values = initial_values
        self._step_size = step_size

    def set_initial_values(self, values):
        self._current_values = np.array(values)

    def succesful(self):
        return True

    def step(self):
        self._time += self._step_size
        self._current_values = self._step()
        return self._current_values

    def integrate(self, time):
        """
        Solves the difeq up until a certain point in time (independent var)

        Args:
            time: The time value to solve the difeq to
        """
        return self._integrate(lambda: self._time >= time)

    def _integrate(self, termination):
        """
        Solves the difeq until a specified termination condition is set

        Args:
            termination: A callable function whose boolean return values determines when to stop
        """
        self._start()
        while not termination():
             self.step()
        self._finish()
        return self._current_values

    def _start(self):
        """
        Called at the beginning of each simulation. If this returns True, self.current_values will be added to the
        values for the simulation
        """
        pass

    def _finish(self):
        """
        Called at the end of each simulation. If this returns True, self.current_values will be added to the
        values for the simulation
        """
        pass

    @abstractmethod
    def _step(self):
        """
        Abstract method that runs one single step of the simulation
        """
        pass