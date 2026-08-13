#!/bin/bash


# copy this code to the test code folder and run by 
# qsub eureka_smit.sh


# ===== PBS settings =====
#PBS -N Segue1_grid_Stability_test
#PBS -M kiefer0655@gmail.com
#PBS -m abe
#PBS -q workq
#PBS -k n
#PBS -l walltime=720:00:00
#PBS -l nodes=2:ppn=16

N=128

# GAMER & Requirment link folder (put all link of required file under one folder)
LINK_DIR="/work1/kiefer0655/gamer/Segue1/ParticleEquilibriumIC/Run_Gamer_Link"

# Output directory for this run
OUTPUT_DIR="/work1/kiefer0655/gamer/Segue1/ParticleEquilibriumIC/Test_$N"

#Create and Test OUTPUT_DIR
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR" || exit 1


# ===== Go to the directory output DIR =====
cd "$OUTPUT_DIR"

# ===== Copy all the link =====
cp -a "$LINK_DIR"/. "$OUTPUT_DIR"/.

# ===== Create Required file with python =====
python3 Create_ExtPot.py -N $N  || exit 1
python3 get_Input_Parameter.py -N $N  || exit 1


# ===== Run GAMER =====
mpirun -map-by ppr:16:socket:pe=1 ./gamer 1>>stdout 2>&1


# log output and error with
# tail -f stdout