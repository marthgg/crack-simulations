#!/bin/bash
#SBATCH --job-name=noR_relaxation
#
#SBATCH --partition=normal
#
#SBATCH --ntasks=2
#
#SBATCH --cpus-per-task=2
#
#SBATCH --gres=gpu:2
#

#mpirun -np 2 lmp_kokkos_cuda_openmpi -pk kokkos newton on -k on g 2 -sf kk -in simulation.run -var dataFile alpha_quartz_structure.data -var temperature 300.000000 
mpirun -np 2 lmp -pk kokkos newton on -k on g 2 -sf kk -in relaxed.run -var dataFile alpha_quartz_structure.data -var temperature 300.000000
