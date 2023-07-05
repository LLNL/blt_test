mkdir tmp_install_dir
cd base
mkdir build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=$(pwd)/../../tmp_install_dir
make
make install

# Build the downstream project
cd ../../downstream
mkdir build
cd build
cmake ../ -Dbase_install_dir=$(pwd)/../../tmp_install_dir
make