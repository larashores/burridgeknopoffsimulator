#include "odesolver/rungekutta.h"

#include <numeric>
#include <sstream>
#include <valarray>


namespace odesolver {

RungeKutta::RungeKutta(const std::vector<double>& step_weights,
                       const std::vector<double>& weight_coefficients,
                       std::shared_ptr<Difeq> difeqs) :
    OdeSolver{difeqs},
    m_step_weights{step_weights},
    m_weight_coefficients{weight_coefficients},
    m_total_weight{std::accumulate(weight_coefficients.begin(), weight_coefficients.end(), 0.0)}
{

}

void RungeKutta::step_impl()
{
    std::valarray<double> derivative (m_current_values.size());
    std::valarray<double> average_derivative (m_current_values.size());
    for (auto i = 0u; i < m_step_weights.size(); i++)
    {
        derivative = m_difeqs->differentiate(m_time + m_step_size * m_step_weights[i],
                                             m_current_values + derivative * m_step_weights[i]) * m_step_size;
        average_derivative += derivative * m_weight_coefficients[i];
    }
    m_current_values += average_derivative / m_total_weight;
}

}  // namespace odesolver
