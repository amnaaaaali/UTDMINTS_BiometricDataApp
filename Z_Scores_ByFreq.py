# import necessary functions
import numpy as np
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from EEGArray import EEGArray
from GetFrequencyBandOrValue import getFreqBandOrValue
from Z_Scores_PlotLines import Blue_Lines, Red_Lines
from Z_Scores_GetZScores import calculate_z_scores


# Calculate z-scores based on selected band: delta band, theta band, or alpha band

# first resolve an EEG stream on the lab network

print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure. figsize sets the default size of the
fig = plt.figure(figsize=(13, 4))
# ax1 is delta freq, ax2 = theta freq, ax3 = alpha freq
ax1 = fig.add_subplot(1, 3, 1)
# create a title for Delta Band Coherence plot
ax1.title.set_text("Delta Band Coherence (Z-Scores)\n" + "(Frequency Range: 1-3 Hz)")
ax2 = fig.add_subplot(1, 3, 2)
# create a title for Theta Band Coherence plot
ax2.title.set_text("Theta Band Coherence (Z-Scores)\n" + "(Frequency Range: 4-8 Hz)")
ax3 = fig.add_subplot(1, 3, 3)
# create a title for Alpha Band Coherence plot
ax3.title.set_text("Alpha Band Coherence (Z-Scores)\n" + "(Frequency Range: 8-12 Hz)")

# define number of electrodes
n = 64

# get node positions
x, y, list = EEGArray()

# initialize data as a numpy array of zeros (of size n x n)
data = np.zeros((n, n))
# initialize data as a numpy array of zeros (of size n)
new_data = np.zeros(n)

# initialize all 3 scatter plots
# initialize all first scatter plot
scat1 = ax1.scatter(x, y)
# initialize all second scatter plot
scat2 = ax2.scatter(x, y)
# initialize all third scatter plot
scat3 = ax3.scatter(x, y)

# create 2 lines for first plot (ax1)
line1 = ax1.plot(0, 0)
line2 = ax1.plot(0, 0)

# create 2 lines for secon plot (ax2)
line3 = ax2.plot(0, 0)
line4 = ax2.plot(0, 0)

# create 2 lines for third plot (ax3)
line5 = ax3.plot(0, 0, "b-", label="Z-Scores < -2.3")
line6 = ax3.plot(0, 0, "r-", label="Z-Scores > 2.3")

# create a legend and define legend position
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='7')
# make the figure layout tight
fig.tight_layout()

x = 0

# create a global max variable with a value of 5000
globalMax = 5000

# Plot z-scores based on band
# define function to plot nodes
def plotNodes(i):
    # define all global variables
    global data
    global globalMax
    global line1
    global line2
    global line3
    global line4
    global line5
    global line6

    # Create an inlet
    inlet = StreamInlet(streams[0])

    # Pull data into the inlet
    amplitudes = inlet.pull_sample()

    # create a new numpy array called new_data for amplitudes
    new_data = np.asarray(amplitudes[0][:n])

    # get the frequency via delta band or by accessing individual frequencies
    temp, localMax, data = getFreqBandOrValue(data, new_data, -1, globalMax)

    # Calculate z-scores for the delta band
    z_scores1 = calculate_z_scores(temp)

    # get the frequency via theta band or by accessing individual frequencies
    temp, localMax, data = getFreqBandOrValue(data, new_data, -2, globalMax)

    # Calculate z-scores for the theta band
    z_scores2 = calculate_z_scores(temp)

    # get the frequency via alpha band or by accessing individual frequencies
    temp, localMax, data = getFreqBandOrValue(data, new_data, -3, globalMax)

    # Calculate z-scores for the alpha band
    z_scores3 = calculate_z_scores(temp)

    # set the x-axis limits for plot ax1
    ax1.set_xlim(-6, 6)
    # set the y-axis limits for plot ax1
    ax1.set_ylim(-6, 6)

    # set the x-axis limits for plot ax2
    ax2.set_xlim(-6, 6)
    # set the y-axis limits for plot ax2
    ax2.set_ylim(-6, 6)

    # set the x-axis limits for plot ax3
    ax3.set_xlim(-6, 6)
    # set the y-axis limits for plot ax3
    ax3.set_ylim(-6, 6)

    # remove the tick-marks on the axes for ax1
    ax1.tick_params(left=False, bottom=False)
    # remove the tick-marks on the axes for ax2
    ax2.tick_params(left=False, bottom=False)
    # remove the tick-marks on the axes for ax3
    ax3.tick_params(left=False, bottom=False)

    # Plot a red line between electrodes where z-score > 2.3
    # Plot a blue line between electrodes where z-score < -2.3
    # Dimensions of z-scores numpy array is not acceptable in scatter function

    # Partially reset the graph plots ax1, ax2, and ax3 by removing every line
    # after it is plotted.

    # remove every line in ax1
    for line in ax1.lines:
        line.remove()

    # remove every line in ax2
    for line in ax2.lines:
        line.remove()

    # remove every line in ax3
    for line in ax3.lines:
        line.remove()

    # for every pair of electrodes:
    #     - plot a red line where the z-scores of the differences is > 2.3
    #     - plot a blue line where the z-scores of the differences is < -2.3
    for i in range(64):
        for j in range(64):
            if j <= i:
                continue
            # if z-scores is > 2.3, plot a red line on ax1
            if z_scores1[i, j] > 2.3:
                Red_Lines(list[i], list[j], ax1)
            # if z-scores is < -2.3, plot a blu line on ax1
            if z_scores1[i, j] < -2.3:
                Blue_Lines(list[i], list[j], ax1)
            # if z-scores is > 2.3, plot a red line on ax2
            if z_scores2[i, j] > 2.3:
                Red_Lines(list[i], list[j], ax2)
            # if z-scores is < -2.3, plot a blue line on ax2
            if z_scores2[i, j] < -2.3:
                Red_Lines(list[i], list[j], ax3)
            # if z-scores is > 2.3, plot a red line on ax3
            if z_scores3[i, j] > 2.3:
                Blue_Lines(list[i], list[j], ax2)
            # if z-scores is < -2.3, plot blue line on ax3
            if z_scores3[i, j] < -2.3:
                Blue_Lines(list[i], list[j], ax3)
            # else, continue
            else:
                continue


# create an animation function
ani = FuncAnimation(fig, plotNodes, interval=200)
# show the plot
plt.show()
