import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy.ma.core import shape

l = 10
w = 10
cx = 20
cy = 20
dt = 0.01
bb = {
    'cells' : [],
    't' : float(0)
}
rb = {
    'cells' : [],
    't' : float(0)
}
tb = {
    'cells' : [],
    't' : float(1)
}
lb = {
    'cells' : [],
    't' : float(1)
}
alpha = 1
dx = l / cx
dy = w / cy
max_dt =(dx*dy)/(alpha*4)
print("Maximum value of time step: ",max_dt)
if dt > max_dt:
    raise ValueError
    exit()

xcells = np.array([(2*i+1)*dx/2 for i in range(cx)])
ycells = np.array([(2*i+1)*dy/2 for i in range(cy)])

for i in range(cx):
    for j in range(cy):
        if j == cy - 1 and i in range(0, cx): 
            rb['cells'].append((i,j))
        if i == 0 and j in range(0, cy): 
            bb['cells'].append((i,j))
        if i == cx - 1 and j in range(0, cy):
            tb['cells'].append((i,j))
        if j == 0 and i in range(0, cx): 
            lb['cells'].append((i,j))

Temp = np.zeros(shape = (cx, cy,))
TempxTime = np.zeros(shape= (cx, cy, 100000))
iteration = int(0)
net_time = 0
while True:
    oldTemp = Temp
    for i in range(cx):
        for j in range(cy):
            n = float(0)
            if (i,j) in bb['cells']:#west
                n += 2*float(bb['t']) - oldTemp[i,j]
            else:
                n += oldTemp[i-1,j]
            if (i,j) in tb['cells']:#east
                n += 2*float(tb['t']) - oldTemp[i,j]
            else:
                n += oldTemp[i+1,j]
            if (i,j) in rb['cells']:#north
                n += 2*float(rb['t']) - oldTemp[i,j]
            else:
                n += oldTemp[i,j+1]
            if (i,j) in lb['cells']:#south
                n += 2*float(lb['t']) - oldTemp[i,j]
            else:
                n += oldTemp[i,j-1]
            n = ((float(alpha)*dt*n)/(dx*dy)) + ((1 - (dt/max_dt))*oldTemp[i,j])
            Temp[i,j] = n
    iteration += 1
    net_time += dt
    if iteration > 1000:
        break
    TempxTime[:,:,iteration] = Temp

print("Net time is ",net_time, "s")
time = float(input("Input time: "))
if time > net_time:
    raise ValueError
    exit()
time = int(time/dt)
z = TempxTime[:,:,time]
plt.contourf(ycells, xcells,z,20,cmap=plt.cm.jet)
plt.show()







