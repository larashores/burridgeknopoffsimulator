#pragma once

#include <boost/python/numpy.hpp>


class Differential
{
public:
    boost::python::numpy::ndarray differentiate(boost::python::numpy::ndarray& current_array) const;

protected:
    Differential(int rows, int cols);

    const int m_rows;
    const int m_cols;

    virtual boost::python::numpy::ndarray diff_full(boost::python::numpy::ndarray& current_array) const;
    virtual boost::python::numpy::ndarray diff_one_dim(boost::python::numpy::ndarray& current_array) const;

private:
    std::function<boost::python::numpy::ndarray(boost::python::numpy::ndarray&)> m_diff_func;
};