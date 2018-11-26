#pragma once

#include "odesolver/odesolver.h"


class Euler : public OdeSolver
{
public:
    using OdeSolver::OdeSolver;

private:
    void step_impl() override;
};
