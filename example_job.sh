#!/bin/bash

####################################
#     ARIS slurm script template   #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH --job-name=test_job    # Job name
#SBATCH --output=test_job.%j.out # Stdout (%j expands to jobId)
#SBATCH --error=test_job.%j.err # Stderr (%j expands to jobId)
#SBATCH --ntasks=1     # Number of tasks(processes)
#SBATCH --nodes=1     # Number of nodes requested
#SBATCH --ntasks-per-node=1     # Tasks per node
#SBATCH --cpus-per-task=1     # Threads per task
#SBATCH --time=0:01:00   # walltime
#SBATCH --mem=1G   # memory per NODE
#SBATCH --partition=gpu    # Partition
#SBATCH --account=pa181004    # Replace with your system project

export I_MPI_FABRICS=shm:dapl

if [ x$SLURM_CPUS_PER_TASK == x ]; then
  export OMP_NUM_THREADS=1
else
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
fi


## LOAD MODULES ##
module purge            # clean up loaded modules 

# load necessary modules
module use ${HOME}/modulefiles
module load gnu/6.4.0
module load intel/19.0.0
module load openblas/0.2.20
module load cuda/9.2.148
module load caffe2/201809
module load slp/0.1.0

## RUN YOUR PROGRAM ##
srun python test.py

