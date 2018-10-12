#include "blockarray.h"

namespace PY = boost::python;
namespace NP = boost::python::numpy;

BlockArray::BlockArray(NP::ndarray& array) :
    m_array{array}
{

}
