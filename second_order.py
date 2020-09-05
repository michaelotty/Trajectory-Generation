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

last_position_demand = 0.0
last_velocity_demand = 0.0

for i in range(len(t_range)):
    input_velocity_demand = (input_demand[i] - last_position_demand)/ts

    if i == 0:
        final_velocity = input_demand[i] - 0
    else:
        final_velocity = input_demand[i] - input_demand[i-1]

    if input_velocity_demand > vMax:
        input_velocity_demand = vMax
    elif input_velocity_demand < -vMax:
        input_velocity_demand = -vMax

    # v^2 = u^2 + 2as
    # u = +-sqrt(v^2 - 2as)

    sqrt2as = np.sqrt(0.9*np.abs(final_velocity**2 - (2*aMax*(input_demand[i] - last_position_demand))))
    if input_velocity_demand > sqrt2as:
        input_velocity_demand = np.sign(input_velocity_demand) * sqrt2as

    input_acceleration_demand = (input_velocity_demand - last_velocity_demand)/ts

    if input_acceleration_demand > aMax:
        a = aMax
    elif input_acceleration_demand < -aMax:
        a = -aMax


    v = v + a*ts

    s = s + v*ts + 0.5*a*ts**2
    last_position_demand = s
    last_velocity_demand = v

    output_demand = np.append(output_demand, s)

plt.figure(1)
ax1 = plt.subplot(311)
ax1.plot(t_range, input_demand, lw=0.75)
ax1.plot(t_range, output_demand, lw=0.75)

ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(t_range[1:], np.diff(output_demand)/ts, lw=0.75)
ax3 = plt.subplot(313, sharex=ax1)
ax3.plot(t_range[2:], np.diff(np.diff(output_demand)/ts)/ts, lw=0.75)

plt.figure(2)
plt.plot(t_range, input_demand-output_demand, lw=0.75)
plt.axis([t_range[0], t_range[-1], -1, 1])

plt.show()
