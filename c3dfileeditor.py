import btk
import matplotlib.pyplot as plt
#matplotlib inline
import numpy as np
import pprint as p
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import sys


reader = btk.btkAcquisitionFileReader()  # build a btk reader object 
reader.SetFilename('GaitNormal0003-processed.c3d')      # set a filename to the reader
acq = reader.GetOutput()                 # btk aquisition object
acq.Update()                             # Update ProcessObject associated with DataObject
clone = acq.Clone()

for i in range(0, acq.GetAnalogs().GetItemNumber()):
    print(acq.GetAnalog(i).GetLabel())   



#plots the values for forces on the z axis in the three plates
ana = acq.GetAnalog("Fz1")
fz1 = ana.GetValues()/ana.GetScale()

#modifies the values in the z axis 1st force plate

ana = clone.GetAnalog("Fz1")
valz1 = ana.GetValues()
scalez1 = ana.GetScale()
x = 0
y = float(sys.argv[2])
for forcez1 in np.nditer(valz1):
        if forcez1/scalez1 > y:
		ana.SetValue(x,y * scalez1)
#		print(ana.GetValue(x))
	x = x + 1
	
	




ana = acq.GetAnalog("Fz2")
fz2 = ana.GetValues()/ana.GetScale()


#modifies the values in the z axis 2nd force plate

ana = clone.GetAnalog("Fz2")
valz2 = ana.GetValues()
scalez2 = ana.GetScale()
x = 0
for forcez2 in np.nditer(valz2):
        if forcez2/scalez2 > y:
                ana.SetValue(x,y * scalez2)
        x = x + 1




ana = acq.GetAnalog("Fz3")
fz3 = ana.GetValues()/ana.GetScale()

#modifies the values in the z axis 3rd force plate

ana = clone.GetAnalog("Fz3")
valz3 = ana.GetValues()
scalez3 = ana.GetScale()
x = 0
for forcez3 in np.nditer(valz3):
        if forcez3/scalez3 > y:
               ana.SetValue(x,y * scalez3)
        x = x + 1




freq2 = acq.GetAnalogFrequency()
t = np.linspace(1, len(fz1), num=len(fz1))/freq2
valz = ana.GetValues()
scale = ana.GetScale()
#for force in np.nditer(valz):
#	print(force/scale)
plt.figure(figsize=(10, 4))
#plt.figure(num=1)
plt.plot(t, fz1, label='Fz1')
plt.plot(t, fz2, label='Fz2')
plt.plot(t, fz3, label='Fz3')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('GRF vertical [N]')
#plt.figure(0)
plt.savefig('forceZaxis.png')


#create a modified c3d file

writer = btk.btkAcquisitionFileWriter()
writer.SetInput(clone)
writer.SetFilename(sys.argv[1]+'.c3d')
writer.Update()

#plot the modified c3d file

reader2 = btk.btkAcquisitionFileReader()  # build a btk reader object 
reader2.SetFilename(sys.argv[1]+'.c3d')      # set a filename to the reader
acq2 = reader2.GetOutput()                 # btk aquisition object
acq2.Update()                             # Update ProcessObject associated with DataObject



ana = acq2.GetAnalog("Fz1")
fz1 = ana.GetValues()/ana.GetScale()
ana = acq2.GetAnalog("Fz2")
fz2 = ana.GetValues()/ana.GetScale()
ana = acq2.GetAnalog("Fz3")
fz3 = ana.GetValues()/ana.GetScale()
freq2 = acq2.GetAnalogFrequency()
t = np.linspace(1, len(fz1), num=len(fz1))/freq2
plt.figure(figsize=(10, 4))
plt.plot(t, fz1, label='Fz1')
plt.plot(t, fz2, label='Fz2')
plt.plot(t, fz3, label='Fz3')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('GRF vertical [N]')
#plt.figure(2)
plt.savefig('modifiedforceZaxis')



#plots the values of the force in the y axis in the three plates
ana = acq.GetAnalog("Fy1")
fy1 = ana.GetValues()/ana.GetScale()
p.pprint(ana)
ana = acq.GetAnalog("Fy2")
fy2 = ana.GetValues()/ana.GetScale()
ana = acq.GetAnalog("Fy3")
fy3 = ana.GetValues()/ana.GetScale()
freq2 = acq.GetAnalogFrequency()
t = np.linspace(1, len(fy1), num=len(fy1))/freq2
#plt.figure(num=2)
plt.figure(figsize=(10, 4))
plt.plot(t, fy1, label='Fy1')
plt.plot(t, fy2, label='Fy2')
plt.plot(t, fy3, label='Fy3')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('GRF vertical [N]')
#plt.figure(2)
plt.savefig('forceYaxis')

#plot the values of the force in the x axis in the three plates
ana = acq.GetAnalog("Fx1")
fx1 = ana.GetValues()/ana.GetScale()
ana = acq.GetAnalog("Fx2")
fx2 = ana.GetValues()/ana.GetScale()
ana = acq.GetAnalog("Fx3")
fx3 = ana.GetValues()/ana.GetScale()
freq2 = acq.GetAnalogFrequency()
t = np.linspace(1, len(fx1), num=len(fx1))/freq2
plt.figure(figsize=(10, 4))
plt.plot(t, fx1, label='Fx1')
plt.plot(t, fx2, label='Fx2')
plt.plot(t, fx3, label='Fx3')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('GRF vertical [N]')
#plt.figure(3)
plt.savefig('forceXaxis')

''' data = np.empty((3, acq.GetPointFrameNumber(), 1))
for i in range(0, acq.GetPoints().GetItemNumber()):
    label = acq.GetPoint(i).GetLabel()
    data = np.dstack((data, acq.GetPoint(label).GetValues().T))
data = data.T
data = np.delete(data, 0, axis=0)  # first marker is noisy for this file
data[data==0] = np.NaN             # handle missing data (zeros)
data.shape
dat = data[:, 130:340, :]
freq = acq.GetPointFrequency()

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.view_init(10, 150)
pts = []
for i in range(dat.shape[0]):
    pts += ax.plot([], [], [], 'o')

ax.set_xlim3d([np.nanmin(dat[:, :, 0]), np.nanmax(dat[:, :, 0])])
ax.set_ylim3d([np.nanmin(dat[:, :, 1]), np.nanmax(dat[:, :, 1])])
ax.set_zlim3d([np.nanmin(dat[:, :, 2]), np.nanmax(dat[:, :, 2])])
ax.set_xlabel('X [mm]')
ax.set_ylabel('Y [mm]')
ax.set_zlabel('Z [mm]')
ax.view_init(azim = 0,elev=22)
# animation function
def animate(i):
    for pt, xi in zip(pts, dat):
        z, y, x = xi[:i].T
        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])   
    return pts

# Animation object
anim = animation.FuncAnimation(fig, func=animate, frames=dat.shape[1], interval=1000/freq, blit=True)

plt.show() '''
