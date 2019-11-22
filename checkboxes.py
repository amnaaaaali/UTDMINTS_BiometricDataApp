import os
from tkinter import *
from tkinter import ttk
from functools import partial
import subprocess

WINDOW_SIZE = "800x400"

top = Tk()
top.title('UTD MINTS')

MultiFreq = ttk.Checkbutton(top, text="Multi Frequencies")
MultiFreq.grid(column=0, row=0)
MultiFreq.state(['!alternate'])

MultiZscore = ttk.Checkbutton(top, text="Multi Zscores")
MultiZscore.grid(column=4, row=0)
MultiZscore.state(['!alternate'])

ZscoreFreq = ttk.Checkbutton(top, text="Z-scores By Frequency")
ZscoreFreq.grid(column=8, row=0)
ZscoreFreq.state(['!alternate'])

video = ttk.Checkbutton(top, text="Gaze Video Livestream")
video.grid(column=12, row=0)
video.state(['!alternate'])


def checkIfSelected(state):
    if(state == ('selected',) or state == ('focus', 'selected')):
        return True
    return False


def callback():
    if os.path.exists("runScripts.sh"):
        os.remove("runScripts.sh")
    file_object = open('runScripts.sh', 'w+')
    file_object.write("#/bin/bash\n")
    file_object.write("sh runSendData.sh &\n")
    # print (file_object)
    if (checkIfSelected(MultiFreq.state())):
        print("MultiFreq")
        file_object.write("python MultiFrequencies.py &\n")

    if (checkIfSelected(ZscoreFreq.state())):
        print("ZscoreFreq")
        file_object.write("python Z_Scores_ByFreq.py &\n")

    if (checkIfSelected(video.state())):
        print("video")
        file_object.write("sh videoBash.sh &\n")

    if (checkIfSelected(MultiZscore.state())):
        print("MultiZscore")
        file_object.write("python MultiZscore.py &\n")
        print("Mai hi land hun")

    file_object.close()
    subprocess.call("sh runScripts.sh", shell=True)


b = Button(top, text="RUN", command=callback, height=2, width=5)
b.grid(row=40, column=5)

top.mainloop()
sys.exit()
