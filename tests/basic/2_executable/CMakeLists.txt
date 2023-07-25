# Copyright (c) 2017-2023, Lawrence Livermore National Security, LLC and
# other BLT Project Developers. See the top-level LICENSE file for details
# 
# SPDX-License-Identifier: (BSD-3-Clause)

cmake_minimum_required(VERSION 3.14)

project(hello_world LANGUAGES CXX)

include(${BLT_SOURCE_DIR}/SetupBLT.cmake)

blt_add_executable(NAME       hello_world
                   SOURCES    main.cpp
                   DEPENDS_ON world::world)

blt_add_test(NAME    hello_world
             COMMAND hello_world)

install(TARGETS hello_world
        RUNTIME DESTINATION bin)