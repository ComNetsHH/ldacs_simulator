#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 14
#SBATCH --mem-per-cpu 8G
#SBATCH --time 2-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
make sh-mac-mcsotdma-opt NUM_CPUS=14

# Exit job
exit
