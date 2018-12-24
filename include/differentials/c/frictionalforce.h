#pragma once

#include <valarray>

class FrictionalForce
{
public:
    FrictionalForce(int rows, int cols, double plate_velocity, double alpha);

    void differentiate(const std::valarray<double>& current,
                       std::valarray<double>& results) const;

private:
    const int m_rows;
    const int m_cols;
    const double m_plate_velocity;
    const double m_alpha;
};
