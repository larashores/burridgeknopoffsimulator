#include "odesolver/odesolver.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;


OdeSolver::OdeSolver(OdeSolver::FuncType difeqs) :
        m_difeqs{difeqs},
        m_current_values{NP::zeros(boost::python::make_tuple(0), NP::dtype::get_builtin<double>())},
        m_time{0.0},
        m_step_size{0.002}
{
}

double OdeSolver::time() const
{
    return m_time;
}

void OdeSolver::set_current_values(const PY::object& values)
{
    m_current_values = NP::array(values, NP::dtype::get_builtin<double>());
}

void OdeSolver::set_step_size(double step)
{
    m_step_size = step;
}

boost::python::numpy::ndarray OdeSolver::current_values()
{
    return m_current_values.copy();
}

void OdeSolver::step()
{
    m_time += m_step_size;
    step_impl();
}

