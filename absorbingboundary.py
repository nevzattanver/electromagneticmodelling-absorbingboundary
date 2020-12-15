import numpy as np
from math import pi, exp
from matplotlib import pyplot as plt
ke = 1024
ex = np.zeros(ke)
hy = np.zeros(ke)
ddx = 0.01 # Cell size
dt = ddx / 6e8 # Time step size
boundary_low = [0, 0]
boundary_high = [0, 0]
# Create Dielectric Profile
epsz = 8.854e-12
epsilon1 = 4
sigma1 = 0.04
sigma2 = 0
ca1 = np.ones(ke)
cb1 = np.ones(ke) * 0.5
ca2 = np.ones(ke)
cb2 = np.ones(ke) * 0.5
cb_start = 250
eaf1 = dt * sigma1 / (2 * epsz * epsilon1)
ca1[cb_start:309] = (1 - eaf1) / (1 + eaf1)
cb1[cb_start:309] = 0.5 / (epsilon1 * (1 + eaf1))
cb2[500:559] = 0.5 / (epsilon1)
nsteps = 5000
# Pulse constants
spread = 12
t0 = 40
# Create drawing area
fig = plt.figure(figsize=(15, 2.25))
# Main FDTD Loop
for time_step in range(1, nsteps + 1):
 # Put a pulse at the low end
 pulse = exp(-0.5 * ((t0 - time_step) / spread) ** 2)
 ex[5] = pulse + ex[5]
11
 # Calculate the Ex field
 for k in range(1, 309):
 ex[k] = ex[k] * ca1[k] + cb1[k] * (hy[k - 1] - hy[k])
 for k in range(309, ke):
 ex[k] = ex[k] + cb2[k] * (hy[k - 1] - hy[k])
 # Absorbing Boundary Conditions
 ex[0] = boundary_low.pop(0)
 boundary_low.append(ex[1])
 ex[ke - 1] = boundary_high.pop(0)
 boundary_high.append(ex[ke - 2])
 # Calculate the Hy field
 for k in range(ke - 1):
 hy[k] = hy[k] + 0.5 * (ex[k] - ex[k + 1])
 # Draw Graph
 if time_step % 10 == 0:
 plt.clf()
 plt.rcParams['font.size'] = 12
 # plt.figure(figsize=(15, 2.25))
 plt.plot(ex, color='r', linewidth=1)
 plt.ylabel('E$_x$', fontsize='14')
 plt.xticks(np.arange(0, 1024, step=100))
 plt.xlim(0, 1024)
 plt.yticks(np.arange(-1, 1.2, step=1))
 plt.ylim(-1.2, 1.2)
 plt.text(50, 0.5, 'T = {}'.format(time_step),
 horizontalalignment='center')
 plt.plot((0.5 / cb1 - 1) / 3, 'k--',
 linewidth=0.75) # The math on cb is just for scaling
 plt.plot((0.5 / cb2 - 1) / 3, 'k--',
 linewidth=0.75) # The math on cb is just for scaling
 plt.text(275, 0.7, 'εr = {}'.format(epsilon1),
 horizontalalignment='center')
 plt.text(275, 0.5, 'μ0 ',
 horizontalalignment='center')
 plt.text(280, 0.3, 'σ = {}'.format(sigma1),
 horizontalalignment='center')
 plt.text(530, 0.7, 'εr = {}'.format(epsilon1),
 horizontalalignment='center')
 plt.text(530, 0.5, 'μ0 ',
 horizontalalignment='center')
 plt.xlabel('FDTD cells')
 fig.canvas.draw()
 plt.pause(1e-5)