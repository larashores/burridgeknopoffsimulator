import random
from datetime import datetime

from scipy.integrate import ode

from files.data import Data
from files.util import write_data
from simulation.blockarray import BlockArray
from simulation.differential import Differential
from physicalconstants import g

import winsound

def solve(data):
    print('Creating initial data')
    blocks = BlockArray(data.rows, data.cols)
    for i in range(data.rows):
        for j in range(data.cols):
            blocks.positions[i, j] = data.spring_length * (j + random.random() / 3)
    print('Initial data created')
    r = ode(Differential(data.rows, data.cols,
                         block_spring_constant=data.spring_constant,
                         plate_spring_constant=data.plate_spring_constant,
                         static_friction=data.static_friction, kinetic_friction=data.kinetic_friction,
                         mass=data.mass, spring_length=data.spring_length,
                         plate_velocity=data.plate_velocity))
    r.set_integrator('dopri5', nsteps=10000)
    r.set_initial_value(blocks.array)
    progress_at = 0
    start = datetime.now().timestamp()
    while r.successful() and r.t < 100:
        values = r.integrate(r.t+data.time_interval)
        data.add_slice(r.t, values)
        if r.t > progress_at:
            current = datetime.now().timestamp() - start
            print('Time-step: {}, Real-time: {:.2f}s'.format(progress_at, current))
            progress_at += 1
    elapsed = datetime.now().timestamp() - start
    data.total_time = elapsed
    print('Finished at: {:.2f}s'.format(elapsed))


if __name__ == '__main__':
    data = Data()
    data.rows = 3
    data.cols = 3
    data.spring_length = 2.0
    data.mass = 1.0
    data.spring_constant = 0.8
    data.static_friction = 1.0 / (data.mass.get() * g)
    data.kinetic_friction = 10.0
    data.plate_velocity = 0.01
    data.plate_spring_constant = 1.0
    data.time_interval = 0.2
    file_name = 'data/{}x{}-{}-V{}.dat'.format(data.rows.get(), data.cols.get(),
                                                datetime.now().strftime('%Y%m%dT%H%M%SZ'),
                                                Data.VERSION)

    solve(data)
    #winsound.Beep(2500, 500)
    write_data(file_name, data)
    print('File saved to: {}'.format(file_name))
