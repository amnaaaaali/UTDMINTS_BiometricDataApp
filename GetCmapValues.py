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


def getCmapByFreqVal(data, newdata, freqValue, globalMax):
    # delete first row
    data = np.delete(data, 0, 0)

    # add newdata as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, newdata])
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    print("ps", ps)
    print("f", f)

    extractAmplitude = []
    # delta freq band
    if(freqValue == -1):
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 0)
    elif freqValue == -2:
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 1)
    elif freqValue == -3:
        extractAmplitude = getAmplitudesByFrequencyBand(ps, 2)
    else:
        interval = [freqValue - 0.5, freqValue + 0.5]
        startIndex = -1
        endIndex = -1
        for i in range(len(f)):
            if interval[0] <= f[i] <= interval[1]:
                if startIndex == -1:
                    startIndex = i
                else:
                    endIndex = i

        print("start ", startIndex, f[startIndex],
              "end ", endIndex, f[endIndex])
        extractAmplitude = ps[:, startIndex:endIndex]

    temp = np.asarray(extractAmplitude)

    # temp holds mean of each row in extractAmplitude
    temp = np.mean(temp, axis=1)
    localMax = max(np.amax(temp), globalMax)

    for i in range(len(temp)):
        # normalize all amplitudes by the global max
        temp[i] = temp[i] / localMax
    return [temp, localMax, data]
