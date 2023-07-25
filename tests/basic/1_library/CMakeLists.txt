# Copyright (c) 2017-2023, Lawrence Livermore National Security, LLC and
# other BLT Project Developers. See the top-level LICENSE file for details
# 
# SPDX-License-Identifier: (BSD-3-Clause)

cmake_minimum_required(VERSION 3.14)

project(world LANGUAGES CXX)

include(${BLT_SOURCE_DIR}/SetupBLT.cmake)

blt_add_library(NAME    world
                SOURCES hello_world.cpp
                HEADERS hello_world.hpp)

install(FILES hello_world.hpp DESTINATION include)

install(TARGETS     world
        EXPORT      world-targets
        DESTINATION lib)

install(EXPORT      world-targets 
        NAMESPACE   world::
        DESTINATION lib/cmake)
