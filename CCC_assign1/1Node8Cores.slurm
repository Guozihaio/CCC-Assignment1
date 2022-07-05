#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=00:20:00
module load foss/2019b
module load python/3.7.4
module load mpi4py/3.0.2-timed-pingpong
srun -n 8 python3 newmain.py sydGrid.json bigTwitter.json 15360
##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s
