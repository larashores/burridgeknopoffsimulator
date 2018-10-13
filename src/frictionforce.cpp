#include "frictionforce.h"


constexpr double epsilon {1e-2};
constexpr double g {9.81};

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