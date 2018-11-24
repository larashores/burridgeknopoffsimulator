#pragma once

double friction_force(double velocity, double static_coefficient, double kinetic_coefficient, double mass);

double scaled_friction_force(double velocity, double alpha);