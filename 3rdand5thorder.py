"""Test"""

import matplotlib.pyplot as plt
import numpy as np


def createTraj3(theta0,thetaf,thetad0,thetadf,tstart,tfinal):
    # % inputs : initial position, velocity + final position, velocity + initial and final times
    # % output : a vector specifying the polynomial and can be used with poly functions such as 
    #  polyder, polyval, etc.
    # % create a 3rd order trajectory
    # % example:
    # % createTraj3(10,30,0,0,0,1)
    # %
    # %
    # % By: Reza Ahmadzadeh - Matlab/Octave - 2013
    T = tfinal - tstart
    a0 = theta0
    a1 = thetad0
    a2 = (-3 * (theta0 - thetaf) - (2 * thetad0+thetadf )*T)/ T ** 2
    a3 = (2 * (theta0 - thetaf) + (thetad0+thetadf )*T)/ T ** 3
    
    return np.array([a3, a2, a1, a0])


def createTraj5(theta0,thetaf,thetad0,thetadf,thetadd0,thetaddf,tstart,tfinal):
    # % inputs : initial position, velocity, and acceleration + final position, velocity, and acceleration, + initial and final times
    # % output : a vector specifying the polynomial and can be used with poly functions such as : polyder, polyval, etc.
    # % create a 5th order trajectory
    # % example:
    # % createTraj5(10,30,0,0,0,0,0,1)
    # %
    # %
    # % By: Reza Ahmadzadeh - Matlab/Octave - 2013
    T = tfinal - tstart
    a0 = theta0
    a1 = thetad0
    a2 = 0.5 * thetadd0
    a3 =(1/(2*T**3)) * (20 * (thetaf - theta0) - (8 * thetadf+ 12*thetad0 )*T - (3 * thetaddf - thetadd0 )*T**2 )
    a4 =(1/(2*T**4)) * (30 * (theta0 - thetaf) + (14 * thetadf+ 16*thetad0 )*T + (3 * thetaddf - 2*thetadd0 )*T**2 )
    a5 =(1/(2*T**5)) * (12 * (thetaf - theta0) - 6*(thetadf+ thetad0 )*T - (thetaddf - thetadd0 )*T**2 )

    return [a5,a4,a3,a2,a1,a0]

t_end = 1.8
ts = 1.0 / 500.0
coeff = createTraj5(0, 30, 0, 0, 0, 0, 0, t_end)
t = np.arange(0, t_end, ts)

pd = np.polyder(coeff)
pdd = np.polyder(pd)
pddd = np.polyder(pdd)

pos = np.polyval(coeff, t)
vel = np.polyval(pd, t)
acc = np.polyval(pdd, t)
jer = np.polyval(pddd, t)

plt.subplot(411)
plt.plot(t, pos)
plt.subplot(412)
plt.plot(t, vel)
plt.subplot(413)
plt.plot(t, acc)
plt.subplot(414)
plt.plot(t, jer)

plt.show()
