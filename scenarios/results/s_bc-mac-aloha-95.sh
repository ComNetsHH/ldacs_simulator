#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 8
#SBATCH --mem-per-cpu 2G
#SBATCH --time 0-12:00:00
#SBATCH --constraint=OS8

# Execute simulation
make bc-mac-aloha-95 NUM_CPUS=8

# Exit job
exit
