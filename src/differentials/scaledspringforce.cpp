#include "differentials/scaledspringforce.h"
#include "utilities.h"

#include <sstream>


namespace NP = boost::python::numpy;

ScaledSpringForce::ScaledSpringForce(int rows, int cols, double spring_length, double l) :
        m_rows{rows},
        m_cols{cols},
        m_spring_length{spring_length},
        m_l_squared{l*l}
{
    if (rows == 1 and cols >= 2)
    {
        m_diff_func = [this](auto current){return diff_one_dim(current);};
    } else
    {
        m_diff_func = [this](auto current){return diff_full(current);};
    }
}

boost::python::numpy::ndarray ScaledSpringForce::differentiate(NP::ndarray& current_ndarray) const
{
    return m_diff_func(current_ndarray);
}

boost::python::numpy::ndarray ScaledSpringForce::diff_full(NP::ndarray& current_ndarray) const
{
    auto results_ndarray {NP::zeros(boost::python::make_tuple(m_rows*m_cols*2), NP::dtype::get_builtin<double>())};
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};

    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double cur {get_position(current, m_cols, i, j)};

            double force {0};
            if(i >= 1) {
                force += get_position(current, m_cols, i - 1, j) - cur;
            } if(i < m_rows - 1) {
                force += get_position(current, m_cols, i + 1, j) - cur;
            } if(j >= 1) {
                force += get_position(current, m_cols, i, j - 1) - cur + m_spring_length;
            } if(j < m_cols - 1) {
                force += get_position(current, m_cols, i, j + 1) - cur - m_spring_length;
            }
            set_velocity(results, m_cols, i, j, force * m_l_squared);
        }
    }

    return results_ndarray;
}

boost::python::numpy::ndarray ScaledSpringForce::diff_one_dim(NP::ndarray& current_ndarray) const
{
    auto results_ndarray {NP::zeros(boost::python::make_tuple(m_rows*m_cols*2), NP::dtype::get_builtin<double>())};
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};

    set_velocity(results, 0,
                 m_l_squared * (get_position(current, 1) - get_position(current, 0) - m_spring_length));
    set_velocity(results, m_cols - 1, m_l_squared *
                                      (get_position(current, m_cols-2) - get_position(current, m_cols-1) + m_spring_length));
    for(int j=1; j < m_cols - 1; j++)
    {
        double force{m_l_squared * (get_position(current, j - 1)
                                    + get_position(current, j + 1)
                                    - 2 * get_position(current, j))};

        set_velocity(results, j, force);
    }

    return results_ndarray;
}
