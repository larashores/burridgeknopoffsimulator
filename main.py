import numpy as np
from scipy.integrate import odeint

mass = 1
gravitational_acceleration = g = 9.81
spring_constant = k = 1
static_friction = us = .1
kinetic_friction = uk = .1


def get_net_force(spring_force):
    cutoff = us * mass * g
    if spring_force >= cutoff:
        return (1 / mass) * (spring_force - uk * mass * g)
    elif spring_force <= cutoff:
        return (1 / mass) * (spring_force + uk * mass * g)
    else:
        return 0


def differential(values, t):
    """
    The first parameter values is a vector with all the values of the system of equations. Since we are splitting a
    system of 2nd order ODEs to 1st order ODEs, values[2n]=x(n) and values[2n+1] = x'(n)

    Function should return a list of values [
    """
    results = np.zeros(len(values))

    for i in range(1, (len(values) // 2) - 1):
        pos_minus = values[2*i - 2]
        pos = values[2*i]
        pos_plus = values[2*i + 2]
        spring_force = k * (pos_plus + pos_minus - 2*pos)
        results[2*i] = values[2*i + 1]                      # x'
        results[2*i + 2] = get_net_force(spring_force)      # x''

    # Left Boundary Condition
    results[0] = values[1]
    results[1] = get_net_force(k * (values[2] - values[0]))

    # Right Boundary Condition
    results[len(values) - 2] = values[len(values) - 1]
    results[len(values) - 1] = 0

    return results


def solve_1d():
    num_blocks = 8
    initial_positions = np.zeros(num_blocks * 2)  # One initial position and initial velocity each
    for i in range(num_blocks):
        initial_positions[2*i] = i      # Initial positions 1 unit apart
        initial_positions[2*i + 1] = 0  # Initial velocities zero
    initial_positions[len(initial_positions) - 1] = .1   # Initial velocity of right block
    ts = np.linspace(0, 10, 101)
    return odeint(differential, initial_positions, ts)


def test(solution):
    n = solution.shape[1]
    last_positions = solution[:,n - 2]
    last_velocities = solution[:,n - 1]

    print('Last block positions:')
    print(last_positions)
    print('Last block velocities:')
    print(last_velocities)


if __name__ == '__main__':
    solution = solve_1d()
    test(solution)
