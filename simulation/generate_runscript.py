import shutil 
import os 
import numpy as np

templateStringHugefacet = """#!/bin/bash
#SBATCH --job-name=%f
#
#SBATCH --partition=normal
#
#SBATCH --ntasks=1
#
#SBATCH --cpus-per-task=2
#
#SBATCH --gres=gpu:1
#

mpirun -n 1 lmp -pk kokkos newton on -k on g 1 -sf kk -in %s -var dataFile %s -var temperature %f -var deform_z %f
"""

temperatures = [300]
deform_z = np.logspace(np.log10(1.03), np.log10(1.08), 15)

rootDir = "/home/users/marthgg/simulations/x2000/vary_deformZ/"
inputFile = "simulation.run"


def createSimulationFolders(deform_z, temperature, inputFile="simulation.run", dataFile="alpha_quartz_structure.data", rootDir=rootDir):
    directoryList = []
    for pressure in deform_z:
        pathFiles = (rootDir)
        os.chdir(pathFiles)

        for temperature in temperatures:

            executionString = templateStringHugefacet % (pressure, inputFile, dataFile, temperature, pressure)
            folderName = "crack_simulation_deformZ_%f" % (pressure)
            
            path = os.path.join(rootDir, folderName)
            os.makedirs(path)

            with open(os.path.join(path, "job.sh"), "w") as ofile:
                ofile.write(executionString)
            
            shutil.copy(inputFile, path)
            shutil.copy(dataFile, path)

            directoryList.append(path)
        
        os.chdir("../")

    return directoryList

folderNames = createSimulationFolders(deform_z, temperatures, inputFile=inputFile, rootDir=rootDir)

