# CODE TO READ DATA STREAM FROM COGNIONICS DATA ACQUISITION SOFTWARE

# CODE AUTHORED BY SHAWHIN TALEBI AND SAM SHIDLER

# import necessary functions
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from EEGArray import EEGArray
<<<<<<< HEAD
=======
import scipy.signal as sps
>>>>>>> temp

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# define number of electrodes
n = 64

# define node positions
x, y = EEGArray()

# initialize data
data = np.zeros(n)

# initialize scatter plot
<<<<<<< HEAD
scat1 = ax1.scatter(x, y, c=data, s=100, cmap=plt.cm.RdYlGn, vmin=-15, vmax=15)
=======
scat1 = ax1.scatter(x, y, c = data, s = 100, cmap = plt.cm.RdYlGn, vmin=-15,vmax=15)
>>>>>>> temp
fig.colorbar(scat1, ax=ax1)

# define function to plot nodes
def plotNodes(i):
    global data

    start_time = time.time()
    inlet = StreamInlet(streams[0])

    # get a new sample
    sample = inlet.pull_sample()
    data = np.asarray(sample[0][:n])
    PosData = data > 0
    NegData = PosData + (-1)*np.ones(len(PosData))
    # print(PosData+NegData)
    # print(data)
    print(np.log(abs(data))*(PosData+NegData))

<<<<<<< HEAD
    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    # Plots amplitudes
    # ax1.scatter(x, y, c = data, s = 100, cmap = plt.cm.RdBu_r, vmin=-10000,vmax=10000)
    ax1.scatter(x, y, c=data, s=100, cmap=plt.cm.RdYlGn, vmin=-15, vmax=15)

    elapsed_time = time.time() - start_time
    print(elapsed_time)

=======
    ax1.set_xlim(-6,6)
    ax1.set_ylim(-6,6)
    # ax1.scatter(x, y, c = data, s = 100, cmap = plt.cm.RdBu_r, vmin=-10000,vmax=10000)
    ax1.scatter(x, y, c = data, s = 100, cmap = plt.cm.RdYlGn, vmin=-15,vmax=15)

    elapsed_time = time.time() - start_time
    print(elapsed_time)
>>>>>>> temp
ani = FuncAnimation(fig, plotNodes, interval=100)
plt.show()
