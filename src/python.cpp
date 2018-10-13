#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

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

    PY::def("friction_force", friction_force);
}
