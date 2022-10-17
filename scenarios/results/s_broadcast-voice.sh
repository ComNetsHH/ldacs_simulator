#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 20
#SBATCH --mem-per-cpu 4G
#SBATCH --time 0-06:00:00
#SBATCH --constraint=OS8

# Execute simulation
make broadcast-voice NUM_CPUS=20

# Exit job
exit
