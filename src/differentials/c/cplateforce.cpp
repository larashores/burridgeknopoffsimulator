#include "differentials/c/cplateforce.h"

#include "cutilities.h"


CPlateForce::CPlateForce(int rows, int cols, double spring_length) :
        m_rows{rows},
        m_cols{cols},
        m_spring_length{spring_length}
{
}

void CPlateForce::differentiate(const std::valarray<double>& current,
                                std::valarray<double>& results) const
{
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double force {j * m_spring_length - get_position(current, m_cols, i, j)};
            add_velocity(results, m_cols, i, j, force);
        }
    }
}