# SLURM Script Files
All `s_<something>.sh` files are SLURM script files, which allow the execution of our simulations on a SLURM-controlled server cluster. 
If you happen to have access to a SLURM system, feel free to modify and use these files.

# Simulation Time
Please be aware that conducting all simulations requires substantial simulation time.
We have run these simulations in a highly parallelized fashion on the High Performance Compute (HPC) Cluster of the Hamburg University of Technology.
The HPC has a large number of servers available, equipped with Intel Xeon E5-2680 CPUs of different versions, ranging from 2.4GHz to 3.3GHz.
When each target is run by 14 cores in parallel (where applicable), allow a simulation time of roughly ten hours per target.
Scale according to the hardware that you have available.