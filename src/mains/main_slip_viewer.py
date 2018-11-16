import glob
import os
import sys

from files.readwrite import read_data
from viewers.slipviewer import view_slip

if __name__ == '__main__':
    if len(sys.argv) == 1:
        files = glob.iglob('data/*')
        file = max(files, key=os.path.getctime)
    elif len(sys.argv) == 2:
        file = os.path.join('data', sys.argv[1])
    else:
        raise TypeError('Usage: [filename]')

    data = read_data(file)
    desc = ('rows: {}\n' +
            'cols: {}\n' +
            'm:    {}\n' +
            'v:    {}\n' +
            'l:    {}\n' +
            'k_b:  {}\n' +
            'k_p:  {}\n' +
            'u_s:  {}\n' +
            'u_k:  {}\n' +
            'dt:   {}').format(data.rows.get(), data.cols.get(), data.mass.get(),
                               data.plate_velocity.get(),
                               data.spring_length.get(),
                               data.spring_constant.get(), data.plate_spring_constant.get(),
                               data.static_friction.get(), data.kinetic_friction.get(),
                               data.time_interval.get())
    view_slip(data, desc)