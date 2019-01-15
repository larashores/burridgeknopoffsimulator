#include "differentials/positionupdater.h"

#include "utilities.h"


namespace differentials {

PositionUpdater::PositionUpdater(int rows, int cols) :
        m_rows{rows},
        m_cols{cols}
{
}

void PositionUpdater::differentiate(const std::valarray<double>& current,
                                     std::valarray<double>& results) const
{
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            add_position(results, m_cols, i, j, get_velocity(current, m_cols, i, j));
        }
    }
}

}  // differentials
