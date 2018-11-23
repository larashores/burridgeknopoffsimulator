import random
from datetime import datetime
from scipy.integrate import ode

from simulation.blockarray import BlockArray


def solve(data, differential, steps):
    print('Creating initial data')
    blocks = BlockArray(data.rows, data.cols)
    for i in range(data.rows):
        for j in range(data.cols):
            blocks.positions[i, j] = data.spring_length * (j + random.random() / 3)
    print('Initial data created')
    r = ode(differential)
    r.set_integrator('dopri5', nsteps=10000)
    r.set_initial_value(blocks.array)
    progress_at = 0
    start = datetime.now().timestamp()
    while r.successful() and r.t < steps * data.time_interval:
        values = r.integrate(r.t+data.time_interval)
        data.add_slice(r.t, values)
        if r.t > progress_at:
            current = datetime.now().timestamp() - start
            print('Time-step: {}, Real-time: {:.2f}s'.format(progress_at, current))
            progress_at += 1
    elapsed = datetime.now().timestamp() - start
    data.total_time = elapsed
    print('Finished at: {:.2f}s'.format(elapsed))
