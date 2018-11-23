from datetime import datetime

from files.data import Data
from files.util import write_data
from simulation.differential import Differential
from simulation.simulation import solve
from physicalconstants import g

import winsound

if __name__ == '__main__':
    data = Data()
    data.rows = 1
    data.cols = 1
    data.spring_length = 2.0
    data.mass = 1.0
    data.spring_constant = 0.8
    data.static_friction = 1.0 / (data.mass * g)
    data.kinetic_friction = 10.0
    data.plate_velocity = 0.01
    data.plate_spring_constant = 1.0
    data.time_interval = 0.2

    differential = Differential(data.rows, data.cols,
                                block_spring_constant=data.spring_constant,
                                plate_spring_constant=data.plate_spring_constant,
                                static_friction=data.static_friction, kinetic_friction=data.kinetic_friction,
                                mass=data.mass, spring_length=data.spring_length,
                                plate_velocity=data.plate_velocity)
    file_name = 'data/{}x{}-{}-V{}.dat'.format(data.rows, data.cols,
                                                datetime.now().strftime('%Y%m%dT%H%M%SZ'),
                                                Data.VERSION)

    solve(data, differential, 100)
    #winsound.Beep(2500, 500)
    write_data(file_name, data)
    print('File saved to: {}'.format(file_name))
