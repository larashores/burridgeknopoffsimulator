#include "odesolver/euler.h"


namespace odesolver {

void Euler::step_impl()
{
    m_current_values += m_difeqs->differentiate(m_time, m_current_values) * m_step_size;
}

}  // namespace odesolver
