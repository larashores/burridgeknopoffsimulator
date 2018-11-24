#pragma once

#include <boost/python/numpy.hpp>


class ScaledSpringForce
{
public:
    ScaledSpringForce(int rows, int cols, double spring_length, double l);

    void differentiate(boost::python::numpy::ndarray& current_array,
                       boost::python::numpy::ndarray& results_array) const;

private:
    void diff_full(boost::python::numpy::ndarray& current_array,
                   boost::python::numpy::ndarray& results_array) const;
    void diff_one_dim(boost::python::numpy::ndarray& current_array,
                      boost::python::numpy::ndarray& results_array) const;

    const int m_rows;
    const int m_cols;
    const double m_spring_length;
    const double m_l_squared;
    std::function<void(boost::python::numpy::ndarray&, boost::python::numpy::ndarray&)> m_diff_func;
};
