#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 14
#SBATCH --mem-per-cpu 2G
#SBATCH --time 5-00:00:00
#SBATCH --constraint=OS8

# Execute simulation
<<<<<<< HEAD
make pp-link-estbl-test NUM_CPUS=14
=======
make pp-link-estbl NUM_CPUS=16
>>>>>>> 9ea4578dae665e606e7158c0ef069f99e7b86916

# Exit job
exit
