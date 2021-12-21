import numpy as np

# Loading along z-axis

c_11 = 7.004353  #10^5 bar
c_13 = 2.410310
c_33 = 8.105284
c_55 = 3.192519

c_55_pa = c_55*1e10 #Pa

'''

# Loading along y-axis
c_11 = 6.986194 #c_22
c_33 = 8.105284
c_13 = 2.408433 #c_23
c_55 = 3.200060 #c_44

c_55_pa = c_55*1e10 #Pa
'''

density = 2561 #kg/m**3

# Calculate Rayleigh wave speed
alpha = c_33/c_11
gamma = c_55/c_11
delta = 1 - ((c_13**2)/(c_11*c_33))
sigma = 1/gamma

a0 = (alpha * sigma**2 * delta**2) / (gamma - alpha)
a1 = (alpha * sigma * delta*(sigma * delta + 2)) / (alpha - gamma)
a2 = (alpha - 1 + 2 * alpha * sigma * delta) / (gamma - alpha)


R = (9 * a1 * a2 - 27 * a0 - 2*a2**3) / 54
D = (4 * a0 * a2**3 - a1**2 * a2**2 - 18 * a0 * a1 * a2 + 27 * a0**2 + 4 * a1**3)/108
d = a2**2 - 3*a1

exp1 = (alpha - 1 + 2 * alpha * sigma * delta) / (3 * (alpha - gamma))
exp2 = np.sign(-d) * (np.sign(-d) * (R + np.sqrt(D, dtype=complex)))**(1/3)
exp3 = (-R + np.sqrt(D, dtype=complex))**(1/3)

exp4 = exp1 + exp2 - exp3

c_R = np.sqrt(exp4 * (c_55_pa/density), dtype=complex)

print(c_R)