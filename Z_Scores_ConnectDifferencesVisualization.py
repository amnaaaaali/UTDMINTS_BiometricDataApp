# import necessary functions
import numpy as np
from scipy import stats
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from EEGArray import EEGArray
from Z_Scores_PlotLines import Red_Lines
from Z_Scores_PlotLines import Blue_Lines

# Make a visualization for EEG coherence such that if the difference
# in z-score between 2 electrodes is above 2.3, plot a red line connecting
# those nodes, and if the difference in z-scores is below -2.3 plot a blue
# line connecting the nodes. Connect red lines between electrodes when z-score
# differences > 2.3. Connect blue lines between electrodes when z-score
# differences < -2.3.


# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure
fig = plt.figure()
# create a subplot
ax1 = fig.add_subplot(1, 1, 1)

# define number of electrodes
n = 64

# get node positions
x, y, list = EEGArray()

# initialize data
data = np.zeros(n)

# initialize scatter plot
scat1 = ax1.scatter(x, y)


# define function to plot nodes
def plotNodes(i):
    # define all global variables
    global data

    # Create an inlet
    inlet = StreamInlet(streams[0])
    # Pull data into the inlet
    amplitudes = inlet.pull_sample()

    # Convert the list to a numpy array
    # Here, all of the amplitudes will be stored in a 2-dimensional Numpy
    # array called 'data'
    data = np.asarray(amplitudes[0][:n])

    # Initialize row and column dimensions for the 64 x 64 list
    # initialize row dimension to 64
    i = 64
    # initialize column dimension to 64
    j = 64

    # Create and initialize a 2-dimensional list with zeros to store differences between amplitudes
    differences = [[0] * j for i in range(64)]
    # print(len(differences))

    # Compute the differences between the amplitudes at every given xth, yth position
    for x in range(63):
        for y in range(63):
            # Compute the difference between the amplitudes at every given xth, yth position
            difference = abs(data[x] - data[y])
            # Store the current difference in the differences list at the given xth, yth position
            differences[x][y] = difference
            # print(differences[x][y].shape)

    # Convert the differences list into a (64 x 64)-element Numpy array
    differences_data = np.asarray(differences)

    # Compute the z-score of the differences
    # print("\nZ-Scores Calculation: \n")
    z_scores = np.zeros([64, 64])

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


# create a function animation
ani = FuncAnimation(fig, plotNodes, interval=100)
# show the plot
plt.show()
