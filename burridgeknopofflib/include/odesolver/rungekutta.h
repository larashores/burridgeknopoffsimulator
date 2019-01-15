#pragma once

#include <odesolver/odesolver.h>


namespace odesolver {

class RungeKutta : public OdeSolver
{
protected:
    RungeKutta(const std::vector<double>& step_weights,
               const std::vector<double>& weight_coefficients,
               std::shared_ptr<differentials::Difeq> difeq);
private:
    void step_impl() override;

    std::vector<double> m_step_weights;
    std::vector<double> m_weight_coefficients;

    double m_total_weight;
};

}  // namespace odesolver
