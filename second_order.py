"""Limit demand by second order constraints"""

import matplotlib.pyplot as plt
import numpy as np

ts = 1/500.0

aMax = 220
vMax = 80

t_range = np.arange(0, 20, ts)

input_demand = np.ones(len(t_range))*60#np.arctan2(2500-300*t_range, 1000)*180/np.pi
actual_velocity_demand = np.diff(input_demand)/ts
actual_acceleration_demand = np.diff(actual_velocity_demand)/ts
output_demand = np.array([])

s = 0
v = 0
a = 0

last_position_demand = 0.0
last_velocity_demand = 0.0
fiddle = 1
decceleration = False

for i in range(len(t_range)):
    input_velocity_demand = (input_demand[i] - last_position_demand)/ts
    input_velocity_demand += aMax*ts


    # s = ut + at^2/2
    # s = (u + at/2)t
    # t = s/(u + at/2)

    if i == 0:
        final_velocity = input_demand[i] - 0
    else:
        final_velocity = input_demand[i] - input_demand[i-1]

    if np.abs(input_velocity_demand) > vMax:
        input_velocity_demand = np.sign(input_velocity_demand) * vMax

    # v^2 = u^2 + 2as
    # u^2 = v^2 - 2as
    # u = +-sqrt(v^2 - 2as)

    if input_demand[i] - last_position_demand > 0.001:
        ta = np.floor((-(v-final_velocity)+np.sqrt(np.abs((v-final_velocity)**2 - 2*aMax*input_demand[i] - s)))/aMax/ts)*ts

        # sqrt2as = np.sqrt(np.abs(fiddle*2*aMax*(input_demand[i] - last_position_demand) - final_velocity**2))
        # if np.sqrt(np.abs(final_velocity**2 - fiddle*2*aMax*(input_demand[i] - last_position_demand))) < sqrt2as:
        #     sqrt2as = np.sqrt(np.abs(final_velocity**2 - fiddle*2*aMax*(input_demand[i] - last_position_demand)))

        # if np.abs(input_velocity_demand) >= sqrt2as:
        #     input_velocity_demand = np.sign(input_velocity_demand) * sqrt2as
        if i > 370:
            print('')
        if ta <= ts:
            decceleration = True

        if decceleration:
            a = -aMax
        else:
            input_acceleration_demand = (input_velocity_demand - last_velocity_demand)/ts
            if np.abs(input_acceleration_demand) > aMax:
                # a = (input_velocity_demand - last_velocity_demand)/ts
                a = np.sign(input_acceleration_demand) * aMax

        v += a*ts
        if np.abs(v) > vMax:
            v = np.sign(v) * vMax

        tv = (input_demand[i] - s) / v

        s += v*ts + 0.5*a*ts**2
    else:
        s = input_demand[i]
    last_position_demand = s
    last_velocity_demand = v

    output_demand = np.append(output_demand, s)

plt.figure(1)
ax1 = plt.subplot(311)
ax1.plot(t_range, input_demand, lw=0.75)
ax1.plot(t_range, output_demand, lw=0.75)
plt.title('Profiled demand')

ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(t_range[1:], np.diff(output_demand)/ts, lw=0.75)
ax3 = plt.subplot(313, sharex=ax1)
ax3.plot(t_range[2:], np.diff(np.diff(output_demand)/ts)/ts, lw=0.75)
ax3.axis([t_range[0], t_range[-1], -350, 350])

plt.figure(2)
plt.plot(t_range, input_demand-output_demand, lw=0.75)
plt.axis([t_range[0], t_range[-1], -1, 1])
plt.title('Error')

plt.figure(3)
ax4 = plt.subplot(311)
plt.title('Input Demand')
ax5 = plt.subplot(312, sharex=ax4)
ax6 = plt.subplot(313, sharex=ax4)

ax4.plot(t_range, input_demand, lw=0.75)

ax5.plot(t_range[1:], actual_velocity_demand, lw=0.75)
ax6.plot(t_range[2:], actual_acceleration_demand, lw=0.75)

plt.show()
