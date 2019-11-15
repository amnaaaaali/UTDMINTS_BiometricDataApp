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
from SelectFrequency import getAmplitudesByFrequencyBand
import scipy.signal as sps
from scipy import stats
# import http.server as server
import socketserver


# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure. figsize sets the default size of the
fig = plt.figure(figsize=(13, 4))
# ax1 is delta freq, ax2 = theta freq, ax3 = alpha freq
ax1 = fig.add_subplot(1, 3, 1)
ax1.title.set_text("Delta Band")
ax1.set_xticks([])
ax1.set_yticks([])
ax2 = fig.add_subplot(1, 3, 2)
ax2.title.set_text("Theta Band")
ax2.set_xticks([])
ax2.set_yticks([])
ax3 = fig.add_subplot(1, 3, 3)
ax3.title.set_text("Alpha Band")
ax3.set_xticks([])
ax3.set_yticks([])
# set colormap
cmap = plt.cm.seismic

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
                    vmax=1, cmap=plt.cm.seismic_r)
cbar = fig.colorbar(scat1, ax=[ax1, ax2, ax3], ticks=[0, 0.5, 1])
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

    # delete first row of data
    data = np.delete(data, 0, 0)

    # add newdata as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, newdata])
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    print("ps", ps)

# get the amplitudes associated with the various bands of frequencies
    extractAmplitudeDelta = getAmplitudesByFrequencyBand(ps, 0)
    extractAmplitudeTheta = getAmplitudesByFrequencyBand(ps, 1)
    extractAmplitudeAlpha = getAmplitudesByFrequencyBand(ps, 2)
    tempDelta = np.asarray(extractAmplitudeDelta)
    tempTheta = np.asarray(extractAmplitudeTheta)
    tempAlpha = np.asarray(extractAmplitudeAlpha)

    # temp holds mean of each row in extractAmplitude
    tempDelta = np.mean(tempDelta, axis=1)
    tempTheta = np.mean(tempTheta, axis=1)
    tempAlpha = np.mean(tempAlpha, axis=1)

    # square all values to make them 0 <= x <= 1
    tempDelta = np.square(tempDelta)
    tempTheta = np.square(tempTheta)
    tempAlpha = np.square(tempAlpha)

    # calculate zscores for the array
    zscoreArrayDelta = stats.zscore(tempDelta)
    zscoreArrayTheta = stats.zscore(tempTheta)
    zscoreArrayAlpha = stats.zscore(tempAlpha)
# do relative here
    # next line creates positive and negative zscores, so if the value was between 0 to 0.5, it is
    # scaled to between -1 and 0, and if the value was between 0.5 and 1, it is scaled to between
    # 0 and 1
    zscoreArrayDelta = (
        (zscoreArrayDelta / np.amax(zscoreArrayDelta)) / 2) + 0.5
    zscoreArrayTheta = (
        (zscoreArrayTheta / np.amax(zscoreArrayTheta)) / 2) + 0.5
    zscoreArrayAlpha = (
        (zscoreArrayAlpha / np.amax(zscoreArrayAlpha)) / 2) + 0.5

    # define vectors for plot colors and opacity
    # altColors = freqs / 33
    colorsDelta = cmap(zscoreArrayDelta)
    colorsTheta = cmap(zscoreArrayTheta)
    colorsAlpha = cmap(zscoreArrayAlpha)

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
    # ax1.scatter(x, y, s = 100, c = altColors, cmap = plt.cm.jet_r)
    ax1.scatter(x, y, s=100, c=colorsDelta)
    ax2.scatter(x, y, s=100, c=colorsTheta)
    ax3.scatter(x, y, s=100, c=colorsAlpha)

    elapsed_time = time.time() - start_time


# print(elapsed_time)

# plot animation
ani = FuncAnimation(fig, plotNodes, interval=100)
# ani.save('visual.mp4', fps=7)3
# # save animation (uncomment to record)
# ani.save('EEG_visiualization_LSL.mp4', writer=writer)

plt.show()
