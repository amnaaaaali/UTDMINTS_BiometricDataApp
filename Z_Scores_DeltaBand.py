# import necessary functions
import numpy as np
from scipy import stats
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from EEGArray import EEGArray
from Z_Scores_PlotLines import Red_Lines
from Z_Scores_PlotLines import Blue_Lines
from GetFrequencyBandOrValue import getFreqBandOrValue

# Repeat red and blue line plots for delta band z-scores.

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# define number of electrodes
n = 64

# get node positions
x, y, list = EEGArray()

# initialize data as a numpy array of zeros (of size n x n)
data = np.zeros((n, n))
# initialize data as a numpy array of zeros (of size n)
new_data = np.zeros(n)

# initialize scatter plot
scat1 = ax1.scatter(x, y)
line1 = ax1.plot(0, 0)
line2 = ax1.plot(0, 0)

x = 0

# create a global max variable with a value of 5000
globalMax = 5000


# define function to plot nodes
def plotNodes(i):
    # define all global variables
    global data
    global globalMax
    global line1
    global line2

    # Create an inlet
    inlet = StreamInlet(streams[0])

    # Pull data into the inlet
    amplitudes = inlet.pull_sample()

    # create a new numpy array called new_data for amplitudes
    new_data = np.asarray(amplitudes[0][:n])

    # get the frequency via delta band or by accessing individual frequencies
    temp, localMax, data = getFreqBandOrValue(data, new_data, 0, globalMax)

    # Initialize row and column dimensions for the 64 x 64 list
    # initialize row dimension to 64
    i = 64
    # initialize column dimension to 64
    j = 64

    # Create and initialize a 2-dimensional list with zeros to store differences between amplitudes
    differences = [[0] * j for i in range(64)]

    # Compute the differences between the amplitudes at every given xth, yth position
    for x in range(63):
        for y in range(63):
            # Compute the difference between the amplitudes at every given xth, yth position
            difference = abs(temp[x] - temp[y])
            # Store the current difference in the differences list at the given xth, yth position
            differences[x][y] = difference

    # Convert the differences list into a (64 x 64)-element Numpy array
    differences_data = np.asarray(differences)
    # print the shape/size of the differences_data array
    print(np.shape(differences_data))

    # Compute the z-score of the differences
    z_scores = np.zeros([64, 64])
    # print the shape/size of the z-scores array
    print(np.shape(z_scores))

    # calculate the z-scores for each row and column in the differences_data array
    for i in range(63):
        # calculate the z-scores
        z_scores[:n][i] = stats.zscore(differences_data[:n][i])
        # print the z-scores
        print(z_scores[:n][i])

    # set the x-axis limits for plot ax1
    ax1.set_xlim(-6, 6)
    # set the y-axis limits for plot ax1
    ax1.set_ylim(-6, 6)

    # Plot z-scores of differences in amplitudes
    ax1.scatter(x, y)

    # Plot a red line between electrodes where z-score > 2.3
    # Plot a blue line between electrodes where z-score < -2.3
    # Dimensions of z-scores numpy array is not acceptable in scatter function

    # remove every line in ax1
    for line in ax1.lines:
        line.remove()

    # for every pair of electrodes:
    #     - plot a red line where the z-scores of the differences is > 2.3
    #     - plot a blue line where the z-scores of the differences is < -2.3
    for i in range(64):
        for j in range(64):
            if j <= i:
                continue
            # if z-scores is > 2.3, plot a red line on ax1
            if z_scores[i, j] > 2.3:
                Red_Lines(list[i], list[j], ax1)
            # if z-scores is < -2.3, plot a blue line on ax1
            elif z_scores[i, j] < -2.3:
                Blue_Lines(list[i], list[j], ax1)
            # else, continue
            else:
                continue


# create an animation funsction
ani = FuncAnimation(fig, plotNodes, interval=200)
# show the plot
plt.show()
