import random
from datetime import datetime

from scipy.integrate import ode

from files.readwrite import write_data
from simulation.blockarray import BlockArray
from simulation.differential import Differential


def solve(num_rows, num_cols, spring_length, mass, spring_constant, static_friction, kinetic_friction, plate_velocity,
          plate_spring_constant):
    blocks = BlockArray(num_rows, num_cols)
    for i in range(num_rows):
        for j in range(num_cols):
            blocks.positions[i, j] = spring_constant * (j + random.random() / 2)
    r = ode(Differential(num_rows, num_cols,
                         block_spring_constant=k, plate_spring_constant=plate_spring_constant,
                         static_friction=static_friction, kinetic_friction=kinetic_friction,
                         mass=mass, spring_length=spring_length, plate_velocity=plate_velocity))
    r.set_integrator('dopri5')
    r.set_initial_value(blocks.array)
    times = []
    sol = []
    progress_at = 0
    while r.successful() and r.t < 300:
        values = r.integrate(r.t+.1)
        times.append(r.t)
        sol.append(values)
        if r.t > progress_at:
            print('Time: {}'.format(progress_at))
            progress_at += 1
    return times, sol


if __name__ == '__main__':
    rows = 3
    cols = 3
    spring_length = l = 1
    mass = m =.5
    spring_constant = k = 1
    static_friction = us = .1
    kinetic_friction = uk = 10
    plate_velocity = v = .05
    plate_spring_constant = kp = .5
    file_name = 'data/{}x{}-{}.dat'.format(rows, cols, datetime.now().strftime('%Y%m%dT%H%M%SZ'))

    times, solution = solve(rows, cols, spring_length, mass, spring_constant, static_friction,
                            kinetic_friction, plate_velocity, plate_spring_constant)
    write_data(file_name, rows, cols, spring_length, mass, spring_constant, static_friction,
               kinetic_friction, plate_velocity, plate_spring_constant, times, solution)
    print('File saved to: {}'.format(file_name))
