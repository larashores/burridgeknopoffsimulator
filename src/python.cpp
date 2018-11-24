#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

#include "scaledspringforce.h"
#include "springforce.h"
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

    PY::def("friction_force", friction_force);
    PY::def("scaled_friction_force", scaled_friction_force);
}
