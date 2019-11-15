# import necessary functions
import numpy as np
from scipy import stats

# create a constant for the 64 electrodes
n = 64


# define a function to calculate the z-scores
def calculate_z_scores(temp):

    # Initialize row and column dimensions for the 64 x 64 list
    # initialize row dimension to 64
    i = 64
    # initialize column dimension to 64
    j = 64

    # Create and initialize a 2-dimensional list with zeros to store differences between amplitudes
    differences = [[0] * j for i in range(64)]

    # Compute the differences between the amplitudes at every given xth, yth position
    for x in range(63):
        for y in range(63):
            # Compute the difference between the amplitudes at every given xth, yth position
            difference = abs(temp[x] - temp[y])
            # Store the current difference in the differences list at the given xth, yth position
            differences[x][y] = difference

    # Convert the differences list into a (64 x 64)-element Numpy array
    differences_data = np.asarray(differences)
    # print the shape/size of the differences_data array
    print(np.shape(differences_data))

    # Compute the z-score of the differences
    z_scores = np.zeros([64, 64])
    # print the shape/size of the z-scores array
    print(np.shape(z_scores))

    # calculate the z-scores for each row and column in the differences_data array
    for i in range(63):
        # calculate the z-scores
        z_scores[:n][i] = stats.zscore(differences_data[:n][i])
        # print the z-scores
        print(z_scores[:n][i])

    # return z-cores
    return z_scores
