#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu 2G
#SBATCH --time 0-12:00:00
#SBATCH --constraint=OS8

# Execute simulation
make sh-mac-mcsotdma-95 NUM_CPUS=6

# Exit job
exit
