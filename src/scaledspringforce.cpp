#include "scaledspringforce.h"
#include "utilities.h"

#include <sstream>


namespace NP = boost::python::numpy;

ScaledSpringForce::ScaledSpringForce(int rows, int cols, double spring_length, double l) :
        m_rows{rows},
        m_cols{cols},
        m_spring_length{spring_length},
        m_l_squared{l*l}
{
}

boost::python::numpy::ndarray ScaledSpringForce::differentiate(NP::ndarray& current_ndarray) const
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
