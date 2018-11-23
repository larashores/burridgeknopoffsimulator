import random
from datetime import datetime

from scipy.integrate import ode

from files.scaledata import ScaledData
from files.util import write_data
from simulation.blockarray import BlockArray
from simulation.scaleddifferential import ScaledDifferential
from physicalconstants import g

import winsound


def solve(data):
    print('Creating initial data')
    blocks = BlockArray(data.rows.get(), data.cols.get())
    for i in range(data.rows.get()):
        for j in range(data.cols.get()):
            blocks.positions[i, j] = data.spring_length.get() * (j + random.random() / 3)
    print('Initial data created')
    r = ode(ScaledDifferential(data.rows.get(), data.cols.get(),
                               scaled_spring_length=data.spring_length.get(),
                               scaled_plate_velocity=data.plate_velocity.get(),
                               alpha=data.alpha.get(),
                               l = data.l.get()))
    r.set_integrator('dopri5', nsteps=10000)
    r.set_initial_value(blocks.array)
    progress_at = 0
    start = datetime.now().timestamp()
    while r.successful() and r.t < 300:
        values = r.integrate(r.t+data.time_interval.get())
        data.add_slice(r.t, values)
        if r.t > progress_at:
            current = datetime.now().timestamp() - start
            print('Time-step: {}, Real-time: {:.2f}s'.format(progress_at, current))
            progress_at += 1
    elapsed = datetime.now().timestamp() - start
    data.total_time = elapsed
    print('Finished at: {:.2f}s'.format(elapsed))


if __name__ == '__main__':
    data = ScaledData()

    data.rows = 1
    data.cols = 1
    data.spring_length = 1.0
    data.plate_velocity = 0.01
    data.alpha = 2.5
    data.l = 10
    data.time_interval = 2.0
    file_name = 'data/S-{}x{}-{}-V{}.dat'.format(data.rows.get(), data.cols.get(),
                                                datetime.now().strftime('%Y%m%dT%H%M%SZ'),
                                                ScaledData.VERSION)

    solve(data)
    #winsound.Beep(2500, 500)
    write_data(file_name, data)
    print('File saved to: {}'.format(file_name))
