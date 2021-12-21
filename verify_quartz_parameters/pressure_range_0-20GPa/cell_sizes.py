import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile
from lammps_logfile import running_mean

N = 1000

log = lammps_logfile.File('log.lammps')

lx = running_mean(log.get('Lx', run_num=1), N)
ly = running_mean(log.get('Ly', run_num=1), N)
lz = running_mean(log.get('Lz', run_num=1), N)

press = running_mean(log.get('Press', run_num=1), N)

lx_start = lx[~np.isnan(lx)]
lx_start = lx_start[0]
lz_start = lz[~np.isnan(lz)]
lz_start = lz_start[0]

press = press*0.0001

lx_diff = lx/lx_start
lz_diff = lz/lz_start

#print(np.arctan(-lxy/ly)*(180/np.pi))

# plt.figure(1)
# plt.plot(press, lx, label='lx')
# plt.plot(press, ly, label='ly')
# plt.plot(press, lz, label='lz')
# # plt.plot(lxy, label='lxy')
# # plt.plot(lxz, label='lxz')
# # plt.plot(lyz, label='lyz')
# plt.legend()

plt.figure(1)
plt.plot(press, lx_diff, label='lx/lx0')
plt.plot(press, lz_diff, label='lz/lz0')
plt.ylim([0.88, 1.02])
plt.xlim([0.0, 21.0])
plt.legend()
plt.show()