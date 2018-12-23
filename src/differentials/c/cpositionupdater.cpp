#include "differentials/c/cpositionupdater.h"

#include "cutilities.h"


CPositionUpdater::CPositionUpdater(int rows, int cols) :
        m_rows{rows},
        m_cols{cols}
{
}

void CPositionUpdater::differentiate(const std::valarray<double>& current,
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