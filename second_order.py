"""Limit demand by second order constraints"""

import matplotlib.pyplot as plt
import numpy as np

ts = 1/500.0

aMax = 220
vMax = 80

t_range = np.arange(0, 20, ts)

input_demand = np.arctan2(2500-300*t_range, 1000)*180/np.pi
output_demand = np.array([])

s = 0
v = 0
a = 0

for i in range(len(t_range)):
    if input_demand[i] > s:  # Going positive
        if np.abs(input_demand[i]-s) <= (v**2/(2*aMax)):
            a = -aMax
        else:
            a = aMax
    elif input_demand[i] < s:
        if np.abs(input_demand[i]-s) <= (v**2/(2*aMax)):
            a = aMax
        else:
            a = -aMax
    else:
        a = 0

    v = v + a*ts
    if v > vMax:
        v = vMax
    elif v < -vMax:
        v = -vMax

    s = s + v*ts + 0.5*a*ts**2
    output_demand = np.append(output_demand, s)

plt.figure(1)
plt.subplot(311)
plt.plot(t_range, input_demand, lw=0.75)
plt.plot(t_range, output_demand, lw=0.75)

plt.subplot(312)
plt.plot(t_range[1:], np.diff(output_demand)/ts, lw=0.75)
plt.subplot(313)
plt.plot(t_range[2:], np.diff(np.diff(output_demand)/ts)/ts, lw=0.75)

plt.figure(2)
plt.plot(t_range[1:], input_demand[1:]-output_demand[:-1], lw=0.75)
plt.axis([t_range[0], t_range[-1], -1, 1])

plt.show()
