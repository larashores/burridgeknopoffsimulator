#include <boost/python/numpy.hpp>

#include "odesolver/rungekutta4.h"
#include "odesolver/odesolver.h"


void set_current_values(odesolver::OdeSolver& solver, const boost::python::object& values);

boost::python::numpy::ndarray current_values(const odesolver::OdeSolver& solver);
