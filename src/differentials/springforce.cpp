#include "differentials/springforce.h"
#include "utilities.h"

#include <sstream>

namespace NP = boost::python::numpy;

SpringForce::SpringForce(int rows, int cols, double spring_constant, double spring_length, double mass) :
    m_rows{rows},
    m_cols{cols},
    m_spring_constant{spring_constant},
    m_spring_length{spring_length},
    m_mass{mass}
{
}

boost::python::numpy::ndarray SpringForce::differentiate(NP::ndarray& current_ndarray) const
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
            set_velocity(results, m_cols, i, j, force * (m_spring_constant / m_mass));
        }
    }
    return results_ndarray;
}
