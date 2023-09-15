cmake_minimum_required(VERSION 3.14)

project(cuda-mpi-cpp-user LANGUAGES CXX)

set(BLT_CXX_STD c++14 CACHE STRING "")
set(ENABLE_MPI On CACHE BOOL "")

# Load BLT
include(${BLT_SOURCE_DIR}/SetupBLT.cmake)

# Calling find_package sets up the TPL targets needed by the project
# in its argument.
find_package(cuda-mpi-cpp REQUIRED 
             NO_DEFAULT_PATH
             PATHS ${base_install_dir}/lib/cmake/cuda-mpi-cpp
             ${base_install_dir})

if (NOT TARGET cuda)
  message(FATAL_ERROR "Target cuda was not configured successfully during"
                      "downstream project configuration.")
endif()

# The downstream project also introduces mpi, so this target must 
# exist as well.
if (NOT TARGET mpi)
  message(FATAL_ERROR "Target MPI was not configured successfully during"
                      "downstream project configuration.")
endif()

get_target_property(compile_flags mpi INTERFACE_COMPILE_OPTIONS)
message(STATUS "KEYWORD ${compile_flags}")

blt_add_library(
    NAME cuda-mpi-cpp-user
    SOURCES cuda-mpi-cpp-user.cpp
    DEPENDS_ON mpi cuda-mpi-cpp)

blt_add_executable(
    NAME hello-mpi-cuda
    SOURCES cuda-mpi-cpp-user.cpp
    DEPENDS_ON cuda-mpi-cpp-user
)
