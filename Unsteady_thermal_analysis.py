import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy.ma.core import shape, sqrt
from matplotlib.animation import FuncAnimation

l = float(input("length: "))
w = float(input("widht: "))
cx = int(input("cells along x: "))
cy = int(input("cells along y: "))
bb = {
    'cells' : [],
    't' : float(0),
    'name' : "bottom"
}
rb = {
    'cells' : [],
    't' : float(0),
    'name' : "right"
}
tb = {
    'cells' : [],
    't' : float(1),
    'name' : "top"
}
lb = {
    'cells' : [],
    't' : float(1),
    'name' : "left"
}
for boundary in [lb,rb,bb,tb]:
    boundary['t'] = input("Enter the Temp for " + boundary['name'] + " boundary: ")
alpha = 1
dx = l / cx
dy = w / cy
max_dt =(dx*dy)/(alpha*4)
print("Maximum value of time step: ",max_dt)
dt = float(input("Input Time step: "))
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
TempxTime = np.zeros(shape= (cx, cy, 50000))
iteration = int(0)
net_time = 0
oldTemp = Temp
while True:
    
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
    net_time += dt
    iteration += 1
    TempxTime[:,:,iteration] = Temp
    if np.max(TempxTime[:,:,iteration] - TempxTime[:,:,iteration - 1]) < 0.000001:
        break
    oldTemp = Temp

print("Net time to reach steady state is ",net_time, "s")
time = float(input("Input time for Temp distribution graph: "))
if time > net_time:
    raise ValueError
    exit()
time = int(time/dt)
z = TempxTime[:,:,time]
plt.contourf(ycells, xcells,z,20,cmap=plt.cm.jet)
plt.show()

fig = plt.figure()

def animate(i): 
    z = TempxTime[:,:,i*5]
    cont = plt.contourf(ycells, xcells, z,10,cmap=plt.cm.jet)

    return cont  

fr = int(iteration/5)
anim = FuncAnimation(fig, animate, frames=fr, interval= dt)
plt.show()

# activate command below to save the animation
# anim.save('animation_unsteady.gif')
exit()