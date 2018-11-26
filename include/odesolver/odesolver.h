#pragma once

#include <functional>
#include <boost/python/numpy.hpp>


class OdeSolver
{
    using FuncType = std::function<boost::python::numpy::ndarray(double, boost::python::numpy::ndarray&)>;

    OdeSolver(const FuncType& difeq, double start_time = 0);

    void set_initial_value(boost::python::numpy::ndarray& values);
    void set_step_size(double step);

    boost::python::numpy::ndarray& step();


protected:
    FuncType m_difeqs;
    boost::python::numpy::ndarray m_current_values;
    double m_time;
    double m_step_size;

private:
    virtual void start() {};
    virtual void finish() {};
    virtual void step_impl() = 0;


};