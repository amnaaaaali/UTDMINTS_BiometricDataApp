# import necessary functions
import random
from scipy import stats
import numpy as np


# Create a numpy array of 64 elements
# Computer z-score from the amplitude

# ORIGINAL OBJECTIVE:
# Then, write code to compute the difference in z-score between every possible pair of
# electrodes (i.e. 4092 differences!). This can be stored in a 64 by 64 array where
# the i,jth element is the difference between the z-scores of the ith and jth electrode.
# Note: only 2016 unique differences need to be computed since the difference of an
# electrode's z-score with itself is 0, and the difference between the ith and jth
# electrodes should be the same as the jth and ith electrodes.

###########################################################################################

# MODIFIED OBJECTIVE:
# Calculate the ***z-scores of the differences***, NOT ***the differences of the z-scores***.

###########################################################################################

# Create an empty list
list = []

# Initialize the value of each of the 64 elements in the list to a number between -5,000 and 5,000
for index in range(64):
    list.append(random.randrange(-5000, 5000))

# Convert the list to a numpy array
print("64-Element Numpy Array: \n")
numpy_array = np.asarray(list)
print(numpy_array)

# Initialize row and column dimensions for the 64 x 64 list
i = 64
j = 64

# Create and initialize a 2-dimensional list with zeros to store differences between z-scores
differences = [[0] * j for i in range(64)]

# Compute the z-scores of the differences
print("\nDifferences of the Z-Scores: \n")
for x in range(64):
    for y in range(64):
        # Compute the difference between the z-scores at a given xth, yth position
        difference = abs(numpy_array[x] - numpy_array[y])
        # Store the current difference in the differences list at the given xth, yth position
        differences[x][y] = difference
        # print(differences[x][y].shape)

# Convert the differences list into a (64 x 64)-element Numpy array
differences_numpy_array = np.reshape(differences, (64*64, 1))
# print(differences_numpy_array.shape)

# Compute the z-score of each amplitude
print("\nZ-Scores Calculation: \n")
z_scores = stats.zscore(differences_numpy_array)
# Convert the z-scores array into a (64 x 64)-element Numpy array
z_scores = np.reshape(z_scores, (64, 64))
print(z_scores)

print("\nDimension of Numpy Array of Differences: ")
dimensions = np.shape(differences_numpy_array)
print(dimensions)
