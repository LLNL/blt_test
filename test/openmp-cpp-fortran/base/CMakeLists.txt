cmake_minimum_required(VERSION 3.14)

project(openmp-cpp-fortran LANGUAGES CXX)

set(BLT_CXX_STD c++14 CACHE STRING "")
set(ENABLE_OPENMP On CACHE BOOL "")
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

blt_export_tpl_targets(EXPORT openmp-cpp-fortran-targets NAMESPACE blt)
blt_install_tpl_setups(DESTINATION lib/cmake/)
install(EXPORT openmp-cpp-fortran-targets
    DESTINATION  lib/cmake/openmp-cpp-fortran)

blt_add_library(
    NAME openmp-cpp-fortran
    SOURCES openmp-cpp-fortran.cpp
    DEPENDS_ON openmp)

# install library
install(TARGETS openmp-cpp-fortran
  EXPORT openmp-cpp-fortran-targets)

# export targets & blt targets
install(FILES
  ${PROJECT_SOURCE_DIR}/openmp-cpp-fortran-config.cmake
  DESTINATION lib/cmake/openmp-cpp-fortran)

install(EXPORT openmp-cpp-fortran-targets
    DESTINATION  lib/cmake/openmp-cpp-fortran)
