#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

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

    PY::def("friction_force", friction_force);
    PY::def("scaled_friction_force", scaled_friction_force);
}
