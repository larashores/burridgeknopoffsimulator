#include "blockarray.h"

#include <sstream>

namespace PY = boost::python;
namespace NP = boost::python::numpy;

BlockArray::BlockArray(PY::object& array) :
    m_array{NP::from_object(*array)}
{
    //Py_INCREF(&array);
    std::ostringstream stream;
    stream << "object size: " << m_array.get_nd() << std::endl;
    PySys_WriteStdout(stream.str().c_str());
}



double BlockArray::get(int index)
{
    int size {m_array.get_dtype().get_itemsize()};
    auto array {reinterpret_cast<double*>(m_array.get_data())};
    return array[index];
}

BlockArray::~BlockArray()
{
    //Py_DECREF(&m_array);
}
