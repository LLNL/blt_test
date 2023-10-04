#include <iostream>

#include "../tmp_install_dir/include/hip.hpp"

int main() {
    std::cout << "Hello from downstream project.  Running hip hello world: " << std::endl;
    run_kernel();

    return 0;
}
