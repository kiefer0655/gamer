#!/bin/bash


# copy this code to the test code folder and run by 
# qsub eureka_smit.sh


# ===== PBS settings =====
#PBS -N YOUR_JOB_NAME
#PBS -M Kiefer0655@gmail.com
#PBS -m abe
#PBS -q workq
#PBS -k n
#PBS -l walltime=1:00:00
#PBS -l nodes=1:ppn=16

# ===== Go to the directory where I submitted the job =====
cd $PBS_O_WORKDIR

# ===== Run GAMER =====
mpirun -map-by ppr:16:socket:pe=1 ./YOUR_EXECUTABLE 1>>stdout 2>>stderr


# log output and error with
# tail -f stdout
# tail -f stderr
