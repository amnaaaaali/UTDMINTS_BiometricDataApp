# CODE TO READ DATA STREAM FROM COGNIONICS DATA ACQUISITION SOFTWARE

# CODE AUTHORED BY SHAWHIN TALEBI AND SAM SHIDLER

# import necessary functions
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import numpy as np
import time
from EEGArray import EEGArray
from GetCmapValues import getCmapByFreqVal
import scipy.signal as sps
import socketserver
import sys


# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# set colormap
cmap = cm.get_cmap("jet")

# define number of electrodes
n = 64

# # define node positions
# x, y = np.meshgrid(np.arange(0, 8), np.arange(0, 8))
# x = x.reshape(n)
# y = y.reshape(n)
x, y = EEGArray()

# initialize newdata
newdata = np.zeros(n)

# initialize scatter plot
scat1 = ax1.scatter(x, y, s=100, c=newdata, vmin=0, vmax=1, cmap=plt.cm.jet_r)
cbar = fig.colorbar(scat1, ax=ax1, ticks=[0, 0.5, 1])
cbar.ax.set_yticklabels(['0', '0.5', '1'])

# for j, lab in enumerate(['$0$','$1$','$2$','$3$']):
#     cbar.ax.text(.5, (2 * j + 1) / 8.0, lab, ha='center', va='center')
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('Normalized Amplitude', rotation=90)

# initialize 64 by 64 data array
data = np.zeros((n, n))

# a few global variables to maintain the maximum we have seen so far, as well as counters to see
# how many times the counters are being updated
globalMax = -(sys.maxsize)-1
# # Set up formatting for the movie files (uncomment this to record)
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=7, metadata=dict(artist='Me'), bitrate=-1)

# define function to plot nodes


def plotNodes(i):
    global data
    global globalMax

    start_time = time.time()
    inlet = StreamInlet(streams[0])

    # get a new sample
    sample = inlet.pull_sample()
    newdata = np.asarray(sample[0][:n])

    temp, globalMax, data = getCmapByFreqVal(data, newdata, 2.5, globalMax)

    colors = cmap(temp)
    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    # ax1.scatter(x, y, s = 100, c = altColors, cmap = plt.cm.jet_r)
    ax1.scatter(x, y, s=100, c=colors, cmap=plt.cm.jet_r)
    elapsed_time = time.time() - start_time


# plot animation

ani = FuncAnimation(fig, plotNodes, interval=100)
# ani.save('visual.mp4', fps=7)
# # save animation (uncomment to record)
# ani.save('EEG_visiualization_LSL.mp4', writer=writer)

plt.show()
