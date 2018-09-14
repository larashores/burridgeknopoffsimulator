from physicalconstants import g


def linear_kinetic_friction(spring_force, static_coefficient, kinetic_coefficient, mass):
    cutoff = static_coefficient * mass * g
    friction = kinetic_coefficient * mass * g
    if spring_force >= cutoff:
        return -friction
    elif spring_force <= -cutoff:
        return friction
    else:
        return 0


def velocity_dependent_friction(velocity, static_coefficient, kinetic_coefficient, mass):
    cutoff = static_coefficient * mass * g
    return -1 / (kinetic_coefficient * velocity + (1 / cutoff))