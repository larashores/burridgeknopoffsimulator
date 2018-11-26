#pragma once

#include "odesolver/rungekutta.h"


class RungeKutta4 : public RungeKutta
{
public:
    explicit RungeKutta4(OdeSolver::FuncType difeqs);
};