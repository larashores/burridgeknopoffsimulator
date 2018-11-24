#include "differentials/scaledplateforce.h"
#include "utilities.h"

#include <sstream>


namespace NP = boost::python::numpy;

ScaledPlateForce::ScaledPlateForce(int rows, int cols, double spring_length) :
        m_rows{rows},
        m_cols{cols},
        m_spring_length{spring_length}
{
}

boost::python::numpy::ndarray ScaledPlateForce::differentiate(NP::ndarray& current_ndarray) const
{
    auto results_ndarray {NP::zeros(boost::python::make_tuple(m_rows*m_cols*2), NP::dtype::get_builtin<double>())};
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double force {j * m_spring_length - get_position(current, m_cols, i, j)};
            set_velocity(results, m_cols, i, j, force);
        }
    }
    return results_ndarray;
}