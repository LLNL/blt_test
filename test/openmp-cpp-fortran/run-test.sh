#!/bin/bash
##############################################################################
# Copyright (c) 2017-2023, Lawrence Livermore National Security, LLC and
# other BLT Project Developers. See the top-level LICENSE file for details
# 
# SPDX-License-Identifier: (BSD-3-Clause)
##############################################################################

function cleanup() {
    rm -rf base/build
    rm -rf downstream/build
    rm -rf tmp_install_dir
}

function or_die () {
    "$@"
    local status=$?
    if [[ $status != 0 ]] ; then
        echo ERROR $status command: $@
        cleanup
        exit $status
    fi
}

# Cleanup any existing builds or installs before running the test
cleanup

# Create the build and install directories
or_die mkdir tmp_install_dir
or_die cd base
or_die mkdir build
or_die cd build
# Build and install the base project
echo "====== CMAKE BASE PROJECT ======"
or_die cmake ../ -DCMAKE_INSTALL_PREFIX=$(pwd)/../../tmp_install_dir
echo "====== BUILDING BASE PROJECT ======"
or_die make
or_die make install

or_die cd ../../downstream
or_die mkdir build
or_die cd build
# Build and install the base project
echo "====== CMAKE DOWNSTREAM PROJECT ======"
or_die cmake ../ -Dbase_install_dir=$(pwd)/../../tmp_install_dir
echo "====== BUILDING DOWNSTREAM PROJECT ======"
or_die make

cleanup
