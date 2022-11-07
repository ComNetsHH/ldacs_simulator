#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu 2G
#SBATCH --time 5-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
make sh-mac-aloha NUM_CPUS=6

# Exit job
exit
