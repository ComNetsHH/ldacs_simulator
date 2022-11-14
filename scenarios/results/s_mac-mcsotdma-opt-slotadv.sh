#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 10
#SBATCH --mem-per-cpu 12G
#SBATCH --time 3-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
make sh-mac-mcsotdma-opt-slotadv NUM_CPUS=10

# Exit job
exit
