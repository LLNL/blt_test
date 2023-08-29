#!/bin/sh
"exec" "python3" "-u" "-B" "$0" "$@"
# Copyright (c) 2017-2023, Lawrence Livermore National Security, LLC and
# other BLT Project Developers. See the top-level LICENSE file for details
# 
# SPDX-License-Identifier: (BSD-3-Clause)

import os
import sys
import subprocess
import glob
import re
import argparse
import string

from functools import partial

# Since we use subprocesses, flushing prints allows us to keep logs in
# order.
print = partial(print, flush=True)

def sexe(cmd):
    """ Helper for executing shell commands. """
    p = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    out = p.communicate()[0]
    out = out.decode('utf8')
    return p.returncode, out

def cmake_build_project(path_to_test: string, path_to_blt: string, host_config: string, is_base: bool):
    base_or_downstream = "base" if is_base else "downstream"
    install_flag = "-DCMAKE_INSTALL_PREFIX" if is_base else "-Dbase_install_dir"
    blt_path_flag = "-DPATH_TO_BLT"

    # Convert these paths to absolute paths to avoid CMake seeing an incorrect relative path.
    source_path = os.path.abspath(os.path.join(path_to_test, base_or_downstream))
    build_path = os.path.abspath(os.path.join(source_path, "build"))
    install_path = os.path.abspath(os.path.join(path_to_test, "tmp_install_dir"))

    # Projects in this directory follow a base/downstream format, where base files 
    # are built and installed, and downstream projects are fed their install path.
    # If a base project is being built, feed CMake the path to install the built
    # project.
    # If a downstream project is being built, feed CMake the base install path.  
    cmake_command = "cmake -B {0} -S {1} {2}={3} {4}={5}".format(
                            build_path, source_path, install_flag, install_path, blt_path_flag, path_to_blt)
    if len(host_config) > 0:
        cmake_command += " -C {0}".format(host_config)
        
    build_command = "cmake --build {0}".format(build_path)
    install_command = "cmake --install {0}".format(build_path)
    # cmake, build and install the base project.
    code, err = sexe(cmake_command)
    if code:
        return code, err
    code, err = sexe(build_command)
    if code:
        return code, err
    if is_base:
        code, err = sexe(install_command)
        if code:
            return code, err

    return 0, "Success"

# Helper to cleanup any build directories, installation directories, or any temporary caches that could 
# create a state between runs of the tests in the repository.
def remove_directory(path: string):
    for p in os.listdir(path):
        abs_path = os.path.abspath(os.path.join(path, p))
        if os.path.isdir(abs_path):
            remove_directory(abs_path)
        else:
            os.remove(abs_path)
    if os.path.isdir(path):
        os.rmdir(path)

def run_test(path_to_test: string, path_to_blt: string, host_config: string):
    """ Run test, using a yaml to specify CMake arguments """
    # CMake, Build and install base
    code, err = cmake_build_project(path_to_test, path_to_blt, host_config, True)
    if code:
        return code, err
    # CMake, build downstream
    code, err = cmake_build_project(path_to_test, path_to_blt, host_config, False)
    if code:
        return code, err

    # Cleanup build and install directories
    remove_directory(os.path.join(path_to_test, "base", "build"))
    remove_directory(os.path.join(path_to_test, "downstream", "build"))
    remove_directory(os.path.join(path_to_test, "tmp_install_dir"))
    
    return 0, "Test {0} passed".format(path_to_test)

def parse_args():
    "Parses args from command line"
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-config",
                      dest="host-config",
                      default=None,
                      help="Host config file to be used by all test projects.")

    # where to install
    parser.add_argument("--blt-source-dir",
                      dest="blt-source-dir",
                      default=None,
                      help="Path to BLT source to be used by all test projects.")

    args, extra_args = parser.parse_known_args()
    args = vars(args)
    
    if not args["blt-source-dir"]:
        print("[ERROR: Required command line argument, 'blt-source-dir', was not provided.]")
        return None

    if len(args["host-config"]) > 0 and not os.path.exists(args["host-config"]):
        print("ERROR: Host config file {0} specified, but file does not exist.".format(args["host-config"]))
        return None

    # Pretty print given args
    print("========================================")
    print("Command line arguments:")
    for key in args.keys():
        print("[{0}]: {1}".format(key, args[key]))
    print("========================================")

    return args

def should_test_run(name, path, hostconfig):
    run_test = True
    #TODO: read regexs (?) from yaml file that show whether we should run the test
    # and run them over the given host-config.
    # for example, ENABLE_CUDA being ON, if none are present just run test always
    return run_test

def main():
    args = parse_args()
    if not args:
        return 1
    
    # Iterate through the tests, run them, and report error if encountered. 
    tests = []
    path_to_blt = args["blt-source-dir"]
    host_config = args["host-config"]
    failed_tests = []
    tests_dir = os.path.relpath("test")
    print("[Searching for tests in '{0}']".format(tests_dir))
    for test_dir in os.listdir(tests_dir):
        path_to_test_dir = os.path.join(tests_dir, test_dir)
        if not os.path.isdir(path_to_test_dir):
            print(path_to_test_dir)
            continue
        tests.append(test_dir)
        status, err = run_test(path_to_test_dir, path_to_blt, host_config)
        print(status, err)
        if status:
            print("Test {0} failed with error {1}".format(test_dir, err))
            failed_tests.append(test_dir)

    # Print final status
    if len(failed_tests) == 0:
        print("[Success! All tests passed!]")
    else:
        print("[ERROR: The following {0} out of {1} tests failed:".format(len(failed_tests), len(tests)))
        for name in failed_tests:
            print("    {0}".format(name))
        print("]")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
