
def potential_energy(time, values, spring_length, k, plate_spring_constant, plate_velocity):
    total_energy = 0
    for i in range(0, len(values)//2 - 1):
        length = values[2*i + 2] - values[2*i]
        energy = .5 * k * (length - spring_length)**2
        total_energy += energy
    for i in range(len(values)//2):
        energy = .5 * plate_spring_constant * (i * spring_length + plate_velocity * time -values[2*i])
        total_energy += energy
    return total_energy
