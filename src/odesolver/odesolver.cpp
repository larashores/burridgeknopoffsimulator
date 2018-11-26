#include "odesolver/odesolver.h"

namespace NP = boost::python::numpy;


OdeSolver::OdeSolver(const OdeSolver::FuncType& difeqs,
                     double start_time) :
        m_difeqs{difeqs},
        m_current_values{NP::zeros(boost::python::make_tuple(0), NP::dtype::get_builtin<double>())},
        m_time{start_time},
        m_step_size{0.001}
{
}

void OdeSolver::set_initial_value(boost::python::numpy::ndarray& values)
{
    m_current_values = values;
}

void OdeSolver::set_step_size(double step)
{
    m_step_size = step;
}

boost::python::numpy::ndarray& OdeSolver::step()
{
    m_time += m_step_size;
    step_impl();
    return m_current_values;
}

