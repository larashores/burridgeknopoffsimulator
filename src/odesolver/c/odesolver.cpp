#include "odesolver/c/odesolver.h"


namespace odesolver {

OdeSolver::OdeSolver(std::shared_ptr<Difeq> difeq) :
        m_difeqs{difeq},
        m_time{0.0},
        m_step_size{0.002}
{
}

double OdeSolver::time() const
{
    return m_time;
}

void OdeSolver::set_current_values(const std::valarray<double>& values)
{
    m_current_values = values;
}

void OdeSolver::set_step_size(double step)
{
    m_step_size = step;
}

std::valarray<double>& OdeSolver::current_values()
{
    return m_current_values;
}

const std::valarray<double>& OdeSolver::current_values() const
{
    return m_current_values;
}

void OdeSolver::step()
{
    m_time += m_step_size;
    step_impl();
}

void OdeSolver::resize(std::size_t size)
{
    m_current_values.resize(size);
}

}  // namespace odesolver
