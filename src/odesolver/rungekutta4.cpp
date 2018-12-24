#include "odesolver/rungekutta4.h"


namespace odesolver {

RungeKutta4::RungeKutta4(std::shared_ptr<Difeq> difeq) :
        RungeKutta{{0, .5, .5, 1},
                   {1, 2, 2, 1},
                   difeq}
{

}

}  // namespace odesolver
