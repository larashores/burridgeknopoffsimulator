#include "frictionforce.h"

#include <cmath>


constexpr double epsilon {0.0};

namespace {
    template <typename T>
    constexpr int sign(T val)
    {
        return (T{0} < val) - (val < T{0});
    }
}

double friction_force(double velocity, double alpha)
{
    if (velocity < -epsilon or velocity > epsilon)
    {
        return - sign(velocity) / (2*alpha*std::abs(velocity) + 1);
    } else
    {
        return - (velocity / (2*alpha*epsilon + 1)) / epsilon;
    }
}