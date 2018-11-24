#include "frictionforce.h"

#include <cmath>


constexpr double epsilon {1e-3};
constexpr double g {9.81};

namespace {
    template <typename T>
    constexpr int sign(T val)
    {
        return (T{0} < val) - (val < T{0});
    }
}

double friction_force(double velocity, double static_coefficient, double kinetic_coefficient, double mass)
{
    double cutoff {static_coefficient * mass * g};
    if(velocity > epsilon)
    {
        return -1 / (kinetic_coefficient * velocity + (1 / cutoff));
    } else if(velocity < -epsilon)
    {
        return - 1 / (kinetic_coefficient * velocity - (1 / cutoff));
    } else
    {
        double y1 {1 / (kinetic_coefficient * epsilon + (1 / cutoff))};
        double y2 {- 1 / (kinetic_coefficient * epsilon + (1 / cutoff))};
        return (y2-y1)*(velocity+epsilon)/(2*epsilon) + y1;
    }
}

double scaled_friction_force(double velocity, double alpha)
{
    if (velocity < -epsilon or velocity > epsilon)
    {
        return - sign(velocity) / (2*alpha*std::abs(velocity) + 1);
    } else
    {
        return - (velocity / (2*alpha*epsilon + 1)) / epsilon;
    }
}