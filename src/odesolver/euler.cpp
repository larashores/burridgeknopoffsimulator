#include "odesolver/euler.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;


void Euler::step_impl()
{
    auto derivatives {PY::call<NP::ndarray>(m_difeqs, m_time, m_current_values)};
    m_current_values += derivatives * m_step_size;
}