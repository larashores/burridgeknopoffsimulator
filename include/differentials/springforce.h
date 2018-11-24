#pragma once

#include <boost/python/numpy.hpp>


class SpringForce
{
public:
    SpringForce(int rows, int cols, double spring_constant, double spring_length, double mass);

    boost::python::numpy::ndarray differentiate(boost::python::numpy::ndarray& current_array) const;

private:
    const int m_rows;
    const int m_cols;
    const double m_spring_constant;
    const double m_spring_length;
    const double m_mass;
};
