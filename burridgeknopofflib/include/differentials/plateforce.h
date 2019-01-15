#pragma once

#include <valarray>


namespace differentials {

class PlateForce
{
public:
    PlateForce(int rows, int cols, double spring_length);

    void differentiate(const std::valarray<double>& current,
                       std::valarray<double>& results) const;

private:
    const int m_rows;
    const int m_cols;
    const double m_spring_length;
};

}  // differentials
