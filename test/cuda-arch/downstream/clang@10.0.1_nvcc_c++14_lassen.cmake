# Copyright (c) 2017-2023, Lawrence Livermore National Security, LLC and
# other BLT Project Developers. See the top-level LICENSE file for details
# 
# SPDX-License-Identifier: (BSD-3-Clause)

#------------------------------------------------------------------------------
# Example host-config file for the blue_os cluster at LLNL, specifically Lassen
#------------------------------------------------------------------------------
#
# This file provides CMake with paths / details for:
#  C/C++:   Clang with GCC 8.3.1 toolchain
#  Cuda
#  MPI
# 
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Compilers
#------------------------------------------------------------------------------

set(BLT_CXX_STD "c++14" CACHE STRING "")
set(CLANG_CUDA_ARCH "sm_70")
set(CLANG_HOME "/usr/tce/packages/clang/clang-ibm-10.0.1-gcc-8.3.1")
set(CMAKE_C_COMPILER   "${CLANG_HOME}/bin/clang" CACHE PATH "")
set(CMAKE_CXX_COMPILER "${CLANG_HOME}/bin/clang++" CACHE PATH "")
set(ENABLE_CLANG_CUDA On CACHE BOOL "")

# Disable Fortran
set(ENABLE_FORTRAN OFF CACHE BOOL "")
# Disable MPI
set(ENABLE_MPI OFF CACHE BOOL "")
# CUDA
set(ENABLE_CUDA ON CACHE BOOL "")
