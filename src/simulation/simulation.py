import random
from datetime import datetime
from scipy.integrate import ode

from simulation.blockarray import BlockArray


def solve(data, differential, initial_steps, steps):
    print('Creating initial data')
    blocks = BlockArray(data.rows, data.cols)
    for i in range(data.rows):
        for j in range(data.cols):
            blocks.positions[i, j] = data.spring_length * (j + random.random() / 3)
    print('Initial data created')
    r = ode(differential)
    r.set_integrator('dopri5', nsteps=10000)
    r.set_initial_value(blocks.array)
    start = datetime.now().timestamp()
    progress_at = start + 3
    for step in range(initial_steps + steps):
        values = r.integrate(r.t+data.time_interval)
        if step > initial_steps:
            data.add_slice(r.t, values)
        current = datetime.now().timestamp()
        if current > progress_at:
            print('Initial steps: {}, Step: {}, Time: {}, Real-time: {:.2f}s'.format(initial_steps,
                                                                                     step, r.t, current - start))
            progress_at = current + 3
        if not r.successful():
            break
    elapsed = datetime.now().timestamp() - start
    data.total_time = elapsed
    print('Finished at: {:.2f}s'.format(elapsed))
