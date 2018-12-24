#pragma once

#include "rungekutta.h"


namespace odesolver {

class RungeKutta4 : public RungeKutta
{
public:
    RungeKutta4(std::shared_ptr<differentials::Difeq> difeq);
};

}  // namespace odesolver
