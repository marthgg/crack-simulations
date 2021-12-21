import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile
from lammps_logfile import running_mean

files = ['log_1bar.lammps', 'log_3000bar.lammps', 'log_neg3000bar.lammps']

for file in files:
    log = lammps_logfile.File(file)

    temp = log.get('Temp', run_num=1)

    lx = log.get('Lx', run_num=1)
    ly = log.get('Ly', run_num=1)
    lz = log.get('Lz', run_num=1)

    lx = running_mean(lx, 70)
    ly = running_mean(ly, 70)
    lz = running_mean(lz, 70)

    if file == 'log_1bar.lammps':
        plt.figure(1)
        plt.plot(temp, lx, 'r', alpha=1.0)#, label = 'lx - 1 bar')
        plt.plot(temp, ly, 'g', alpha=1.0)#, label = 'ly - 1 bar')
        plt.plot(temp, lz, 'b', alpha=1.0)#, label = 'lz - 1 bar')

    if file == 'log_3000bar.lammps':
        plt.figure(1)
        plt.plot(temp, lx, 'r', alpha=0.5)#, label = 'lx - 3000 bar')
        plt.plot(temp, ly, 'g', alpha=0.5)#, label = 'ly - 3000 bar')
        plt.plot(temp, lz, 'b', alpha=0.5)#, label = 'lz - 3000 bar')

    if file == 'log_neg3000bar.lammps':
        plt.figure(1)
        plt.plot(temp, lx, 'r', alpha=0.8)#, label = 'lx - -3000 bar')
        plt.plot(temp, ly, 'g', alpha=0.8)#, label = 'ly - -3000 bar')
        plt.plot(temp, lz, 'b', alpha=0.8)#, label = 'lz - -3000 bar')

plt.xlabel('Temperature (K)')
plt.ylabel('Cell length (Å)')
plt.xlim([0.0, 600.0])
plt.ylim([29.0, 37.0])
plt.legend(['lx', 'ly', 'lz'])
#plt.legend(['lx 1 bar', 'ly 1 bar', 'lz 1 bar', 'lx 3000 bar', 'ly 3000 bar', 'lz 3000 bar', 'lx -3000 bar', 'ly -3000 bar', 'lz -3000 bar'])
plt.show()