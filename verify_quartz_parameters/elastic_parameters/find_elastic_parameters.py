import lammps_logfile
import matplotlib.pyplot as plt
import numpy as np

# X shear
log = lammps_logfile.File('log_deformX.lammps')

time = log.get('Time'); lx = log.get('Lx')

lx_start = np.mean(lx[200:400]); lx_end = lx[1000:]

strain_xx = (lx_end - lx_start)/lx_start; stress_xx = log.get('Pxx')

[c_11, b_11] = -np.polyfit(strain_xx, stress_xx[1000:], 1)

plt.figure(1)
plt.plot(strain_xx, stress_xx[1000:], c='darkblue')
plt.plot(strain_xx, -c_11*strain_xx + b_11, c='red', linewidth=2, label = 'C_11 = %f GPa' %(c_11/10**4))
plt.legend()

# Y shear
log = lammps_logfile.File('log_deformY.lammps')

time = log.get('Time'); ly = log.get('Ly')

ly_start = np.mean(ly[200:400]); ly_end = ly[1000:]

strain_yy = (ly_end - ly_start)/ly_start
stress_xx = log.get('Pxx'); stress_yy = log.get('Pyy')

[c_12, b_12] = -np.polyfit(strain_yy, stress_xx[1000:], 1)
[c_22, b_22] = -np.polyfit(strain_yy, stress_yy[1000:], 1)

plt.figure(2)
plt.plot(strain_yy, stress_xx[1000:], c='darkblue')
plt.plot(strain_yy, stress_yy[1000:], c='darkblue')
plt.plot(strain_yy, -c_12*strain_yy + b_12, c='lightblue', linewidth=2, label = 'C_12 = %f GPa' %(c_12/10**4))
plt.plot(strain_yy, -c_22*strain_yy + b_22, c='red', linewidth=2, label = 'C_22 = %f GPa' %(c_22/10**4))
plt.legend()

# Z shear
log = lammps_logfile.File('log_deformZ.lammps')

time = log.get('Time'); lz = log.get('Lz')

lz_start = np.mean(lz[200:400]); lz_end = lz[1000:]

strain_zz = (lz_end - lz_start)/lz_start
stress_xx = log.get('Pxx'); stress_zz = log.get('Pzz'); stress_yy = log.get('Pyy')

[c_13, b_13] = -np.polyfit(strain_zz, stress_xx[1000:], 1)
[c_33, b_33] = -np.polyfit(strain_zz, stress_zz[1000:], 1)
[c_23, b_23] = -np.polyfit(strain_zz, stress_yy[1000:], 1)

plt.figure(3)
plt.plot(strain_zz, stress_xx[1000:], c='darkblue')
plt.plot(strain_zz, stress_zz[1000:], c='darkblue')

plt.plot(strain_zz, -c_13*strain_zz + b_13, c='lightblue', linewidth=2, label = 'C_13 = %f GPa' %(c_13/10**4))
plt.plot(strain_zz, -c_23*strain_zz + b_33, c='red',       linewidth=2, label = 'C_23 = %f GPa' %(c_23/10**4))
plt.plot(strain_zz, -c_33*strain_zz + b_23, c='yellow',    linewidth=2, label = 'C_33 = %f GPa' %(c_33/10**4))

plt.xlabel('strain')
plt.ylabel('stress')
plt.legend()

# YZ shear
log = lammps_logfile.File('log_deformYZ.lammps')

time = log.get('Time'); lyz = log.get('Yz'); lz = log.get('Lz')
pyz = log.get('Pyz'); pxx = log.get('Pxx')

strain_yz = lyz[1000:]/lz[1000:]

[c_14, b_14] = -np.polyfit(strain_yz, pxx[1000:], 1)
[c_44, b_44] = -np.polyfit(strain_yz, pyz[1000:], 1)

plt.figure(4)
plt.plot(strain_yz, pyz[1000:], c='darkblue')
plt.plot(strain_yz, pxx[1000:], c='darkblue')

plt.plot(strain_yz, -c_14*strain_yz - b_14, c='lightblue', label = 'C_14 = %f GPa' %(c_14/10**4))
plt.plot(strain_yz, -c_44*strain_yz - b_44, c='red', label = 'C_44 = %f GPa' %(c_44/10**4))

plt.xlabel('strain')
plt.ylabel('stress')
plt.legend()

# XZ shear
log = lammps_logfile.File('log_deformXZ.lammps')

time = log.get('Time')
lxz = log.get('Xz')
lz = log.get('Lz')
pxz = log.get('Pxz')

strain_xz = lxz[1000:]/lz[1000:]

[c_55, b_55] = -np.polyfit(strain_xz, pxz[1000:], 1)

plt.figure(5)
plt.plot(strain_xz, pxz[1000:], c='darkblue')
plt.plot(strain_xz, -c_55*strain_xz - b_55, c='red', label = 'C_55 = %f GPa' %(c_55/10**4))

plt.xlabel('strain')
plt.ylabel('stress')
plt.legend()

# XY shear
log = lammps_logfile.File('log_deformXY.lammps')

time = log.get('Time')
lxy = log.get('Xy')
ly = log.get('Ly')
pxx = log.get('Pxx')
pxy = log.get('Pxy')

strain_xy = lxy[1000:]/ly[1000:]

[c_16, b_16] = -np.polyfit(strain_xy, pxx[1000:], 1)
[c_66, b_66] = -np.polyfit(strain_xy, pxy[1000:], 1)

plt.figure(6)
plt.plot(strain_xy, pxx[1000:], c='darkblue')
plt.plot(strain_xy, pxy[1000:], c='darkblue')
plt.plot(strain_xy, -c_16*strain_xy - b_16, c='lightblue', label = 'C_16 = %f GPa' %(c_16/10**4))
plt.plot(strain_xy, -c_66*strain_xy - b_66, c='red', label = 'C_66 = %f GPa' %(c_66/10**4))

plt.xlabel('strain')
plt.ylabel('stress')
plt.legend()

plt.show()

print('C_11 = %f GPa' %(c_11/10**4))
print('C_12 = %f GPa' %(c_12/10**4))
print('C_13 = %f GPa' %(c_13/10**4))
print('C_14 = %f GPa' %(c_14/10**4))
print('C_16 = %f GPa' %(c_16/10**4))
print('C_22 = %f GPa' %(c_22/10**4))
print('C_23 = %f GPa' %(c_23/10**4))
print('C_33 = %f GPa' %(c_33/10**4))
print('C_44 = %f GPa' %(c_44/10**4))
print('C_55 = %f GPa' %(c_55/10**4))
print('C_66 = %f GPa' %(c_66/10**4))