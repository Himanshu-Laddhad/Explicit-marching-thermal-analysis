import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy.ma.core import shape, sqrt

l = float(10)
cx = int(20)
rb = {
    't' : float(-0.1),
    'name' : "right"
}
lb = {
    't' : float(1),
    'name' : "left"
}
alpha = 1
dx = l / cx
max_dt =(dx**2)/(alpha*2)
print("Maximum value of time step: ",max_dt)
dt = float(0.001)
if dt > max_dt:
    raise ValueError
    exit()

xcells = np.array([(2*i+1)*dx/2 for i in range(cx)])

Temp = np.zeros(shape = (cx))
TempxTime = np.zeros(shape= (cx,50000))
iteration = int(0)
net_time = 0
oldTemp = Temp
while True:
    for i in range(cx):
        n = float(0)
        if i == cx - 1:#right
            n += 2*float(rb['t']) + oldTemp[i]
        else:
            n += oldTemp[i+1]
        if i == 0:#left
            n += 2*float(lb['t']) - oldTemp[i]
        else:
            n += oldTemp[i-1]
        n = ((float(alpha)*dt*n)/(dx*dx)) + ((1 - (dt/max_dt))*oldTemp[i])
        Temp[i] = n
    net_time += dt
    iteration += 1
    TempxTime[:,iteration] = Temp
    if np.max(TempxTime[:,iteration] - TempxTime[:,iteration - 1]) < 0.000001:
        break
    oldTemp = Temp
print(Temp)
print("Net time to reach steady state is ",net_time, "s")
for time in range(1,iteration,int(iteration/5)):
    z = TempxTime[:,time]
    plt.plot(xcells,z)
plt.show()
