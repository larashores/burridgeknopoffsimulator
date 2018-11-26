#include "odesolver/rungekutta4.h"

RungeKutta4::RungeKutta4(OdeSolver::FuncType difeqs) :
        RungeKutta{{0, .5, .5, 1},
                   {1, 2, 2, 1},
                   difeqs}
{

}
