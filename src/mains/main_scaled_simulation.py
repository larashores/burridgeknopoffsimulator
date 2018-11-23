from datetime import datetime

from simulation.simulation import solve
from files.scaledata import ScaledData
from files.util import write_data
from simulation.scaleddifferential import ScaledDifferential

import winsound


if __name__ == '__main__':
    data = ScaledData()

    data.rows = 1
    data.cols = 1
    data.spring_length = 1.0
    data.plate_velocity = 0.01
    data.alpha = 2.5
    data.l = 10
    data.time_interval = 1.0

    differential = ScaledDifferential(data.rows, data.cols,
                                      scaled_spring_length=data.spring_length,
                                      scaled_plate_velocity=data.plate_velocity,
                                      alpha=data.alpha,
                                      l = data.l)
    file_name = 'data/S-{}x{}-{}-V{}.dat'.format(data.rows, data.cols,
                                                datetime.now().strftime('%Y%m%dT%H%M%SZ'),
                                                ScaledData.VERSION)

    solve(data, differential, 100)
    #winsound.Beep(2500, 500)
    write_data(file_name, data)
    print('File saved to: {}'.format(file_name))
