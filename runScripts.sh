#/bin/bash
sh runSendData.sh &
python MultiFrequencies.py &
python Z_Scores_ByFreq.py &
sh videoBash.sh &
