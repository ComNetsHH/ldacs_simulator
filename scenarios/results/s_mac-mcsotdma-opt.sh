#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 14
#SBATCH --mem-per-cpu 2G
#SBATCH --time 0-12:00:00
#SBATCH --constraint=OS8

# Execute simulation
make sh-mac-mcsotdma-opt NUM_CPUS=14
make sh-mac-mcsotdma-all_plot

# Exit job
exit
