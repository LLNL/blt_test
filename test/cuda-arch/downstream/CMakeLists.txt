cmake_minimum_required(VERSION 3.14)

project(cuda-clang-cpp-user LANGUAGES CXX)

set(ENABLE_CLANG_CUDA On CACHE BOOL "")
set(CLANG_CUDA_ARCH "sm_70" CACHE STRING "")

set(CMAKE_CUDA_SEPARABLE_COMPILATION On CACHE BOOL "")

set(BLT_CXX_STD c++14 CACHE STRING "")
# Calling find_package sets up the TPL targets needed by the project
# in its argument.
find_package(cuda-clang-cpp REQUIRED
  NO_DEFAULT_PATH
  PATHS ${base_install_dir}/lib/cmake/cuda-clang-cpp
  ${base_install_dir})

# Load BLT
include(${BLT_SOURCE_DIR}/SetupBLT.cmake)

if (NOT TARGET cuda)
  message(FATAL_ERROR "Target cuda was not configured successfully during"
                      "downstream project configuration.")
endif()

get_target_property(cuda_compile_flags cuda INTERFACE_COMPILE_OPTIONS)
string(FIND "${cuda_compile_flags}" "-x" clang_cuda_flag)
string(FIND "${cuda_compile_flags}" "${CLANG_CUDA_ARCH}" clang_cuda_arch)
string(FIND "${cuda_compile_flags}" "/usr/tce/packages/cuda/cuda-11.1.0" expected_cuda_toolkit_dir)
if (clang_cuda_flag EQUAL -1 OR clang_cuda_arch EQUAL -1)
    message(FATAL_ERROR "Expected downstream project config flags to override upstream project's.")
endif()
if (expected_cuda_toolkit_dir EQUAL -1)
    message(FATAL_ERROR "Expected downstream project config flags to inherit upstream project's when to alternative is specified.")
endif()

blt_add_executable(
    NAME hello-cuda
    SOURCES cuda-clang-cpp-user.cpp
    DEPENDS_ON cuda-clang-cpp cuda
)
