#pragma once

#include <boost/python/numpy.hpp>


class ScaledPlateForce
{
public:
    ScaledPlateForce(int rows, int cols, double spring_length);

    void differentiate(boost::python::numpy::ndarray& current_array,
                       boost::python::numpy::ndarray& results_array) const;

private:
    const int m_rows;
    const int m_cols;
    const double m_spring_length;
};
