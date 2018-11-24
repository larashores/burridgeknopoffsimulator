#pragma once

#include <boost/python/numpy.hpp>


class ScaledSpringForce
{
public:
    ScaledSpringForce(int rows, int cols, double spring_length, double l);

    boost::python::numpy::ndarray differentiate(boost::python::numpy::ndarray& current_array) const;

private:
    boost::python::numpy::ndarray diff_full(boost::python::numpy::ndarray& current_array) const;
    boost::python::numpy::ndarray diff_one_dim(boost::python::numpy::ndarray& current_array) const;

    const int m_rows;
    const int m_cols;
    const double m_spring_length;
    const double m_l_squared;
    std::function<boost::python::numpy::ndarray(boost::python::numpy::ndarray&)> m_diff_func;
};
