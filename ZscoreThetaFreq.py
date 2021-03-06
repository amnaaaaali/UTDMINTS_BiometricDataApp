# CODE TO READ DATA STREAM FROM COGNIONICS DATA ACQUISITION SOFTWARE

# CODE AUTHORED BY SHAWHIN TALEBI AND SAM SHIDLER

# import necessary functions
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import numpy as np
import time
from EEGArray import EEGArray
from GetCmapValues import getCmapForZscores
import scipy.signal as sps
from scipy import stats
# import http.server as server
import socketserver


# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.title.set_text("Theta Band By Z-scores")
# set colormap
cmap = plt.cm.seismic

# define number of electrodes
n = 64

# # define node positions
# x, y = np.meshgrid(np.arange(0, 8), np.arange(0, 8))
# x = x.reshape(n)
# y = y.reshape(n)
x, y, _ = EEGArray()

# initialize newdata
newdata = np.zeros(n)

# initialize scatter plot
scat1 = ax1.scatter(x, y, s=100, c=newdata, vmin=0,
                    vmax=1, cmap=plt.cm.seismic_r)
cbar = fig.colorbar(scat1, ax=ax1, ticks=[0, 0.5, 1])
cbar.ax.set_yticklabels(['-1', '0', '1'])

# for j, lab in enumerate(['$0$','$1$','$2$','$3$']):
#     cbar.ax.text(.5, (2 * j + 1) / 8.0, lab, ha='center', va='center')
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('Normalized Z-scores', rotation=90)

# initialize 64 by 64 data array
data = np.zeros((n, n))

# # Set up formatting for the movie files (uncomment this to record)
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=7, metadata=dict(artist='Me'), bitrate=-1)

# define function to plot nodes


def plotNodes(i):
    global data

    start_time = time.time()
    inlet = StreamInlet(streams[0])

    # get a new sample
    sample = inlet.pull_sample()
    newdata = np.asarray(sample[0][:n])
    # print(newdata)

    zscoreArray, data = getCmapForZscores(data, newdata, -2)

    colors = cmap(zscoreArray)
    # colors.astype(float)
    # colors[:, -1] = maxes / maxes.max()
    # print(altColors)
    # print(colors)

    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    # ax1.scatter(x, y, s = 100, c = altColors, cmap = plt.cm.jet_r)
    ax1.scatter(x, y, s=100, c=colors)

    elapsed_time = time.time() - start_time


# print(elapsed_time)

# plot animation
ani = FuncAnimation(fig, plotNodes, interval=100)
# ani.save('visual.mp4', fps=7)3
# # save animation (uncomment to record)
# ani.save('EEG_visiualization_LSL.mp4', writer=writer)

plt.show()
