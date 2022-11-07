#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 14
#SBATCH --mem-per-cpu 3G
#SBATCH --time 0-12:00:00
#SBATCH --constraint=OS8

# Execute simulation
make sh-mac-mcsotdma-05-slotadv NUM_CPUS=14

# Exit job
exit
