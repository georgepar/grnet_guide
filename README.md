# grnet_guide

## Step 1: RTFM

Read the infrastructure documentation [here](http://doc.aris.grnet.gr/)

Don't even continue reading (or even worse try to use the cluster) if you don't finish this document.


## Step 2: Copy your data

We all share a common $USER in the cluster, so we need to be careful to keep the filesystem
organized.

1. Create a source dir in /users/pa18/geopar/${YOUR_NAME}. This is your home. Here you put code etc.  
2. Create a source dir in /work2/pa18/geopar/${YOUR_NAME}. This is where your data are kept.
3. scp or rsync your data in /work2/pa18/geopar/${YOUR_NAME}.

As you read in the docs you are not supposed to run your jobs (data) from /users. All data should be in work2. If you did not read this RTFM before continuing.

## Step 2: Creating a batch job

Now that you RTFM you know ARIS is a batch system and you need to submit batch jobs to it.

An example batch script is contained in `example_job.sh`.

Let's say we need to run `test.py`. First we need to configure the batch job

```bash
#SBATCH --job-name=test_job    # DO NOT FORGET TO CHANGE THIS
#SBATCH --output=test_job.%j.out # DO NOT FORGET TO CHANGE THIS. the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --error=test_job.%j.err # DO NOT FORGET TO CHANGE THIS. the job stdout will be dumped here. (%j expands to jobId).
#SBATCH --ntasks=1     # How many times the command will run. Leave this to 1 unless you know what you are doing
#SBATCH --nodes=1     # The task will break in so many nodes. Use this if you need many GPUs
#SBATCH --gres=gpu:1 # GPUs per node to be allocated
#SBATCH --ntasks-per-node=1     # Same as ntasks
#SBATCH --cpus-per-task=1     # If you need multithreading
#SBATCH --time=0:01:00   # HH:MM:SS Estimated time the job will take. It will be killed if it exceeds the time limit
#SBATCH --mem=1G   # memory to be allocated per NODE
#SBATCH --partition=gpu    # gpu: Job will run on one or more of the nodes in gpu partition. ml: job will run on the ml node
#SBATCH --account=pa181004    # DO NOT CHANGE THIS
```

After this the script loads the required modules. Modules are a way to dynamically configure your dependencies.

caffe2/201809 is for pytorch. There are also some tensorflow modules. You can see all available modules if you run module avail.

There is also the slp/0.1.0 module which loads some useful tools that did not exist in the system like nltk, gensim, librosa and ekphrasis, courtesy of @geopar.

You normally won't need to change this section except if you want tensorflow.

```bash
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
```

Now you specify the script you want to run

```bash
## RUN YOUR PROGRAM ##
srun python test.py
```

This is saved in a `job.sh` script and you can submit it to the queue with

```bash
sbatch job.sh
```

## Hacking the system

As you probably will know because you definitely read the documentation...
Ok seriously go read it.

As you know SLURM is a batch system and there is a job queue. This means that you may wait for other jobs to complete before enough resources become available.

Here are some tips and tricks to jump the queue

1. Don't spam jobs. This is not a development environment, it's a production one. Make sure your code runs correctly before submitting. There is some fair sharing built into the queue so if you spam, other users will jump before you.  
2. Do not oversize your jobs. Just because you **can** request 256GB of RAM and 10 GPUs it doesn't mean you **should**. Have a basic knowledge of your actual HW  requirements.  
3. Do not overestimate the time your job will need to complete. You should know how long it should take approximately. If it takes 3 hours, request 4-5 to be safe, not a week.

## Access

1. You need to connect to the NTUA VPN to access the infrastructure. Here's a
[guide](http://www.noc.ntua.gr/el/help-page/vpn/linux) on how to connect  
2. Send your ssh key to @geopar and he will grant you access. If you have read the docs. There will be an exam.


## How to install a dependency

1. Send a mail to support  
2. If this fails, notify geopar  
3. DIY  
```bash
git clone http://github.com/<vendor>/my_repo
cd my_repo
module purge # clean up loaded modules 
# load necessary modules
module use ${HOME}/modulefiles
module load gnu/6.4.0
module load intel/19.0.0
module load openblas/0.2.20
module load cuda/9.2.148 
module load caffe2/201809
module load slp/0.1.0
pip install . --prefix /users/pa18/geopar/packages/python/

```
