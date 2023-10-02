#include <iostream>

#include "../tmp_install_dir/include/cuda-clang-cpp.cuh"

int main() {
    std::cout << "Hello from downstream project.  Running cuda hello world: " << std::endl;
    run_kernel();

    return 0;
}
