cmake_minimum_required(VERSION 3.14)

project(openmp-cpp-fortran-user LANGUAGES CXX Fortran)

message(STATUS ${base_install_dir})

find_package(openmp-cpp-fortran REQUIRED
             NO_DEFAULT_PATH 
             PATHS ${base_install_dir}/lib/cmake/openmp-cpp-fortran)

add_executable(openmp-cpp-fortran-user openmp-cpp-fortran-user.F)
target_link_libraries(openmp-cpp-fortran-user PUBLIC openmp-cpp-fortran)

set_source_files_properties(
    openmp-cpp-fortran-user.F
    PROPERTIES
    Fortran_FORMAT FREE)

# Including BLTOptions should enable FORTRAN
# TODO(bowen) These two includes should be done automatically with 
# a macro that just include the whole cmake directory present in the install path?
include(${base_install_dir}/lib/cmake/BLTOptions.cmake)
include(${base_install_dir}/lib/cmake/SetupOpenMP.cmake)
get_target_property(imported_omp_flags blt::openmp INTERFACE_COMPILE_OPTIONS)

# The below print statement should emit the generator expression for the OMP flags,
# which is necessary because the flag is CPP and Fortran compiler dependent.
message(STATUS "${imported_omp_flags}")
