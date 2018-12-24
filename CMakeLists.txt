cmake_minimum_required(VERSION 3.12)
project(BurridgeKnopoffLib VERSION 0.1)

#-----------Project Files------------

set(SOURCE_FILES src/python.cpp
                 src/cutilities.cpp
                 src/frictionforce.cpp
                 src/differentials/c/springforce.cpp
                 src/differentials/c/plateforce.cpp
                 src/differentials/c/positionupdater.cpp
                 src/differentials/c/frictionalforce.cpp
                 src/differentials/c/bkdifeq.cpp
                 src/odesolver/c/odesolver.cpp
                 src/odesolver/c/euler.cpp
                 src/odesolver/c/rungekutta.cpp
                 src/odesolver/c/rungekutta4.cpp
                 src/python/odesolver/py_odesolver.cpp)

set(HEADER_FILES include/cutilities.h
                 include/frictionforce.h
                 include/differentials/c/springforce.h
                 include/differentials/c/plateforce.h
                 include/differentials/c/positionupdater.h
                 include/differentials/c/frictionalforce.h
                 include/differentials/c/bkdifeq.h
                 include/differentials/c/difeq.h
                 include/odesolver/c/odesolver.h
                 include/odesolver/c/euler.h
                 include/odesolver/c/rungekutta.h
                 include/odesolver/c/rungekutta4.h
                 include/python/odesolver/py_odesolver.h)

#------------------------------------

#-----------Build options------------
set(ARCHITECTURE x64)
set(BUILD_STATIC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wall -Wextra -pedantic -g -O3")
set(CMAKE_CXX_COMPILER_ARCHITECTURE_ID ${ARCHITECTURE})  # Used to find Boost libraries correctly
#------------------------------------

#------Find boost python and numpy library-----
set(BOOST_LIBRARYDIR C:/boost_1_67_0/stage/${ARCHITECTURE}/lib)
set(Boost_USE_STATIC_LIBS ${BUILD_STATIC})
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME ${BUILD_STATIC})
if(${BUILD_STATIC})
    add_definitions(-DBOOST_PYTHON_STATIC_LIB)
    add_definitions(-DBOOST_NUMPY_STATIC_LIB)
endif()
find_package(Boost 1.67.0 REQUIRED python37 numpy37)
if (Boost_FOUND)
    message(" Boost include directory found at ${Boost_INCLUDE_DIRS}")
    message(" Boost libraries found at ${Boost_LIBRARIES}")
else()
    message(" Boost not found")
    return()
endif()
#-----------------------------------

#-----Find python link library------
find_package(PythonLibs 3.7 REQUIRED)
if (PYTHONLIBS_FOUND)
    message(" Python include directory found at ${PYTHON_INCLUDE_DIRS}")
    message(" Python libraries found at ${PYTHON_LIBRARIES}")
else()
    message(" Python not found")
endif()
#-----------------------------------

#---------Add Python Library--------
add_library(burridgeknopoff MODULE ${SOURCE_FILES} ${HEADER_FILES})
set_target_properties(burridgeknopoff PROPERTIES PREFIX "")
set_target_properties(burridgeknopoff PROPERTIES SUFFIX ".pyd")
target_include_directories(burridgeknopoff PRIVATE include)
target_include_directories(burridgeknopoff SYSTEM PRIVATE ${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
target_link_libraries(burridgeknopoff ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

install(TARGETS burridgeknopoff
        DESTINATION "E:/Users/Vincent/Documents/RIT/Capstone/Capstone 1/simulator"
        CONFIGURATIONS Debug Release)
#-----------------------------------