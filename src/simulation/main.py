import random
from datetime import datetime

from scipy.integrate import ode

from files.saveables import Data
from files.readwrite import write_data
from simulation.blockarray import BlockArray
from simulation.differential import Differential


def solve(data):
    print('Creating initial data')
    blocks = BlockArray(data.rows.get(), data.cols.get())
    for i in range(data.rows.get()):
        for j in range(data.cols.get()):
            blocks.positions[i, j] = data.spring_constant.get() * (j + random.random() / 2)
    print('Initial data created')
    r = ode(Differential(data.rows.get(), data.cols.get(),
                         block_spring_constant=data.spring_constant.get(),
                         plate_spring_constant=data.plate_spring_constant.get(),
                         static_friction=data.static_friction.get(), kinetic_friction=data.kinetic_friction.get(),
                         mass=data.mass.get(), spring_length=data.spring_length.get(),
                         plate_velocity=data.plate_velocity.get()))
    r.set_integrator('dopri5')
    r.set_initial_value(blocks.array)
    times = []
    sol = []
    progress_at = 0
    start = datetime.now().timestamp()
    while r.successful() and r.t < 300:
        values = r.integrate(r.t+.1)
        times.append(r.t)
        sol.append(values)
        if r.t > progress_at:
            current = datetime.now().timestamp() - start
            print('Time-step: {}, Real-time: {:.2f}s'.format(progress_at, current))
            progress_at += 1
    current = datetime.now().timestamp() - start
    print('Finished at: {:.2f}s'.format(current))

    return times, sol, current


if __name__ == '__main__':
    data = Data()
    data.rows = 25
    data.cols = 25
    data.spring_length = 1.0
    data.mass = 2.0
    data.spring_constant = 1.0
    data.static_friction = 0.1
    data.kinetic_friction = 6.0
    data.plate_velocity = 0.05
    data.plate_spring_constant = 3
    file_name = 'data/{}x{}-{}.dat'.format(data.rows.get(), data.cols.get(), datetime.now().strftime('%Y%m%dT%H%M%SZ'))

    times, solution, elapsed = solve(data)
    data.total_time = elapsed
    write_data(file_name, data, times, solution)
    print('File saved to: {}'.format(file_name))
