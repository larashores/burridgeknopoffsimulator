import glob
import os
import sys

from files.readwrite import read_data
from viewers.tkviewer2d import view_2d

if __name__ == '__main__':
    if len(sys.argv) == 1:
        files = glob.iglob('data/*')
        file = max(files, key=os.path.getctime)
    elif len(sys.argv) == 2:
        file = os.path.join('data', sys.argv[1])
    else:
        raise TypeError('Usage: [filename]')
    rows, cols, times, solution = read_data(file)
    view_2d(rows, cols, solution)
