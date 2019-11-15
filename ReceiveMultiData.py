# CODE TO READ MULTIPLE DATA STREAMS USING pylsl

# CODE AUTHORED BY: SHAWHIN TALEBI

from pylsl import StreamInlet, resolve_stream
import time

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
# streams = resolve_stream('type', 'EEG')
streams = resolve_stream()

print(streams[0].source_id())
print(streams[1].source_id())

# create a new inlet to read from the stream
inlet1 = StreamInlet(streams[0])
inlet2 = StreamInlet(streams[1])

i=0
while True:
    # get a 1st new sample
    sample1, timestamp1 = inlet1.pull_sample()
    timeCorr1 = inlet1.time_correction()
    # print(timestamp1, '\n',sample1, '\n', timeCorr1, '\n', timestamp1+timeCorr1, '\n')
    print(timestamp1+timeCorr1, '\n')

    # get a 2nd new sample
    sample2, timestamp2 = inlet2.pull_sample()
    timeCorr2 = inlet2.time_correction()
    # print(timestamp2, '\n',sample2, '\n', timeCorr2, '\n',timestamp2+timeCorr2, '\n')
    # time.sleep(0.01)
    print(timestamp2+timeCorr2, '\n')

    if i==10:
        break
    # break
    i = i + 1
    time.sleep(0.01)
