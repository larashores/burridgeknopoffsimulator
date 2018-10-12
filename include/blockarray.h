#pragma once

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>


class BlockArray
{
public:
    BlockArray(boost::python::numpy::ndarray& array);

private:
    boost::python::numpy::ndarray& m_array;
};