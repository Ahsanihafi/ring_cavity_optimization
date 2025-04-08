import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(5,10))



inst=[72,199]
for i in range(len(inst)):
    data = np.loadtxt('data/Output_%d.csv'%inst[i], delimiter=',')
    control = np.loadtxt('control_point/control_%d.csv'%inst[i], delimiter = ',')
    tdata = np.transpose(data)
    sumbux = tdata[1]
    sumbuy = tdata[2]
    tcontrol = np.transpose(control)
    controlx = tcontrol[0]
    controly = tcontrol[1]
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.plot(sumbux,sumbuy, label='Cavity-%d'%inst[i])
    plt.scatter(controlx,controly)
plt.legend()
plt.savefig('full_design_final.png')
plt.show()

"""
i=222
data = np.loadtxt('data/Output_%d.csv'%i, delimiter=',')
tdata = np.transpose(data)
sumbux = tdata[1]
sumbuy = tdata[2]
plt.plot(sumbux,sumbuy, label='Cavity-%d'%i)
"""
