cmake_minimum_required(VERSION 3.14)

project(mpi-cpp-fortran-user LANGUAGES CXX Fortran)

# Print the install directory of the base project for debugging purposes.
message(STATUS ${base_install_dir})

# This call creates targets with relevant compile flags (i.e. for Fortran and
# cpp) for MPI.
find_package(mpi-cpp-fortran REQUIRED
             NO_DEFAULT_PATH
             PATHS ${base_install_dir}/lib/cmake/mpi-cpp-fortran)

add_executable(mpi-cpp-fortran-user mpi-cpp-fortran-user.F)
target_link_libraries(mpi-cpp-fortran-user PUBLIC mpi-cpp-fortran)

set_source_files_properties(
    mpi-cpp-fortran-user.F
    PROPERTIES
    Fortran_FORMAT FREE)
