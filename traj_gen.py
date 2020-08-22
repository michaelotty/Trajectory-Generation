"""Trajectory Generator"""

import numpy as np
import matplotlib.pyplot as plt

j_max = 1000.0
a_max = 100.0
v_max = 20.0
s1 = 0.0
s2 = 20.0
s = abs(s2 - s1)
direction = np.sign(s2 - s1)

v_a = (a_max**2)/j_max
s_a = (2 * a_max**3)/j_max**2

if ((v_max * j_max) < (a_max**2)):
    M = 1
    N = 0
else:
    M = 0
    N = 1

s_v = v_max * (M * (2.0 * np.sqrt(v_max/j_max)) + N * (v_max/a_max + a_max/j_max))

# Type I or III
if ((v_max < v_a) and (s >= s_a)) or ((v_max < v_a) and (s < s_a) and (s >= s_v)):
    print('Type I or III')
    t_j = np.sqrt(v_max/j_max)
    t_a = t_j
    t_v = s/v_max

# Type II or IV
elif ((v_max >= v_a) and (s < s_a)) or ((v_max < v_a) and (s < s_a) and (s < s_v)):
    print('Type II or IV')
    t_j = np.cbrt(s/(2*j_max))
    t_a = t_j
    t_v = 2 * t_j

# Type V
elif ((v_max >= v_a) and (s >= s_a) and (s >= s_v)):
    print('Type V')
    t_j = a_max/j_max
    t_a = v_max/a_max
    t_v = s/v_max

# Type VI
elif ((v_max >= v_a) and (s >= s_a) and (s < s_v)):
    print('Type VI')
    t_j = a_max/j_max
    t_a = 1/2 * (np.sqrt((4*s*j_max^2 + a_max**3)/(a_max*j_max**2)) - a_max/j_max)
    t_v = t_a + t_j

t1 = t_j
t2 = t_a
t3 = t_j + t_a
t4 = t_v
t5 = t_v + t_j
t6 = t_v + t_a
t7 = t_v + t_a + t_j

print(f'Time: {t1}, {t2}, {t3}, {t4}, {t5}, {t6}, {t7}')

ts = 1.0 / 500.0

s_profile = np.array([])
v_profile = np.array([])
a_profile = np.array([])

t = np.arange(0, t1, ts)
s1 = 1/6 * j_max * t**3
v1 = 1/2 * j_max * t**2
a1 = j_max * t
s_profile = np.append(s_profile, s1)
v_profile = np.append(v_profile, v1)
a_profile = np.append(a_profile, a1)
pos_ax = plt.subplot(411)
pos_ax.plot(t, s1, color='black', lw=0.75)

t = np.arange(0, t2 - t1, ts)
s2 = s_profile[-1] + v_profile[-1] * t + 1/2 * a_profile[-1] * t**2
v2 = v_profile[-1] + a_profile[-1] * t
a2 = a_profile[-1] * np.ones_like(s2)
s_profile = np.append(s_profile, s2)
v_profile = np.append(v_profile, v2)
a_profile = np.append(a_profile, a2)
pos_ax.plot(t+t1, s2, color='brown', lw=0.75)

t = np.arange(0, t3 - t2, ts)
s3 = s_profile[-1] + v_profile[-1] * t + 1/2 * a_profile[-1] * t**2 + 1/6 * -j_max * t**3
v3 = v_profile[-1] + a_profile[-1] * t + 1/2 * -j_max * t**2
a3 = a_profile[-1] - j_max * t
s_profile = np.append(s_profile, s3)
v_profile = np.append(v_profile, v3)
a_profile = np.append(a_profile, a3)
pos_ax.plot(t+t2, s3, color='red', lw=0.75)

t = np.arange(0, t4 - t3, ts)
s4 = s_profile[-1] + v_profile[-1] * t
v4 = v_profile[-1] * np.ones_like(s4)
a4 = np.zeros_like(s4)
s_profile = np.append(s_profile, s4)
v_profile = np.append(v_profile, v4)
a_profile = np.append(a_profile, a4)
pos_ax.plot(t+t3, s4, color='orange', lw=0.75)

t = np.arange(0, t5 - t4, ts)
s5 = s_profile[-1] + v_profile[-1] * t + 1/6 * -j_max * t**3
v5 = v_profile[-1] + 1/2 * -j_max * t**2
a5 = -j_max * t
s_profile = np.append(s_profile, s5)
v_profile = np.append(v_profile, v5)
a_profile = np.append(a_profile, a5)
pos_ax.plot(t+t4, s5, color='yellow', lw=0.75)

t = np.arange(0, t6 - t5, ts)
s6 = s_profile[-1] + v_profile[-1] * t + 1/2 * a_profile[-1] * t**2
v6 = v_profile[-1] + a_profile[-1] * t + 1/2
a6 = a_profile[-1] * np.ones_like(s6)
s_profile = np.append(s_profile, s6)
v_profile = np.append(v_profile, v6)
a_profile = np.append(a_profile, a6)
pos_ax.plot(t+t5, s6, color='green', lw=0.75)

t = np.arange(0, t7 - t6, ts)
s7 = s_profile[-1] + v_profile[-1] * t + 1/2 * a_profile[-1] * t**2 + 1/6 * j_max * t**3
v7 = v_profile[-1] + a_profile[-1] * t + 1/2 * j_max * t**2
a7 = a_profile[-1] + j_max * t
s_profile = np.append(s_profile, s7)
v_profile = np.append(v_profile, v7)
a_profile = np.append(a_profile, a7)
pos_ax.plot(t+t6, s7, color='blue', lw=0.75)

t = np.arange(0, t7+(ts*3), ts)
vel_ax = plt.subplot(412, sharex=pos_ax)
vel_ax.plot(t, v_profile, lw=0.75)

acc_ax = plt.subplot(413, sharex=pos_ax)
acc_ax.plot(t, a_profile, lw=0.75)

jer_ax = plt.subplot(414, sharex=pos_ax)
jer_ax.plot(t[:-1], np.diff(a_profile)/ts, lw=0.75)

plt.show()
