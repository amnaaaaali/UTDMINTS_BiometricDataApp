# import necessary functions
import numpy as np
from scipy import stats
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from EEGArray import EEGArray

# Write code to visualize amplitudes of the EEG electrodes in terms of their z-score.
# Have a color bar for the z-score of each element
# For every element in the array, calculate the difference in the z-scores compared to
# every other element in the array.

# Create an inlet
# Pull data into the inlet
# Convert data to numpy array
# Compute z-scores

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create figure
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# define number of electrodes
n = 64
# define node positions
x, y = EEGArray()

# initialize data
data = np.zeros(n)

# initialize scatter plot
scat1 = ax1.scatter(x, y, c=data, s=100, cmap=plt.cm.RdYlGn, vmin=-7, vmax=7)
cbar = fig.colorbar(scat1, ax=ax1)


# define function to plot nodes
def plotNodes(i):
    global data

    # Create an inlet
    # start_time = time.time()
    inlet = StreamInlet(streams[0])
    # Pull data into the inlet
    amplitudes = inlet.pull_sample()

    # Convert the list to a numpy array
    data = np.asarray(amplitudes[0][:n])

    # Compute the z-score of each amplitude
    z_scores = stats.zscore(data)

    # pos_data = data > 0
    # neg_data = pos_data + (-1) * np.ones(len(pos_data))
    # print(PosData+NegData)
    # print(data)
    # print("pos neg data...")
    # print(np.log(abs(data)) * (pos_data + neg_data))

    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    # Plots amplitudes
    # ax1.scatter(x, y, c = data, s = 100, cmap = plt.cm.RdBu_r, vmin=-10000,vmax=10000)
    ax1.scatter(x, y, c=z_scores, s=100, cmap=plt.cm.RdYlGn, vmin=-7, vmax=7)
    cbar.ax.set_ylabel('Z-Scores', rotation=90)

    print(z_scores)


ani = FuncAnimation(fig, plotNodes, interval=100)
plt.show()
