#/bin/bash

# TODO(jbowen) Delete
export $TMP=/Users/bowen36/homebrew/bin/brew

# This test will build camp without the CPP MPI compiler,
# install this build, then attempt to build Umpire with MPI
# using this install.
git clone git@github.com:LLNL/camp.git

git clone git@github.com:LLNL/Umpire.git

# Build camp without MPI.
cd camp
mkdir build
cd build
$TMP/cmake ../
make install

# Cleanup the two directories.
rm -rf camp

rm -rf Umpire