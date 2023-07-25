#include <mpi.h>
#include <stdio.h>

#include "../tmp_install_dir/include/openmp-mpi-cpp.hpp"

int main() {
    MPI_Init(nullptr, nullptr);

    int world_size = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len = 0;
    MPI_Get_processor_name(processor_name, &name_len);

    // Print off a hello world message
    printf("Hello world from processor %s, rank %d out of %d processors\n",
           processor_name, world_rank, world_size);

    test_func();

    // Finalize the MPI environment.
    MPI_Finalize();

    return 0;
}