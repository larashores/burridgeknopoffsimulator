#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

#include "odesolver/rungekutta4.h"
#include "odesolver/rungekutta.h"
#include "odesolver/odesolver.h"
#include "odesolver/euler.h"
#include "differentials/positionupdater.h"
#include "differentials/scaledfrictionalforce.h"
#include "differentials/scaledplateforce.h"
#include "differentials/scaledspringforce.h"
#include "differentials/springforce.h"
#include "frictionforce.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;


BOOST_PYTHON_MODULE(burridgeknopoff)
{
    Py_Initialize();
    NP::initialize();
    PY::class_<SpringForce>("SpringForce", PY::init<int, int, double, double, double>())
            .def("__call__", &SpringForce::differentiate);
    PY::class_<ScaledSpringForce>("ScaledSpringForce", PY::init<int, int, double, double>())
            .def("__call__", &ScaledSpringForce::differentiate);
    PY::class_<ScaledFrictionalForce>("ScaledFrictionalForce", PY::init<int, int, double, double>())
            .def("__call__", &ScaledFrictionalForce::differentiate);
    PY::class_<ScaledPlateForce>("ScaledPlateForce", PY::init<int, int, double>())
            .def("__call__", &ScaledPlateForce::differentiate);
    PY::class_<PositionUpdater>("PositionUpdater", PY::init<int, int>())
            .def("__call__", &PositionUpdater::differentiate);


    PY::class_<OdeSolver, boost::noncopyable>("OdeSolver", PY::no_init)
              .def("time", &OdeSolver::time)
            .def("set_current_values", &OdeSolver::set_current_values)
            .def("set_step_size", &OdeSolver::set_step_size)
            .def("current_values", &OdeSolver::current_values)
            .def("step", &OdeSolver::step);

    PY::class_<Euler, PY::bases<OdeSolver>>("Euler", PY::init<OdeSolver::FuncType, double>());

    PY::class_<RungeKutta, PY::bases<OdeSolver>, boost::noncopyable>("RungeKutta", PY::no_init);
    PY::class_<RungeKutta4, PY::bases<RungeKutta>>("RungeKutta4", PY::init<OdeSolver::FuncType, double>());

    PY::def("friction_force", friction_force);
    PY::def("scaled_friction_force", scaled_friction_force);
}
