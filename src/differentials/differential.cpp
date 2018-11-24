#include "differentials/differential.h"
#include "utilities.h"

#include <sstream>

namespace NP = boost::python::numpy;


Differential::Differential(int rows, int cols) :
        m_rows{rows},
        m_cols{cols}
{
    if (rows == 1 and cols >= 2)
    {
        m_diff_func = [this](auto current){return diff_one_dim(current);};
    } else
    {
        m_diff_func = [this](auto current){return diff_full(current);};
    }
}

boost::python::numpy::ndarray Differential::differentiate(NP::ndarray& current_ndarray) const
{
    return m_diff_func(current_ndarray);
}

boost::python::numpy::ndarray Differential::diff_full(boost::python::numpy::ndarray&) const
{
    auto results_ndarray {NP::zeros(boost::python::make_tuple(m_rows*m_cols*2), NP::dtype::get_builtin<double>())};
    return results_ndarray;
}

boost::python::numpy::ndarray Differential::diff_one_dim(boost::python::numpy::ndarray& current_array) const
{
    return diff_full(current_array);
}
