"""Trajectory Generator"""

from math import ceil

import matplotlib.pyplot as plt
import numpy as np

J_MAX = 1000.0
A_MAX = 100.0
V_MAX = 20.0
S_START = 0.0
S_END = 30.0
TS = 1.0 / 500.0

s = abs(S_END - S_START)
direction = np.sign(S_END - S_START)

V_A = (A_MAX**2)/J_MAX
S_A = (2 * A_MAX**3)/J_MAX**2

if (V_MAX * J_MAX) < (A_MAX**2):
    S_V = V_MAX * 2.0 * np.sqrt(V_MAX/J_MAX)
else:
    S_V = V_MAX * (V_MAX/A_MAX + A_MAX/J_MAX)

# Type I or III
if ((V_MAX < V_A) and (s >= S_A)) or ((V_MAX < V_A) and (s < S_A) and (s >= S_V)):
    print('Type I or III')
    T_J = np.sqrt(V_MAX/J_MAX)
    T_A = T_J
    T_V = s/V_MAX

# Type II or IV
elif ((V_MAX >= V_A) and (s < S_A)) or ((V_MAX < V_A) and (s < S_A) and (s < S_V)):
    print('Type II or IV')
    T_J = np.cbrt(s/(2*J_MAX))
    T_A = T_J
    T_V = 2 * T_J

# Type V
elif ((V_MAX >= V_A) and (s >= S_A) and (s >= S_V)):
    print('Type V')
    T_J = A_MAX/J_MAX
    T_A = V_MAX/A_MAX
    T_V = s/V_MAX

# Type VI
elif ((V_MAX >= V_A) and (s >= S_A) and (s < S_V)):
    print('Type VI')
    T_J = A_MAX/J_MAX
    T_A = 1/2 * (np.sqrt((4*s*J_MAX^2 + A_MAX**3)/(A_MAX*J_MAX**2)) - A_MAX/J_MAX)
    T_V = T_A + T_J

t1 = T_J
t2 = T_A
t3 = T_J + T_A
t4 = T_V
t5 = T_V + T_J
t6 = T_V + T_A
t7 = T_V + T_A + T_J

print(f'Time: {t1}, {t2}, {t3}, {t4}, {t5}, {t6}, {t7}')

# Create motion path step by step
s_profile = np.array([])
steps = ceil(t7/TS)
t = np.linspace(0, t7, num=steps+1)

# Step 1
s1 = 1/6 * J_MAX * t**3
v1 = 1/2 * J_MAX * t**2
a1 = J_MAX * t
s_profile = np.append(s_profile, s1)
pos_ax = plt.subplot(411)
pos_ax.plot(t, s1, color='black', lw=0.75)

t = t1
s_end = 1/6 * J_MAX * t**3
v_end = 1/2 * J_MAX * t**2
a_end = J_MAX * t


# Step 2
t = np.arange(0, t2 - t1, TS)
s2 = s_end + v_end * t + 1/2 * a_end * t**2
v2 = v_end + a_end * t
a2 = a_end * np.ones_like(s2)
s_profile = np.append(s_profile, s2)
pos_ax.plot(t+t1, s2, color='brown', lw=0.75)

t = t2 - t1
s_end = s_end + v_end * t + 1/2 * a_end * t**2
v_end = v_end + a_end * t
# a_end = a_end


# Step 3
t = np.arange(0, t3 - t2, TS)
s3 = s_end + v_end * t + 1/2 * a_end * t**2 + 1/6 * -J_MAX * t**3
v3 = v_end + a_end * t + 1/2 * -J_MAX * t**2
a3 = a_end - J_MAX * t
s_profile = np.append(s_profile, s3)
pos_ax.plot(t+t2, s3, color='red', lw=0.75)

t = t3 - t2
s_end = s_end + v_end * t + 1/2 * a_end * t**2 + 1/6 * -J_MAX * t**3
v_end = v_end + a_end * t + 1/2 * -J_MAX * t**2
a_end = a_end - J_MAX * t


# Step 4
t = np.arange(0, t4 - t3, TS)
s4 = s_end + v_end * t
v4 = v_end * np.ones_like(s4)
a4 = np.zeros_like(s4)
s_profile = np.append(s_profile, s4)
pos_ax.plot(t+t3, s4, color='orange', lw=0.75)

t = t4 - t3
s_end = s_end + v_end * t
v_end = v_end * 1.0
a_end = 0.0


# Step 5
t = np.arange(0, t5 - t4, TS)
s5 = s_end + v_end * t + 1/6 * -J_MAX * t**3
v5 = v_end + 1/2 * -J_MAX * t**2
a5 = -J_MAX * t
s_profile = np.append(s_profile, s5)
pos_ax.plot(t+t4, s5, color='yellow', lw=0.75)

t = t5 - t4
s_end = s_end + v_end * t + 1/6 * -J_MAX * t**3
v_end = v_end + 1/2 * -J_MAX * t**2
a_end = -J_MAX * t


# Step 6
t = np.arange(0, t6 - t5, TS)
s6 = s_end + v_end * t + 1/2 * a_end * t**2
v6 = v_end + a_end * t + 1/2
a6 = a_end * np.ones_like(s6)
s_profile = np.append(s_profile, s6)
pos_ax.plot(t+t5, s6, color='green', lw=0.75)

t = t6 - t5
s_end = s_end + v_end * t + 1/2 * a_end * t**2
v_end = v_end + a_end * t + 1/2
# a_end = a_end


# Step 7
t = np.arange(0, t7 - t6, TS)
s7 = s_end + v_end * t + 1/2 * a_end * t**2 + 1/6 * J_MAX * t**3
v7 = v_end + a_end * t + 1/2 * J_MAX * t**2
a7 = a_end + J_MAX * t
s_profile = np.append(s_profile, s7)
pos_ax.plot(t+t6, s7, color='blue', lw=0.75)


# Gather Results and Plot
s_profile = direction * np.concatenate((s1, s2, s3[:-1], s4, s5[:-1], s6, s7[:-3]))

t = np.arange(0, t7-(TS*2), TS)
vel_ax = plt.subplot(412, sharex=pos_ax)
vel_ax.plot(t[:-1], np.diff(s_profile)/TS, lw=0.75)

acc_ax = plt.subplot(413, sharex=pos_ax)
acc_ax.plot(t[:-2], np.diff(np.diff(s_profile)/TS)/TS, lw=0.75)

jer_ax = plt.subplot(414, sharex=pos_ax)
jer_ax.plot(t[:-3], np.diff(np.diff(np.diff(s_profile)/TS)/TS)/TS, lw=0.75)

plt.figure(2)
plt.plot(t, s_profile)

plt.show()
