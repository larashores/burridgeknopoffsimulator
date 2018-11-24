#pragma once

#include <boost/python/numpy.hpp>


class PositionUpdater
{
public:
    PositionUpdater(int rows, int cols);

    void differentiate(boost::python::numpy::ndarray& current_array,
                       boost::python::numpy::ndarray& results_array) const;

private:
    const int m_rows;
    const int m_cols;
};