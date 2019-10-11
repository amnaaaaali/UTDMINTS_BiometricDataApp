import numpy as np
import math
from SelectFrequency import getAmplitudesByFrequencyBand
from SelectFrequency import getAmplitudeByFreqIndex
import scipy.signal as sps

# takes in the data from EEG, and calls the fourier transform
# and processes it so it can be passed into the plot/cmap


def getCmapByFreqBand(data, newdata, freq, globalMax):
    # delete first row
    data = np.delete(data, 0, 0)

    # add newdata as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, newdata])
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    print("ps", ps)
    print("f", f)

    # get the amplitudes associated with the delta frequencies
    extractAmplitude = getAmplitudesByFrequencyBand(ps, freq)
    temp = np.asarray(extractAmplitude)

 # temp holds mean of each row in extractAmplitude
    temp = np.mean(temp, axis=1)
    localMax = max(np.amax(temp), globalMax)

    for i in range(len(temp)):
        # normalize all amplitudes by the global max
        temp[i] = temp[i] / localMax
    return [temp, localMax, data]


def getCmapByFreqVal(data, newdata, freqIndex):
    # delete first row
    data = np.delete(data, 0, 0)

    # add newdata as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, newdata])
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    print("ps", ps)
    print("f", f)

    # get the amplitudes associated with the delta frequencies
    extractAmplitude = getAmplitudeByFreqIndex(ps, freqIndex)
    print("EA", extractAmplitude, freqIndex)
    return extractAmplitude
