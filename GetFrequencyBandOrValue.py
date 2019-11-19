# import necessary functions
import numpy as np
from SelectFrequency import getAmplitudesByFrequencyBand
import scipy.signal as sps


# function that gets the frequency based on either the frequency band or the
# individual frequency value
def getFreqBandOrValue(data, new_data, freq_value, global_max):
    # delete first row
    data = np.delete(data, 0, 0)

    # add new_data as a row at the end of data. columns=electrodes rows=timestep
    data = np.vstack([data, new_data])
    # transpose the data numpy array
    data = np.transpose(data)

    # compute power spectrum of data
    f, ps = sps.welch(data, fs=26)
    # print the power spectrum
    print("ps", ps)
    # print the frequency
    print("f", f)

    extract_amplitude = []
    # delta freq band
    if freq_value == -1:
        extract_amplitude = getAmplitudesByFrequencyBand(ps, 0)
    # theta freq band
    elif freq_value == -2:
        extract_amplitude = getAmplitudesByFrequencyBand(ps, 1)
    # alpha freq band
    elif freq_value == -3:
        extract_amplitude = getAmplitudesByFrequencyBand(ps, 2)
    # specific freq value wanted
    else:
        interval = [freq_value - 0.5, freq_value + 0.5]
        start_index = -1
        end_index = -1
        for i in range(len(f)):
            if interval[0] <= f[i] <= interval[1]:
                if start_index == -1:
                    start_index = i
                else:
                    end_index = i

        print("start ", start_index, f[start_index],
              "end ", end_index, f[end_index])
        extract_amplitude = ps[:, start_index:end_index]
    # create a numpy array called temp
    temp = np.asarray(extract_amplitude)

    # temp holds mean of each row in extractAmplitude
    temp = np.mean(temp, axis=1)
    # calculate the maximum of the two values - called local_max
    local_max = max(np.amax(temp), global_max)

    # traverse through elements in the temp nuumpy array
    for i in range(len(temp)):
        # normalize all amplitudes by the global max
        temp[i] = temp[i] / local_max
    # return the temp, local_max, and data numpy arrays
    return [temp, local_max, data]

