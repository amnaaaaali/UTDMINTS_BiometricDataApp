"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
import time
import random
import numpy as np
from scipy import stats

# Create a numpy array of 64 elements
# Computer z-score from the amplitude

# Create an empty list
list = []

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
# streams = resolve_stream('type', 'EEG')
streams = resolve_stream()

print(streams[0].source_id())
# print(streams[1].source_id())

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

i=0
while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    timeCorr = inlet.time_correction()
    print(timestamp, '\n',sample, '\n', timeCorr, '\n')
    # if i==10:
    #     break
    # break
    i = i + 1
    time.sleep(0.01)