def getAmplitudesByFrequencyBand(ps, x):
    # if delta freq wanted
    if x == 0:
        return ps[:, 3:9]
    # if theta freq wanted
    elif x == 1:
        return ps[:, 10:19]
    # if alpha freq wanted
    elif x == 2:
        return ps[:, 20:29]


def getAmplitudeByFreqIndex(ps, x):
    return ps[: x]
