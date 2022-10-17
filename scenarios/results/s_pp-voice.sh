#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 20
#SBATCH --mem-per-cpu 5G
#SBATCH --time 5-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
make pp-voice NUM_CPUS=20

# Exit job
exit
