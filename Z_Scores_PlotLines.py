import matplotlib.pyplot as plt
import numpy as np
from EEGArray import EEGArray


# Create a method to plot red lines
def Red_Lines(e1, e2, ax):
    # define properties of red line
    line1,  = ax.plot(np.linspace(e1[0], e2[0], 5), np.linspace(e1[1], e2[1], 5), 'r-')
    # return line1
    return line1


# Create a method to plot blue lines
def Blue_Lines(e1, e2, ax):
    # define properties of blue line
    line2, = ax.plot(np.linspace(e1[0], e2[0], 5), np.linspace(e1[1], e2[1], 5), 'b-')
    # return line2
    return line2
