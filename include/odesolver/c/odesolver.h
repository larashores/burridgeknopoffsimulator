#pragma once

#include <functional>
#include <memory>
#include <valarray>

#include "differentials/c/difeq.h"


namespace odesolver {

class OdeSolver
{
public:
    OdeSolver(std::shared_ptr<Difeq> difeq);
    virtual ~OdeSolver() = default;

    void resize(std::size_t size);
    void set_current_values(const std::valarray<double>& values);
    void set_step_size(double step);
    void step();

    std::valarray<double>& current_values();
    const std::valarray<double>& current_values() const;
    double time() const;


protected:
    std::shared_ptr<Difeq> m_difeqs;
    std::valarray<double> m_current_values;
    double m_time;
    double m_step_size;

private:
    virtual void start() {};
    virtual void finish() {};
    virtual void step_impl() = 0;
};

}  // namespace odesolver
