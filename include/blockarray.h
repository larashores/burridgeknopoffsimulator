#pragma once

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>


class BlockArray
{
public:
    explicit BlockArray(boost::python::object& array);
    ~BlockArray();

    double get(int index);

private:
    boost::python::numpy::ndarray m_array;
};