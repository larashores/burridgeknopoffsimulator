from datetime import datetime

from simulation.simulation import solve
from files.scaledata import ScaledData
from files.util import write_data
from simulation.scaleddifferential import ScaledDifferential

import winsound


if __name__ == '__main__':
    import random
    data = ScaledData()
    info = data.run_info

    info.rows = 3
    info.cols = 3
    info.spring_length = 3.0
    info.plate_velocity = 0.01
    info.alpha = 2.5
    info.l = 10
    info.time_interval = .2
    period = 2 / info.plate_velocity
    steps = int(period / info.time_interval)

    differential = ScaledDifferential(info.rows, info.cols,
                                      scaled_spring_length=info.spring_length,
                                      scaled_plate_velocity=info.plate_velocity,
                                      alpha=info.alpha,
                                      l=info.l)
    file_name = 'data/S-{}x{}-{}-V{}.dat'.format(info.rows, info.cols,
                                                 datetime.now().strftime('%Y%m%dT%H%M%SZ'),
                                                 ScaledData.VERSION)
    print('Loading period: {}'.format(2 / info.plate_velocity))
    print('Initial steps: {}'.format(steps))


    solve(data, differential, 0, steps)
    winsound.Beep(int(100 + random.random() * 2900), 500)
    write_data(file_name, data)
    print('File saved to: {}'.format(file_name))
