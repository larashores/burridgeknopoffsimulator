#include "odesolver/rungekutta.h"

#include <numeric>
#include <sstream>

namespace PY = boost::python;
namespace NP = boost::python::numpy;

RungeKutta::RungeKutta(const std::vector<double>& step_weights,
                       const std::vector<double>& weight_coefficients,
                       OdeSolver::FuncType difeqs) :
    OdeSolver{difeqs},
    m_step_weights{step_weights},
    m_weight_coefficients{weight_coefficients},
    m_total_weight{std::accumulate(weight_coefficients.begin(), weight_coefficients.end(), 0.0)}
{

}

void RungeKutta::step_impl()
{
    NP::ndarray derivative {NP::zeros(m_current_values.get_nd(),
                                      m_current_values.get_shape(),
                                      m_current_values.get_dtype())};
    NP::ndarray average_derivative {NP::zeros(m_current_values.get_nd(),
                                              m_current_values.get_shape(),
                                              m_current_values.get_dtype())};
    for (auto i = 0u; i < m_step_weights.size(); i++)
    {
        derivative = PY::call<NP::ndarray>(m_difeqs,
                                           m_time + m_step_size * m_step_weights[i],
                                           m_current_values + derivative * m_step_weights[i]);
        derivative *= m_step_size;
        average_derivative += derivative * m_weight_coefficients[i];
    }
    m_current_values += average_derivative * (1 / m_total_weight);
}
