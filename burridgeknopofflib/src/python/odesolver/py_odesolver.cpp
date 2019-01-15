#include "python/odesolver/py_odesolver.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;


namespace python::odesolver {

void set_current_values(::odesolver::OdeSolver& solver, const PY::object& values)
{
    solver.resize(static_cast<size_t>(PY::len(values)));
    auto& current{solver.current_values()};
    for (auto i = 0u; i < PY::len(values); i++) {
        current[i] = PY::extract<double>(values[i]);
    }
}

NP::ndarray current_values(const ::odesolver::OdeSolver& solver)
{
    auto& current{solver.current_values()};
    NP::ndarray values{NP::empty(PY::make_tuple(current.size()),
                                 NP::dtype::get_builtin<double>())};
    for (auto i = 0u; i < current.size(); i++) {
        values[i] = current[i];
    }
    return values;
}

}  // python
