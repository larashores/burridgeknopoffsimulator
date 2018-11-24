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

void ScaledFrictionalForce::differentiate(NP::ndarray& current_ndarray, NP::ndarray& results_ndarray) const
{
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double force {scaled_friction_force(m_plate_velocity + get_velocity(current, m_cols, i, j), m_alpha)};
            add_velocity(results, m_cols, i, j, force);
        }
    }
}