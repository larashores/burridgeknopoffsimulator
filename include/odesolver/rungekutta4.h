#pragma once

#include "odesolver/rungekutta.h"


class RungeKutta4 : public RungeKutta
{
public:
    RungeKutta4(OdeSolver::FuncType difeqs, double start_time);
};