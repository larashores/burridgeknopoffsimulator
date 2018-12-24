#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

#include "python/odesolver/py_odesolver.h"
#include "odesolver/c/rungekutta4.h"
#include "odesolver/c/rungekutta.h"
#include "odesolver/c/odesolver.h"
#include "odesolver/c/euler.h"
#include "frictionforce.h"
#include "differentials/c/cdifferential.h"
#include "differentials/c/difeq.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;
namespace ODE = odesolver;

BOOST_PYTHON_MODULE(burridgeknopoff)
{
    Py_Initialize();
    NP::initialize();

    PY::class_<Difeq, boost::noncopyable>("Difeq", PY::no_init);
    PY::class_<CDifferential, PY::bases<Difeq>>("ScaledDifferential",
                                                PY::init<int, int, double, double, double, double>());

    PY::class_<ODE::OdeSolver, boost::noncopyable>("OdeSolver", PY::no_init)
            .def("time", &ODE::OdeSolver::time)
            .def("set_step_size", &ODE::OdeSolver::set_step_size)
            .def("set_current_values", set_current_values)
            .def("current_values", current_values)
            .def("step", &ODE::OdeSolver::step);

    PY::class_<ODE::Euler, PY::bases<ODE::OdeSolver>>("Euler", PY::no_init);

    PY::class_<ODE::RungeKutta, PY::bases<ODE::OdeSolver>, boost::noncopyable>("RungeKutta", PY::no_init);
    PY::class_<ODE::RungeKutta4, PY::bases<ODE::RungeKutta>>("RungeKutta4", PY::init<std::shared_ptr<Difeq>>());

    PY::def("friction_force", friction_force);
    PY::def("scaled_friction_force", scaled_friction_force);
}
