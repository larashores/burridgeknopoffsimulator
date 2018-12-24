#pragma once

#include <valarray>
#include <functional>


namespace differentials {

class SpringForce
{
public:
    SpringForce(int rows, int cols, double spring_length, double l);

    void differentiate(const std::valarray<double>& current,
                       std::valarray<double>& results) const;

private:
    void diff_full(const std::valarray<double>& current,
                   std::valarray<double>& results) const;
    void diff_one_dim(const std::valarray<double>& current,
                      std::valarray<double>& results) const;

    const int m_rows;
    const int m_cols;
    const double m_spring_length;
    const double m_l_squared;
    std::function<void(const std::valarray<double>&, std::valarray<double>&)> m_diff_func;
};

}  // differentials
