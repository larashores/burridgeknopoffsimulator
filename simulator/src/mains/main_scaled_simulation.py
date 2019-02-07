from datetime import datetime
from simulation.simulation import solve
from files.scaledata import ScaledData
from files.util import write_data

import burridgeknopoff as bk
import winsound
import random
import sys


if __name__ == '__main__':
    data = ScaledData()
    info = data.run_info

    if len(sys.argv) == 3:
        info.rows = int(sys.argv[1])
        info.cols = int(sys.argv[2])
    else:
        info.rows = 5
        info.cols = 5
    print('Rows: {}, Cols: {}'.format(info.rows, info.cols))
    info.spring_length = 3.0
    info.plate_velocity = 0.01
    info.alpha = 2.5
    info.l = 10
    info.time_interval = .2
    period = 2 / info.plate_velocity
    steps = int(period / info.time_interval)

    differential = bk.ScaledDifferential(info.rows, info.cols,
                                         info.spring_length,
                                         info.plate_velocity,
                                         info.alpha,
                                         info.l)
    file_name = 'data/S-{}x{}-{}-V{}.dat'.format(info.rows, info.cols,
                                                 datetime.now().strftime('%Y%m%dT%H%M%SZ'),
                                                 ScaledData.VERSION)
    print('Loading period: {}'.format(2 / info.plate_velocity))
    print('Initial steps: {}'.format(steps))

    solve(data, differential, 20*steps, 1000*steps)
    winsound.Beep(int(100 + random.random() * 2900), 500)
    write_data(file_name, data)
    print('File saved to: {}'.format(file_name))
