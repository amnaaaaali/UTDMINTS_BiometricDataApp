Files:

AlphaFrequencies.py, DeltaFrequencies.py, ThetaFrequencies.py
------------
Each file shows each of the different Alpha, Delta, and Theta bands' EEG plots in
seperate plots


MultiFrequencies.py
------------
All 3 frequency bands, Alpha, Delta and Theta bands' plots are shown in one figure
in this file. 


MultiZscore.py
------------
All 3 frequency bands are shown with their Zscores plotted instead of the powers as with
the other Files


GetCmapValues.py
------------

getCmapByFreqVal: For a given frequency value, the function calls the fourier transform on the current
sample of data and computes the cmap value for that sample of data based on the power value??
getCmapForZscores: Exactly the same as getCmapByFreqVal but computes the zscore value and uses
that in the cmap



