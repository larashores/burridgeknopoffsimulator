import random
import numpy as np
from scipy.integrate import odeint, ode

from viewers.potentialenergy import view_energy
from viewers.tkviewer1d import view_1d
from friction import OneDimFrictionalForce
from springforce import OneDimSpringForce
from velocity import OneDimVelocity
from drivingplate import OneDimDrivingPlate


spring_length = 1
mass = .5
gravitational_acceleration = g = 9.81
spring_constant = k = 1
static_friction = us = .1
kinetic_friction = uk = 10
plate_velocity = .05
plate_spring_constant = .5


def potential_energy(time, values):
    total_energy = 0
    for i in range(0, len(values)//2 - 1):
        length = values[2*i + 2] - values[2*i]
        energy = .5 * k * (length - spring_length)**2
        total_energy += energy
    for i in range(len(values)//2):
        energy = .5 * plate_spring_constant * (i * spring_length + plate_velocity * time -values[2*i])
        total_energy += energy
    return total_energy

class Differential:
    def __init__(self, num_blocks):
        self.one_dim_spring_force = OneDimSpringForce(num_blocks, k, spring_length, mass)
        self.one_dim_plate = OneDimDrivingPlate(num_blocks, plate_spring_constant, spring_length, plate_velocity, mass)
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
        plate_force = self.one_dim_plate(values, t)
        new_positions = self.one_dim_velocity(values)
        net = spring_force + new_positions + friction_force + plate_force
        np.set_printoptions(precision=4)
        return net

def initial_positions(num_blocks, initial_velocity):
    positions = np.zeros(num_blocks * 2)                               # One initial position and initial velocity each
    for i in range(num_blocks):
        positions[2*i] = spring_length * (i + random.random() / 2)  # Initial positions 1 unit apart
        positions[2*i + 1] = 0                                         # Initial velocities zero
    return positions

def solve_1d():
    num_blocks = 8
    r = ode(Differential(num_blocks))
    r.set_integrator('dopri5')
    r.set_initial_value(initial_positions(num_blocks, .2))
    sol = []
    energies = []
    times = []
    while r.successful() and r.t < 300:
        values = r.integrate(r.t+.1)
        times.append(r.t)
        sol.append(values)
        energies.append(potential_energy(r.t, values))
    return times, np.array(sol), np.array(energies)


if __name__ == '__main__':
    times, solution, energies = solve_1d()
    view_energy(times, energies)
    view_1d(solution)
