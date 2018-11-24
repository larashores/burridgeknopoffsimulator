#include "differentials/scaledfrictionalforce.h"
#include "frictionforce.h"
#include "utilities.h"

#include <sstream>


namespace NP = boost::python::numpy;

ScaledFrictionalForce::ScaledFrictionalForce(int rows, int cols, double plate_velocity, double alpha) :
        m_rows{rows},
        m_cols{cols},
        m_plate_velocity{plate_velocity},
        m_alpha{alpha}
{
}

boost::python::numpy::ndarray ScaledFrictionalForce::differentiate(NP::ndarray& current_ndarray) const
{
    auto results_ndarray {NP::zeros(boost::python::make_tuple(m_rows*m_cols*2), NP::dtype::get_builtin<double>())};
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double force {scaled_friction_force(m_plate_velocity + get_velocity(current, m_cols, i, j), m_alpha)};
            set_velocity(results, m_cols, i, j, force);
        }
    }
    return results_ndarray;
}