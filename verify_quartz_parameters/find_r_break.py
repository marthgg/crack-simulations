import numpy as np
import matplotlib.pyplot as plt 

H = 30.923
eta = 9
ZO = -0.3936
ZSi = 0.7872
lambda1 = 4.43 
D = 10.701 
labmda4 = 2.5
r_c = 5.5 
W = 0

def V2(r): 
    U = H/(r**eta) + ZO*ZSi/r * np.exp(-r/lambda1) - D/r**4*np.exp(-r/labmda4)
    return U

x = np.linspace(1.0, 7.0, 1000)
y = V2(x) 

v = y 
dv = np.diff(y)/np.diff(x)
vmax = x[np.argmin(v)]
dvmax = x[np.argmax(dv)]

diff = np.diff(y)/np.diff(x)

print(f"r_break = {dvmax/vmax}")

plt.plot(x, y)
plt.plot(x[:-1], np.diff(y)/np.diff(x))
plt.xlim([1, 3])
plt.ylim([-1, 1])
plt.hlines(0, x[0], x[-1], color='black')
plt.axvline(vmax, color='black', linestyle='dotted', label='r_equilibrium')
plt.axvline(dvmax, color='black', linestyle='dashed', label='r_critical')
plt.xlabel('Interatomic distance (Angstrom)')
plt.ylabel('Potential energy (eV)')
plt.legend()
plt.show()