#include <boost/python/numpy.hpp>

#include "odesolver/c/rungekutta4.h"
#include "odesolver/c/odesolver.h"


void set_current_values(odesolver::OdeSolver& solver, const boost::python::object& values);

boost::python::numpy::ndarray current_values(const odesolver::OdeSolver& solver);
