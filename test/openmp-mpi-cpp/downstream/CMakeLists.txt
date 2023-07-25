cmake_minimum_required(VERSION 3.14)

project(openmp-cpp-fortran-user LANGUAGES CXX)

set(BLT_CXX_STD c++14 CACHE STRING "")
set(ENABLE_MPI On CACHE BOOL "")

if (NOT BLT_LOADED)
    if (DEFINED BLT_SOURCE_DIR)
      if (NOT EXISTS ${BLT_SOURCE_DIR}/SetupBLT.cmake)
        message(FATAL_ERROR "Given BLT_SOURCE_DIR does not contain SetupBLT.cmake")
      endif()
    else ()
      set (BLT_SOURCE_DIR ${PROJECT_SOURCE_DIR}/../../../blt CACHE PATH "")
  
      if (NOT EXISTS ${BLT_SOURCE_DIR}/SetupBLT.cmake)
        message(FATAL_ERROR "\
        The BLT submodule is not present. \
        If in git repository run the following two commands:\n \
        git submodule init\n \
        git submodule update")
      endif ()
    endif ()
  
    include(${BLT_SOURCE_DIR}/SetupBLT.cmake)
endif()

message(STATUS "${BLT_ROOT_DIR}")

find_package(openmp-mpi-cpp REQUIRED 
             NO_DEFAULT_PATH
             PATHS ${base_install_dir}/lib/cmake/openmp-mpi-cpp
             ${base_install_dir})

blt_add_library(
    NAME openmp-mpi-cpp-user
    SOURCES openmp-mpi-cpp-user.cpp
    DEPENDS_ON mpi openmp-mpi-cpp)

blt_add_executable(
    NAME hello-mpi-openmp
    SOURCES openmp-mpi-cpp-user.cpp
    DEPENDS_ON openmp-mpi-cpp-user
)
