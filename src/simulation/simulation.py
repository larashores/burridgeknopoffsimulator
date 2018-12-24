import random
from datetime import datetime
from scipy.integrate import ode
from odesolver.rungekutta import RungeKutta4
import burridgeknopoff as bk

from simulation.blockarray import BlockArray


def solve(data, differential, initial_steps, steps):
    print('Creating initial data')
    blocks = BlockArray(data.run_info.rows, data.run_info.cols)
    for i in range(data.run_info.rows):
        for j in range(data.run_info.cols):
            blocks.positions[i, j] = data.run_info.spring_length * (j + random.random() / 3)
    print('Initial data created')
    r = bk.RungeKutta4(differential)
    r.set_step_size(.0001)
    r.set_current_values(blocks.array)
    start = datetime.now().timestamp()
    progress_at = start + 3
    for step in range(steps+initial_steps):
        for _ in range(int(data.run_info.time_interval / .001)):
            r.step()
        if step > initial_steps:
            data.add_slice(r.time(), r.current_values())
        current = datetime.now().timestamp()
        if current > progress_at:
            print('Step: {}, Time: {}, Real-time: {:.2f}s'.format(step, r.time(), current - start))
            progress_at = current + 3
    elapsed = datetime.now().timestamp() - start
    data.run_info.total_time = elapsed
    print('Finished at: {:.2f}s'.format(elapsed))
