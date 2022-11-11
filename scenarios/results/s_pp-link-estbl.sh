#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 8
#SBATCH --mem-per-cpu 8G
#SBATCH --time 5-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
make pp-link-estbl NUM_CPUS=8

# Exit job
exit
