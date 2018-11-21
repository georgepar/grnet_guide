import os
import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


##########################################################
# Read arguments
##########################################################
job_name = sys.argv[1]
command = ' '.join(sys.argv[2:])

header = """#!/bin/bash

####################################
#     ARIS slurm script template   #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH --job-name={0}    # DO NOT FORGET TO CHANGE THIS
#SBATCH --output={1}.%j.out # DO NOT FORGET TO CHANGE THIS. the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --error={2}.%j.err # DO NOT FORGET TO CHANGE THIS. the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --ntasks=1     # How many times the command will run. Leave this to 1 unless you know what you are doing
#SBATCH --nodes=1     # The task will break in so many nodes. Use this if you need many GPUs
#SBATCH --gres=gpu:1 # GPUs per node to be allocated
#SBATCH --ntasks-per-node=1     # Same as ntasks
#SBATCH --cpus-per-task=1     # If you need multithreading
#SBATCH --time=32:00:00   # HH:MM:SS Estimated time the job will take. It will be killed if it exceeds the time limit
#SBATCH --mem=32G   # memory to be allocated per NODE
#SBATCH --partition=gpu    # gpu: Job will run on one or more of the nodes in gpu partition. ml: job will run on the ml node
#SBATCH --account=pa181004    # DO NOT CHANGE THIS
""".format(job_name, job_name, job_name)

body = """

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

"""

footer = """

## RUN YOUR PROGRAM ##
srun python {0}

""".format(command)

runner = header + body + footer

write_approval = query_yes_no("IS THE GENERATED SCRIPT OK? \n\n" + "=" * 50 +
                              "\n\n\n {0}".format(runner), default="no")

if write_approval:
    with open("{0}.sh".format(job_name), "w") as f:
        f.write(header + body + footer)

    ex_approval = query_yes_no("Execute the job '{0}' ?".format(job_name),
                               default="no")

    if ex_approval:
        os.system("sbatch {0}.sh".format(job_name))

else:
    print("Exiting...")
