cmake_minimum_required(VERSION 3.14)

project(mpi-cpp-fortran-user LANGUAGES CXX Fortran)

message(STATUS ${base_install_dir})

find_package(mpi-cpp-fortran REQUIRED
             NO_DEFAULT_PATH
             PATHS ${base_install_dir}/lib/cmake/mpi-cpp-fortran)

add_executable(mpi-cpp-fortran-user mpi-cpp-fortran-user.F)
target_link_libraries(mpi-cpp-fortran-user PUBLIC mpi-cpp-fortran)

set_source_files_properties(
    mpi-cpp-fortran-user.F
    PROPERTIES
    Fortran_FORMAT FREE)

get_target_property(mpi_flags mpi INTERFACE_COMPILE_OPTIONS)

# The below print statement should emit the generator expression for the OMP flags,
# which is necessary because the flag is CPP and Fortran compiler dependent.
message(STATUS "${mpi_flags}")
