#pragma once

#include <boost/python/numpy.hpp>


class ScaledFrictionalForce
{
public:
    ScaledFrictionalForce(int rows, int cols, double plate_velocity, double alpha);

    boost::python::numpy::ndarray differentiate(boost::python::numpy::ndarray& current_array) const;

private:
    const int m_rows;
    const int m_cols;
    const double m_plate_velocity;
    const double m_alpha;
};
