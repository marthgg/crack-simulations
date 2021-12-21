import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile
from lammps_logfile import running_mean

def save_figure(output_file_name):
    plt.savefig(output_file_name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait')

N = 10

log = lammps_logfile.File('log.lammps')

press = running_mean(log.get('Press', run_num=1), N)
press = press*0.0001 #GPa

lx = running_mean(log.get('Lx', run_num=1), N)
ly = running_mean(log.get('Ly', run_num=1), N)
lz = running_mean(log.get('Lz', run_num=1), N)

atoms = 2592
volume = lx*ly*lz
mass_O = 1728 * (2.656692e-26)
mass_Si = 864 * (4.6673066e-26)
mass_kg = mass_O + mass_Si

volume_m3 = volume*1e-30

density_kg_m3 = mass_kg/volume_m3

#print(density_kg_m3[1:15])

press_paper = [1e-4, 1.5, 4.4, 6.9, 10.2]
density_paper = [2648, 2742, 2897, 3004, 3120]

plt.figure(1)
plt.plot(press, density_kg_m3, 'r-')
#plt.plot(press_paper, density_paper, 'bo')
plt.xlim([0, 12])
plt.ylim([2500, 3400])
#plt.legend(['This study', 'Kimizuka et al. (2007)'])
plt.ylabel('Density (kg/m3)')
plt.xlabel('Pressure (GPa)')
#save_figure('/Users/marthgg/Dropbox/Project4-Fractures/figures/density_pressure.png')
plt.show()
