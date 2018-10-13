import glob
import os
import sys
import numpy as np

from files.readwrite import read_data
from viewers.tkviewer import view_2d

if __name__ == '__main__':
    if len(sys.argv) == 1:
        files = glob.iglob('data/*')
        file = max(files, key=os.path.getctime)
    elif len(sys.argv) == 2:
        file = os.path.join('data', sys.argv[1])
    else:
        raise TypeError('Usage: [filename]')

    data = read_data(file)
    solution = []
    for values in data.values_list:
        array = np.zeros(len(values))
        for i, value in enumerate(values):
            array[i] = value.get()
        solution.append(array)
    desc = ('rows: {}\n' +
            'cols: {}\n' +
            'm:    {}\n' +
            'v:    {}\n' +
            'k_b:  {}\n' +
            'k_p:  {}\n' +
            'u_s:  {}\n' +
            'u_k:  {}').format(data.rows.get(), data.cols.get(), data.mass.get(), data.plate_velocity.get(),
                                data.spring_constant.get(), data.plate_spring_constant.get(),
                                data.static_friction.get(), data.kinetic_friction.get())
    view_2d(data.rows.get(), data.cols.get(), solution, desc)
