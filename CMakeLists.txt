cmake_minimum_required(VERSION 3.12)
project(BurridgeKnopoffLib VERSION 0.1)

#-----------Project Files------------

set(SOURCE_FILES src/python.cpp
                 src/blockarray.cpp)

set(HEADER_FILES include/blockarray.h)

#------------------------------------

#-----------Build options------------
set(ARCHITECTURE x64)
set(BUILD_STATIC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -Wall -Wextra -pedantic -g")
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
        DESTINATION "E:/Users/Vincent/Documents/Capstone/Capstone 1/BurridgeKnopoffLib/build"
        CONFIGURATIONS Debug Release)
#-----------------------------------