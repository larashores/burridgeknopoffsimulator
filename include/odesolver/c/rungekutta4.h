#pragma once

#include "odesolver/c/rungekutta.h"


namespace odesolver {

class RungeKutta4 : public RungeKutta
{
public:
    explicit RungeKutta4(std::shared_ptr<Difeq> difeq);
};

}  // namespace odesolver
