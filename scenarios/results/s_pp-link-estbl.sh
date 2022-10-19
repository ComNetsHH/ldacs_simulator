#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 16
#SBATCH --mem-per-cpu 2G
#SBATCH --time 5-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
make pp-link-estbl-test NUM_CPUS=16

# Exit job
exit
