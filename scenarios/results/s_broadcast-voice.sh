#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 16
#SBATCH --mem-per-cpu 2G
#SBATCH --time 0-06:00:00
#SBATCH --constraint=OS8

# Execute simulation
make broadcast-voice NUM_CPUS=16

# Exit job
exit
