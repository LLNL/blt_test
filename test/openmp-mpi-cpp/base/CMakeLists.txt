cmake_minimum_required(VERSION 3.14)

project(open-mpi-cpp LANGUAGES CXX)

set(BLT_CXX_STD c++14 CACHE STRING "")
set(ENABLE_OPENMP On CACHE BOOL "")

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
  NAME openmp-mpi-cpp
  SOURCES openmp-mpi-cpp.cpp
  HEADERS include/openmp-mpi-cpp.hpp
  DEPENDS_ON openmp)

install(DIRECTORY include/ DESTINATION include FILES_MATCHING PATTERN *.hpp)

# install library
install(TARGETS openmp-mpi-cpp
  EXPORT openmp-mpi-cpp-targets)

# export targets & blt targets
install(FILES
  ${PROJECT_SOURCE_DIR}/openmp-mpi-cpp-config.cmake
  DESTINATION lib/cmake/openmp-mpi-cpp)

install(EXPORT openmp-mpi-cpp-targets
    DESTINATION  lib/cmake/openmp-mpi-cpp)
