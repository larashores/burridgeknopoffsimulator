cmake_minimum_required(VERSION 3.12)
project(BurridgeKnopoffLib VERSION 1.0)

#-----------Project Files------------

set(SOURCE_FILES src/python.cpp
                 src/utilities.cpp
                 src/frictionforce.cpp
                 src/differentials/springforce.cpp
                 src/differentials/plateforce.cpp
                 src/differentials/positionupdater.cpp
                 src/differentials/frictionalforce.cpp
                 src/differentials/bkdifeq.cpp
                 src/odesolver/odesolver.cpp
                 src/odesolver/euler.cpp
                 src/odesolver/rungekutta.cpp
                 src/odesolver/rungekutta4.cpp
                 src/python/odesolver/py_odesolver.cpp)

set(HEADER_FILES include/utilities.h
                 include/frictionforce.h
                 include/differentials/springforce.h
                 include/differentials/plateforce.h
                 include/differentials/positionupdater.h
                 include/differentials/frictionalforce.h
                 include/differentials/bkdifeq.h
                 include/differentials/difeq.h
                 include/odesolver/odesolver.h
                 include/odesolver/euler.h
                 include/odesolver/rungekutta.h
                 include/odesolver/rungekutta4.h
                 include/python/odesolver/py_odesolver.h)

#------------------------------------

#-----------Build options------------
set(ARCHITECTURE x64)
set(BUILD_STATIC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-std=c++17 -Wall -Wextra -pedantic -g")
set(CMAKE_CXX_FLAGS_RELEASE "-O2")
set(CMAKE_CXX_COMPILER_ARCHITECTURE_ID ${ARCHITECTURE})  # Used to find Boost libraries correctly
#------------------------------------

#------Find boost python and numpy library-----
set(BOOST_ROOT C:/boost_1_69_0)
set(BOOST_LIBRARYDIR C:/boost_1_69_0/stage/${ARCHITECTURE}/lib)
set(Boost_USE_STATIC_LIBS ${BUILD_STATIC})
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME ${BUILD_STATIC})
if(${BUILD_STATIC})
    add_definitions(-DBOOST_PYTHON_STATIC_LIB)
    add_definitions(-DBOOST_NUMPY_STATIC_LIB)
endif()
find_package(Boost 1.69.0 REQUIRED python37 numpy37)
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