cmake_minimum_required(VERSION 3.14)

project(mpi-cpp-fortran LANGUAGES CXX)

set(BLT_CXX_STD c++14 CACHE STRING "")
set(ENABLE_MPI On CACHE BOOL "")
set(BLT_EXPORT_THIRDPARTY On CACHE BOOL "")

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

blt_install_tpl_setups(DESTINATION lib/cmake/)

blt_add_library(
    NAME mpi-cpp-fortran
    SOURCES mpi-cpp-fortran.cpp
    DEPENDS_ON mpi)

# install library
install(TARGETS mpi-cpp-fortran
  EXPORT mpi-cpp-fortran-targets)

# export targets & blt targets
install(FILES
  ${PROJECT_SOURCE_DIR}/mpi-cpp-fortran-config.cmake
  DESTINATION lib/cmake/mpi-cpp-fortran)

install(EXPORT mpi-cpp-fortran-targets
    DESTINATION  lib/cmake/mpi-cpp-fortran)
