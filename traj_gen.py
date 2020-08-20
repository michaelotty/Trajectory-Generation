"""Trajectory Generator"""

import numpy as np

j_max = 20
a_max = 200
v_max = 20
s1 = 0
s2 = 100

s = abs(s2 - s1)
v_a = (a_max**2)/j_max
s_a = (2*a_max**3)/j_max**2

if ((v_max * j_max) < (a_max**2)):
    M = 1
    N = 0
else:
    N = 0
    M = 1


s_v = v_max * (M * (2 * np.sqrt(v_max/j_max)) + N * (v_max/a_max + a_max/j_max))

# Type I
if ((v_max < v_a) and (s >= s_a)):
    print('Type I')
    t_j = np.sqrt(v_max/j_max)
    t_a = t_j
    t_v = s/v_max

# Type II
elif ((v_max >= v_a) and (s < s_a)):
    print('Type II')

# Type III
elif ((v_max < v_a) and (s < s_a) and (s >= s_v)):
    print('Type III')


# Type IV
elif ((v_max < v_a) and (s < s_a) and (s < s_v)):
    print('Type IV')


# Type V
elif ((v_max >= v_a) and (s >= s_a) and (s >= s_v)):
    print('Type V')


# Type VI
elif ((v_max >= v_a) and (s >= s_a) and (s < s_v)):
    print('Type VI')
