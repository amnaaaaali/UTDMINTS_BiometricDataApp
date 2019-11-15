# import necessary functions
from pylsl import StreamInlet, resolve_stream
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

# create figure. figsize sets the default size of the
fig = plt.figure(figsize=(13, 4))
# ax1 is delta freq, ax2 = theta freq, ax3 = alpha freq
ax1 = fig.add_subplot(2, 7, 1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.title.set_text("1 Hz")
ax2 = fig.add_subplot(2, 7, 2)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.title.set_text("2 Hz")
ax3 = fig.add_subplot(2, 7, 3)
ax3.set_xticks([])
ax3.set_yticks([])
ax3.title.set_text("3 Hz")
ax4 = fig.add_subplot(2, 7, 4)
ax4.set_xticks([])
ax4.set_yticks([])
ax4.title.set_text("4 Hz")
ax5 = fig.add_subplot(2, 7, 5)
ax5.set_xticks([])
ax5.set_yticks([])
ax5.title.set_text("5 Hz")
ax6 = fig.add_subplot(2, 7, 6)
ax6.set_xticks([])
ax6.set_yticks([])
ax6.title.set_text("6 Hz")
ax7 = fig.add_subplot(2, 7, 7)
ax7.set_xticks([])
ax7.set_yticks([])
ax7.title.set_text("7 Hz")
ax8 = fig.add_subplot(2, 7, 8)
ax8.set_xticks([])
ax8.set_yticks([])
ax8.title.set_text("8 Hz")
ax9 = fig.add_subplot(2, 7, 9)
ax9.set_xticks([])
ax9.set_yticks([])
ax9.title.set_text("9 Hz")
ax10 = fig.add_subplot(2, 7, 10)
ax10.set_xticks([])
ax10.set_yticks([])
ax10.title.set_text("10 Hz")
ax11 = fig.add_subplot(2, 7, 11)
ax11.set_xticks([])
ax11.set_yticks([])
ax11.title.set_text("11 Hz")
ax12 = fig.add_subplot(2, 7, 12)
ax12.set_xticks([])
ax12.set_yticks([])
ax12.title.set_text("12 Hz")
ax13 = fig.add_subplot(2, 7, 13)
ax13.set_xticks([])
ax13.set_yticks([])
ax13.title.set_text("13 Hz")
# set colormap
# cmap = plt.cm.jet
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
scat1 = ax1.scatter(x, y, s=100, c=newdata, vmin=0,
                    vmax=1, cmap=cm.get_cmap("jet"))
cbar = fig.colorbar(scat1, ticks=[0, 0.5, 1])
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
    temp1, globalMax, _ = getCmapByFreqVal(data, newdata, 1, globalMax)
    temp2, globalMax, _ = getCmapByFreqVal(data, newdata, 2, globalMax)
    temp3, globalMax, _ = getCmapByFreqVal(data, newdata, 3, globalMax)
    temp4, globalMax, _ = getCmapByFreqVal(data, newdata, 4, globalMax)
    temp5, globalMax, _ = getCmapByFreqVal(data, newdata, 5, globalMax)
    temp6, globalMax, _ = getCmapByFreqVal(data, newdata, 6, globalMax)
    temp7, globalMax, _ = getCmapByFreqVal(data, newdata, 7, globalMax)
    temp8, globalMax, _ = getCmapByFreqVal(data, newdata, 8, globalMax)
    temp9, globalMax, _ = getCmapByFreqVal(data, newdata, 9, globalMax)
    temp10, globalMax, _ = getCmapByFreqVal(data, newdata, 10, globalMax)
    temp11, globalMax, _ = getCmapByFreqVal(data, newdata, 11, globalMax)
    temp12, globalMax, _ = getCmapByFreqVal(data, newdata, 12, globalMax)
    temp13, globalMax, data = getCmapByFreqVal(data, newdata, 13, globalMax)

    colors1, colors2, colors3, colors4, colors5, colors6, colors7, colors8, colors9, colors10, colors11, colors12, colors13 = cmap(temp1), cmap(temp2), cmap(
        temp3), cmap(temp4), cmap(temp5), cmap(temp6), cmap(temp7), cmap(temp8), cmap(temp9), cmap(temp10), cmap(temp11), cmap(temp12), cmap(temp13)
    # colors.astype(float)
    # colors[:, -1] = maxes / maxes.max()
    # print(altColors)
    # print(colors)

    # ax1.set_xlim(-6, 6)
    # ax1.set_ylim(-6, 6)
    # ax2.set_xlim(-6, 6)
    # ax2.set_ylim(-6, 6)
    # ax3.set_xlim(-6, 6)
    # ax3.set_ylim(-6, 6)

    ax1.scatter(x, y, s=100, c=colors1, cmap=cm.get_cmap("jet"))
    ax2.scatter(x, y, s=100, c=colors2, cmap=cm.get_cmap("jet"))
    ax3.scatter(x, y, s=100, c=colors3, cmap=cm.get_cmap("jet"))
    ax4.scatter(x, y, s=100, c=colors4, cmap=cm.get_cmap("jet"))
    ax5.scatter(x, y, s=100, c=colors5, cmap=cm.get_cmap("jet"))
    ax6.scatter(x, y, s=100, c=colors6, cmap=cm.get_cmap("jet"))
    ax7.scatter(x, y, s=100, c=colors7, cmap=cm.get_cmap("jet"))
    ax8.scatter(x, y, s=100, c=colors8, cmap=cm.get_cmap("jet"))
    ax9.scatter(x, y, s=100, c=colors9, cmap=cm.get_cmap("jet"))
    ax10.scatter(x, y, s=100, c=colors10, cmap=cm.get_cmap("jet"))
    ax11.scatter(x, y, s=100, c=colors11, cmap=cm.get_cmap("jet"))
    ax12.scatter(x, y, s=100, c=colors12, cmap=cm.get_cmap("jet"))
    ax13.scatter(x, y, s=100, c=colors13, cmap=cm.get_cmap("jet"))

    elapsed_time = time.time() - start_time
    # print(elapsed_time)


# plot animation

ani = FuncAnimation(fig, plotNodes, interval=100)
# ani.save('visual.mp4', fps=7)
# # save animation (uncomment to record)
# ani.save('EEG_visiualization_LSL.mp4', writer=writer)

plt.show()
