"""Limit demand by second order constraints (acceleration and velocity maximum)"""

import matplotlib.pyplot as plt
import numpy as np

def symetrical_limit(value, limit, midpoint):
    offset_value = value - midpoint
    limit = abs(limit)
    if offset_value > limit:
        offset_value = limit
    
    if offset_value < -limit:
        offset_value = -limit

    return offset_value + midpoint

ts = 1/500.0

aMax = 220
vMax = 80

t_range = np.arange(0, 20, ts)


input_position_demand = np.arctan2(3000-300*t_range, 1000)*180/np.pi

# for i in range(len(t_range) - 500):
#     input_position_demand[i+500] = 60

# for i in range(len(t_range) - 1000):
#     input_position_demand[i+1000] = -10

input_velocity_demand = np.zeros_like(input_position_demand)
input_acceleration_demand = np.zeros_like(input_position_demand)
output_demand = np.zeros_like(input_position_demand)

state = {'STOPPED': 0, 'TRACKING': 2, 'SLEWING': 1}
current_state = state['STOPPED']
state_array = np.zeros_like(input_position_demand)

# Initialise variables
s = 0
v = 0
a = 0
last_position_demand = 0.0
last_velocity_demand = 0.0
last_output_position_demand = 0.0
last_output_velocity_demand = 0.0
fiddle = 1

for i in range(len(t_range)):
    input_velocity_demand[i] = (input_position_demand[i] - last_position_demand)/ts
    input_acceleration_demand[i] = (input_velocity_demand[i] - last_velocity_demand)/ts

    last_position_demand = input_position_demand[i]
    last_velocity_demand = input_velocity_demand[i]

    if abs(input_velocity_demand[i]) > vMax or abs(input_acceleration_demand[i]) > aMax:
        current_state = state['SLEWING']

    if current_state is state['SLEWING']:
        s = input_position_demand[i] - last_output_position_demand

        v = symetrical_limit(s/ts, vMax, 0)
        a = symetrical_limit(v/ts, aMax, 0)
        v = symetrical_limit(v, np.sqrt(fiddle*2*aMax*abs(s)), 0)
        v = symetrical_limit(v, a*ts, last_output_velocity_demand)

        last_output_velocity_demand = v

        if abs(s) < (abs(input_velocity_demand[i])+0.5*aMax*ts*ts) and abs(v - input_velocity_demand[i]) < (1*aMax*ts):
            current_state = state['TRACKING']

        output_demand[i] = last_output_position_demand + v*ts

        state_array[i] = current_state
        last_output_velocity_demand = (output_demand[i] - last_output_position_demand)/ts

        last_output_position_demand = output_demand[i]
        continue

    if current_state is state['TRACKING']:
        if last_output_position_demand == input_position_demand[i]:
            current_state = state['STOPPED']
        output_demand[i] = input_position_demand[i]

    if current_state is state['STOPPED']:
        if last_output_position_demand != input_position_demand[i]:
            current_state = state['TRACKING']
        output_demand[i] = input_position_demand[i]

    state_array[i] = current_state
    last_output_velocity_demand = (output_demand[i] - last_output_position_demand)/ts

    last_output_position_demand = output_demand[i]

plt.figure(1)
ax1 = plt.subplot(311)
ax1.plot(t_range, input_position_demand, lw=0.75)
ax1.plot(t_range, output_demand, lw=0.75)
plt.title('Profiled demand')

ax2 = plt.subplot(312, sharex=ax1)
ax2.plot(t_range, np.gradient(output_demand, t_range), lw=0.75)
ax3 = plt.subplot(313, sharex=ax1)
ax3.plot(t_range, np.gradient(np.gradient(output_demand, t_range), t_range), lw=0.75)
ax3.axis([t_range[0], t_range[-1], -350, 350])

plt.figure(2)
plt.subplot(211)
plt.plot(t_range, input_position_demand-output_demand, lw=0.75)
plt.axis([t_range[0], t_range[-1], -1, 1])
plt.title('Error')
plt.subplot(212)
plt.plot(t_range, state_array, lw=0.75)
plt.axis([t_range[0], t_range[-1], -0.1, 2.1])


plt.figure(3)
ax4 = plt.subplot(311)
plt.title('Input Demand')
ax5 = plt.subplot(312, sharex=ax4)
ax6 = plt.subplot(313, sharex=ax4)

ax4.plot(t_range, input_position_demand, lw=0.75)

ax5.plot(t_range, input_velocity_demand, lw=0.75)
ax6.plot(t_range, input_acceleration_demand, lw=0.75)
ax5.axis([t_range[0], t_range[-1], -20, 20])
ax6.axis([t_range[0], t_range[-1], -10, 10])

plt.show()
