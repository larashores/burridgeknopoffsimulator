#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

#include "python/odesolver/py_odesolver.h"
#include "odesolver/rungekutta4.h"
#include "odesolver/rungekutta.h"
#include "odesolver/odesolver.h"
#include "odesolver/euler.h"
#include "frictionforce.h"
#include "differentials/bkdifeq.h"
#include "differentials/difeq.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;
namespace ODE = odesolver;
namespace DIFF = differentials;

BOOST_PYTHON_MODULE(burridgeknopoff)
{
    Py_Initialize();
    NP::initialize();

    PY::class_<DIFF::Difeq, boost::noncopyable>("Difeq", PY::no_init);
    PY::class_<DIFF::BkDifeq, PY::bases<DIFF::Difeq>>("ScaledDifferential",
                                                      PY::init<int, int, double, double, double, double>());

    PY::class_<ODE::OdeSolver, boost::noncopyable>("OdeSolver", PY::no_init)
            .def("time", &ODE::OdeSolver::time)
            .def("set_step_size", &ODE::OdeSolver::set_step_size)
            .def("set_current_values", python::odesolver::set_current_values)
            .def("current_values", python::odesolver::current_values)
            .def("step", &ODE::OdeSolver::step);

    PY::class_<ODE::Euler, PY::bases<ODE::OdeSolver>>("Euler", PY::no_init);

    PY::class_<ODE::RungeKutta, PY::bases<ODE::OdeSolver>, boost::noncopyable>("RungeKutta", PY::no_init);
    PY::class_<ODE::RungeKutta4, PY::bases<ODE::RungeKutta>>("RungeKutta4", PY::init<std::shared_ptr<DIFF::Difeq>>());
}
