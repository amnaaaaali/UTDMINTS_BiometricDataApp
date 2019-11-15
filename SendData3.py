# CODE TO SEND PREVIOUSLY RECORDED EEG DATA VIA AN LSL DATA OUTLET

# CODE AUTHORED BY: SHAWHIN TALEBI

import time
import csv
from pylsl import StreamInfo, StreamOutlet

# initialize the info for an 64 element LSL EEG outlet
info = StreamInfo('BioSemi', 'EEG', 64, 100, 'float32', 'surface')
# create an outlet from the info
outlet = StreamOutlet(info)

# send data
print("now sending data...")
# open EEGsample.csv
with open('EEGsample.csv') as csvfile:
    # read the .csv file
    readCSV = csv.reader(csvfile, delimiter=',')

    # start forever while loop to stream data
    while True:
        # for every row of data in .csv file
        for row in readCSV:
            # if the row corresponds to the header move to next row
            if row[0] == 'Fp1':
                continue
            # initialize a data list
            data = []
            # for every element in the row convert it from a string to a float
            # and store it in data
            for ele in row:
                data.append(float(ele))
            # send data using the LSL outlet
            outlet.push_sample(data)
            # wait 10 ms
            time.sleep(0.01)
