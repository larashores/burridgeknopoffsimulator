#include "positionupdater.h"
#include "utilities.h"

#include <sstream>


namespace NP = boost::python::numpy;

PositionUpdater::PositionUpdater(int rows, int cols) :
        m_rows{rows},
        m_cols{cols}
{
}

boost::python::numpy::ndarray PositionUpdater::differentiate(NP::ndarray& current_ndarray) const
{
    auto results_ndarray {NP::zeros(boost::python::make_tuple(m_rows*m_cols*2), NP::dtype::get_builtin<double>())};
    auto results {reinterpret_cast<double*>(results_ndarray.get_data())};
    auto current {reinterpret_cast<double*>(current_ndarray.get_data())};
    for(int i=0; i < m_rows; i++)
    {
        for(int j=0; j < m_cols; j++)
        {
            double next {get_velocity(current, m_cols, i, j)};
            set_position(results, m_cols, i, j, next);
        }
    }
    return results_ndarray;
}