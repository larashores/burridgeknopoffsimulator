import numpy as np
import scipy.optimize as opt
import scipy.odr as odr
import inspect


def rows_to_numpy(string_data):
    """
    Converts data that has been copy-pasted from excel into a 2d array.
    Columns should be seperated by spaces and rows by newlines

    string_data: A string with floats copied from excel
    """
    data = [row.split() for row in string_data.strip().split('\n')]
    return np.array(data, 'f')


def cols_to_numpy(string_data):
    return rows_to_numpy(string_data, ).transpose()


def pprint_matrix(matrix, column_lables=None, *, title=None):
    """
    A pretty printer for 2d arrays

    matrix: The 2d array
    column_labels: Labels for the columns while printing
    """
    if len(matrix.shape) != 2:
        raise ValueError

    rows, cols = matrix.shape
    if str(matrix.dtype).startswith('f'):
        string = ' {:^20.10}' + ' | {:^20.10}' * (cols - 1)
    else:
        string = ' {:^20}' + ' | {:^20}' * (cols - 1)

    if title:
        spaces = 20 + 23 * (cols - 1)
        title_string = '{:^' + str(spaces) + '}'
        print(title_string.format(title))
    if column_lables:
        print(string.format(*column_lables))
    for row in range(rows):
        print(string.format(*matrix[row]))


def pprint_uncertainty_matrix(value_matrix, dvalue_matrix, column_labels=None, *, title=None):
    """
    Accepts a matrix of values, a matrix of uncertainties, and pretty-prints a single matrix
    that has both

    value_matrix: The 2d array of values
    dvalue_matrix: The 2d array of uncertainties where the indices corresponds to value_matrix
    column_labels: Labels for the columns while printing
    """
    if len(value_matrix.shape) == 1 and len(dvalue_matrix.shape) == 1:
        value_matrix = value_matrix.reshape(1, len(value_matrix))
        dvalue_matrix = dvalue_matrix.reshape(1, len(dvalue_matrix))
    elif len(value_matrix.shape) != 2 or len(dvalue_matrix.shape) != 2:
        raise ValueError('Must be 2d or 1d array')

    new = np.zeros(value_matrix.shape, dtype=object)
    for i, j in np.ndindex(value_matrix.shape):
        new[i][j] = uncertainty_str(value_matrix[i][j], dvalue_matrix[i][j])

    pprint_matrix(new, column_labels)


def sci_str(num):
    return '{:e}'.format(num)


def uncertainty_str_decimal(val, dval):
    dstr = sci_str(abs(dval))
    dpow = int(dstr[-3:])
    if sci_str(abs(round(dval, -dpow)))[0] == '1':
        dpow -= 1
    val = round(val, -dpow)
    dval = round(dval, -dpow)

    precision = max(-dpow, 0)
    fmt = '{:.' + str(precision) + 'f}'
    return fmt.format(val), fmt.format(dval)


def uncertainty_str(val, dval):
    """
    Returns a string that holds both a value and an uncertainty

    value: The value
    dvalue: The uncertainty
    """
    vpow = int(sci_str(val)[-3:])
    if -5 <= vpow <= 5:
        return '{} +- {}'.format(*uncertainty_str_decimal(val, dval))
    else:
        val *= 10**-vpow
        dval *= 10**-vpow
        return '({} +- {})e{}'.format(*uncertainty_str_decimal(val, dval), vpow)

def _fit_func(func, xs, ys, dxs=None, dys=None, guesses=None):
    if dxs is None:
        optimal, covarience = opt.curve_fit(func, xs, ys, sigma=dys, absolute_sigma=True, maxfev=10000)
    else:
        data = odr.RealData(xs, ys, dxs, dys)
        new_func = lambda beta, x: func(x, *beta)
        sig = inspect.signature(func)
        options = len(sig.parameters) - 1
        model = odr.Model(new_func)
        odr_obj = odr.ODR(data, model, beta0=[1 for _ in range(options)] if guesses is None else guesses)
        res = odr_obj.run()
        optimal, covarience = res.beta, res.cov_beta
    stddev = np.sqrt(np.diag(covarience))
    return optimal, stddev


def fit_func(func, xs, ys, dxs=None, dys=None, limits=None, guesses=None):
    if limits is not None:
        trim = lambda values: values[limits[0]:limits[1]] if values is not None else None
        values = [trim(values) for values in (xs, ys, dxs, dys)]
    else:
        values = (xs, ys, dxs, dys)
    return _fit_func(func, *values, guesses=guesses)

if __name__ == '__main__':
    print(uncertainty_str(321.8, .0324))
    print(uncertainty_str(321.856, .0324))
    print(uncertainty_str(321.856, 3.86))
    print(uncertainty_str(-321.856, 11.34))
    print(uncertainty_str(3.21856e-10, 3.24e-12))
    print(uncertainty_str(3.21856e10, 3.24e8))
    print(uncertainty_str(3.21856e10, 1.24e8))
    print(uncertainty_str(0.02094495456, 9.541774545e-05))
    print(uncertainty_str(0.02094495456, 9.341774545e-05))
    print(uncertainty_str(3559.8838983606497, 21.815841616631992))
