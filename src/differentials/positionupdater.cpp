#include "differentials/positionupdater.h"
#include "utilities.h"

#include <sstream>


namespace NP = boost::python::numpy;

PositionUpdater::PositionUpdater(int rows, int cols) :
        m_rows{rows},
        m_cols{cols}
{
}

void PositionUpdater::differentiate(NP::ndarray& current_ndarray, NP::ndarray& results_ndarray) const
{
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double old {get_position(results, m_cols, i, j)};
            set_position(results, m_cols, i, j, old + get_velocity(current, m_cols, i, j));
        }
    }
}