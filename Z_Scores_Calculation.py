# import necessary functions
import random
from scipy import stats
import numpy as np

# Create a numpy array of 64 elements
# Computer z-score from the amplitude

# Create an empty list
list = []

# Initialize the value of each of the 64 elements in the
# list to a number between -5,000 and 5,000
for index in range(64):
    # Append a new random integer in the range (-5,000 , 5,000) to the list
    list.append(random.randrange(-5000, 5000))

# Convert the list to a numpy array
print("64-Element Numpy Array: \n")
# convert the list to a numpy array
numpy_array = np.asarray(list)
# print the numpy array
print(numpy_array)

# Compute the z-score of each amplitude
print("Z-Scores Calculation: \n")
z_scores = stats.zscore(numpy_array)
# print the z-scores
print(z_scores)
