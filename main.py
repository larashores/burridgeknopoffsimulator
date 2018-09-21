import random
import numpy as np
from scipy.integrate import odeint, ode

from viewers.tkviewer1d import view_1d
from friction import OneDimFrictionalForce
from springforce import OneDimSpringForce
from velocity import OneDimVelocity


spring_length = 1
mass = 1
gravitational_acceleration = g = 9.81
spring_constant = k = 1
static_friction = us = .03
kinetic_friction = uk = .025


class Differential:
    def __init__(self, num_blocks):
        self.one_dim_spring_force = OneDimSpringForce(num_blocks, k, spring_length)
        self.one_dim_friction_force = OneDimFrictionalForce(num_blocks, static_friction, kinetic_friction, mass)
        self.one_dim_velocity = OneDimVelocity(num_blocks)

    def __call__(self, t, values):
        """
        The first parameter values is a vector with all the values of the system of equations. Since we are splitting a
        system of 2nd order ODEs to 1st order ODEs, values[2n]=x(n) and values[2n+1] = x'(n)

        Function should return a list of values [
        """
        spring_force = self.one_dim_spring_force(values)
        friction_force = self.one_dim_friction_force(values)
        new_positions = self.one_dim_velocity(values)
        net = (1 / mass) * (spring_force + friction_force + new_positions)
        return net


def solve_1d():
    num_blocks = 5
    differential = Differential(num_blocks)
    initial_positions = np.zeros(num_blocks * 2)  # One initial position and initial velocity each
    for i in range(num_blocks):
        initial_positions[2*i] = i + (random.random() / 2)      # Initial positions 1 unit apart
        initial_positions[2*i + 1] = 0  # Initial velocities zero
    initial_positions[len(initial_positions) - 1] = .2   # Initial velocity of right block
    r = ode(differential)
    r.set_integrator('dopri5')
    r.set_initial_value(initial_positions)
    sol = []
    while r.successful() and r.t < 300:
        sol.append(r.integrate(r.t+.1))
    return np.array(sol)


def test(solution):
    n = solution.shape[1]
    last_positions = solution[:,n - 4]
    last_velocities = solution[:,n - 3]

    print('Last block positions:')
    print(last_positions)
    print('Last block velocities:')
    print(last_velocities)


if __name__ == '__main__':
    solution = solve_1d()
    # test(solution)
    view_1d(solution)
