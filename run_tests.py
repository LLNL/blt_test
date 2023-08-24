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

from functools import partial

# Since we use subprocesses, flushing prints allows us to keep logs in
# order.
print = partial(print, flush=True)

def sexe(cmd, ret_output=False, echo=False):
    """ Helper for executing shell commands. """
    if echo:
        print("[exe: {0}]".format(cmd))
    if ret_output:
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        out = p.communicate()[0]
        out = out.decode('utf8')
        return p.returncode, out
    else:
        return subprocess.call(cmd, shell=True)

def cmake_build_project(path_to_test: string, is_base: bool):
    base_or_downstream = "base" if is_base else "downstream"
    install_flag = "-DCMAKE_INSTALL_PREFIX" if is_base else "-Dbase_install_dir"

    build_path = os.path.join(path_to_test, base_or_downstream, "build")
    install_path = os.path.join(path_to_test, "..", "tmp_install_dir")

    cmake_command = "cmake -B {0} -S {1} {2}={3}".format(
                            build_path, path_to_test, install_flag, install_path)
    build_command = "cmake --build {0}".format(build_path)
    install_command = "cmake --install {0}".format(build_path)
    # cmake, build and install the base project.
    code, err = sexe(cmake_command)
    if code:
        return code, err
    code, err = sexe(build_command)
    if code:
        return code, err
    if (is_base):
        code, err = sexe(install_command)
        if code:
            return code, err   

def run_test(path_to_test: string, path_to_yaml: string):
    """ Run test, using a yaml to specify CMake arguments """
    with open(path_to_yaml, 'r') as stream:
        test_yaml = yaml.safe_load(stream)
    # CMake, Build and install base
    cmake_build_project(path_to_test, True)
    # CMake, build downstream
    cmake_build_project(path_to_test, False)

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

    # Check for required args
    if not args["host-config"]:
        print("[ERROR: Required command line argument, 'host-config', was not provided.]")
        return None
    
    if not args["blt-source-dir"]:
        print("[ERROR: Required command line argument, 'blt-source-dir', was not provided.]")
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

def run_test(name, path):
    success = True
    print("[Running test '{0}' in '{1}']".format(name, path))
    #TODO: load commands to run tests from json file and run projects
    return success

def main():
    args = parse_args()
    if not args:
        return 1
    
    # Get directories inside the tests directory
    tests = []
    tests_dir = os.path.abspath("tests")
    print("[Searching for tests in '{0}']".format(tests_dir))
    for name in os.listdir(tests_dir):
        path = os.path.join(tests_dir, name)
        if not os.path.isdir(path):
            continue
        tests.append([name, path])
    
    # Run all tests and remember which failed
    failed_tests = []
    for test in tests:
        if not run_test(test[0], test[1]):
            failed_tests.append(test[0])

    # Print final status
    if len(failed_tests) == 0:
        print("[Success! All test passed!]")
    else:
        print("[ERROR: The following {0} out of {1} tests failed:".format(len(failed_tests), len(tests)))
        for name in failed_tests:
            print("    {0}".format(name))
        print("]")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
