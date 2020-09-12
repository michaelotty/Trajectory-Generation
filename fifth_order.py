"""Create 5th order slew"""

import numpy as np
import matplotlib.pyplot as plt


def create_traj3(s_0, s_f, v_0, v_f, t_0, t_f):
    """create_traj3
    inputs : initial position, velocity + final position, velocity + initial and final times
    output : a vector specifying the polynomial and can be used with poly functions such as
    polyder, polyval, etc.
    create a 3rd order trajectory"""

    t_d = t_f - t_0
    poly_0 = s_0
    poly_1 = v_0
    poly_2 = (-3 * (s_0 - s_f) - (2 * v_0+v_f )*t_d)/ t_d ** 2
    poly3 = (2 * (s_0 - s_f) + (v_0+v_f )*t_d)/ t_d ** 3

    return [poly3, poly_2, poly_1, poly_0]


def create_traj5(s_0, s_f, v_0, v_f, a_0, a_f, initial_t, final_t):
    """create_traj5
    inputs : initial position, velocity, and acceleration + final position, velocity, and
    acceleration, + initial and final times
    output : a vector specifying the polynomial and can be used with poly functions such as :
    polyder, polyval, etc.
    create a 5th order trajectory"""

    t_d = final_t - initial_t
    poly_0 = s_0
    poly_1 = v_0
    poly_2 = 0.5 * a_0
    poly_3 = (1/(2*t_d**3)) * (20 * (s_f - s_0) - (8*v_f + 12*v_0)*t_d - (3*a_f - a_0)* t_d**2)
    poly_4 = (1/(2*t_d**4)) * (30 * (s_0 - s_f) + (14*v_f + 16*v_0)*t_d + (3*a_f - 2*a_0)* t_d**2)
    poly_5 = (1/(2*t_d**5)) * (12 * (s_f - s_0) - 6*(v_f + v_0)*t_d - (a_f - a_0)* t_d**2)

    return [poly_5,poly_4,poly_3,poly_2,poly_1,poly_0]

T_END = 1
TS = 1 / 500.0
t_range = np.arange(0, T_END, TS)
s_traj = np.polyval(create_traj5(0, 1, 0, 0, 0, 0, 0, T_END), t_range)
v_traj = np.gradient(s_traj, TS)
a_traj = np.gradient(v_traj, TS)
j_traj = np.gradient(a_traj, TS)

plt.subplot(411)
plt.plot(t_range, s_traj)
plt.subplot(412)
plt.plot(t_range, v_traj)
plt.subplot(413)
plt.plot(t_range, a_traj)
plt.subplot(414)
plt.plot(t_range, j_traj)

plt.show()
