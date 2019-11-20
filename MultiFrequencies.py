# import necessary functions
from pylsl import StreamInlet, resolve_stream
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import numpy as np
import time
from EEGArray import EEGArray
from SelectFrequency import getAmplitudesByFrequencyBand
from GetCmapValues import getCmapByFreqVal
import scipy.signal as sps
import socketserver
import sys


print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# changes the backend used to set up the figure, to support the forced placement
# of the figure on the screen
matplotlib.use("TkAgg")
# removes toolbar at the bottom of plot
matplotlib.rcParams['toolbar'] = 'None'
# create figure. figsize sets the default size of the
fig = plt.figure(figsize=(10, 4))
# remove extra spacing around figure
fig.set_tight_layout(True)
# ax1 is delta freq, ax2 = theta freq, ax3 = alpha freq
ax1 = fig.add_subplot(1, 3, 1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.title.set_text("Delta Band")
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.title.set_text("Theta Band")
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_xticks([])
ax3.set_yticks([])
ax3.title.set_text("Alpha Band")

# set colormap
# cmap = plt.cm.jet
cmap = cm.get_cmap("jet")

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
                    vmax=1, cmap=cm.get_cmap("jet"))
cbar = fig.colorbar(scat1, ax=ax3, ticks=[0, 0.5, 1])
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

    # have to update the data array only after all 3 plots are done
    tempDelta, globalMax, _ = getCmapByFreqVal(data, newdata, -1, globalMax)
    tempTheta, globalMax, _ = getCmapByFreqVal(data, newdata, -2, globalMax)
    tempAlpha, globalMax, data = getCmapByFreqVal(data, newdata, -3, globalMax)

    colorsDelta = cmap(tempDelta)
    colorsTheta = cmap(tempTheta)
    colorsAlpha = cmap(tempAlpha)
    # colors.astype(float)
    # colors[:, -1] = maxes / maxes.max()
    # print(altColors)
    # print(colors)

    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    ax2.set_xlim(-6, 6)
    ax2.set_ylim(-6, 6)
    ax3.set_xlim(-6, 6)
    ax3.set_ylim(-6, 6)

    ax1.scatter(x, y, s=100, c=colorsDelta, cmap=cm.get_cmap("jet"))
    ax2.scatter(x, y, s=100, c=colorsTheta, cmap=cm.get_cmap("jet"))
    ax3.scatter(x, y, s=100, c=colorsAlpha, cmap=cm.get_cmap("jet"))

    elapsed_time = time.time() - start_time
    # print(elapsed_time)


# plot animation

ani = FuncAnimation(fig, plotNodes, interval=100)
# ani.save('visual.mp4', fps=7)
# # save animation (uncomment to record)
# ani.save('EEG_visiualization_LSL.mp4', writer=writer)

plt.get_current_fig_manager().window.wm_geometry("+0+0")
plt.show()
