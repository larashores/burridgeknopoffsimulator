#include <boost/python.hpp>
#include <boost/python/numpy.hpp>

#include "blockarray.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;

BOOST_PYTHON_MODULE(burridgeknopoff)
{
    Py_Initialize();
    NP::initialize();
    PY::class_<BlockArray>("BlockArray", PY::init<PY::object&>())
            .def("get", &BlockArray::get);
}
