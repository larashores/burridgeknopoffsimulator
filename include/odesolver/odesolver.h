#pragma once

#include <functional>
#include <boost/python/numpy.hpp>


class OdeSolver
{
public:
    using FuncType = PyObject*;

    OdeSolver(FuncType difeq, double start_time = 0);
    virtual ~OdeSolver() = default;

    double time() const;

    void set_current_values(const boost::python::object& values);
    void set_step_size(double step);

    boost::python::numpy::ndarray current_values();

    void step();

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