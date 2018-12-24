#include "differentials/c/frictionalforce.h"
#include "frictionforce.h"
#include "cutilities.h"


FrictionalForce::FrictionalForce(int rows, int cols, double plate_velocity, double alpha) :
        m_rows{rows},
        m_cols{cols},
        m_plate_velocity{plate_velocity},
        m_alpha{alpha}
{
}

void FrictionalForce::differentiate(const std::valarray<double>& current,
                                     std::valarray<double>& results) const
{
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double force {scaled_friction_force(m_plate_velocity + get_velocity(current, m_cols, i, j), m_alpha)};
            add_velocity(results, m_cols, i, j, force);
        }
    }
}