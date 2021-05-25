#!/bin/bash
#SBATCH --job-name=noRot
#
#SBATCH --partition=normal
#
#SBATCH --ntasks=1
#
#SBATCH --cpus-per-task=2
#
#SBATCH --gres=gpu:1
#

mpirun -n 1 lmp -pk kokkos newton on -k on g 1 -sf kk -in relaxed.run -var dataFile alpha_quartz_structure.data -var temperature 300.000000
