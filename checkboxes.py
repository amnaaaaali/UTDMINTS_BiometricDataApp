from tkinter import *
from tkinter import ttk
from functools import partial
import subprocess

WINDOW_SIZE="800x400"

top = Tk()
top.title('UTD MINTS')

DeltaFreq = ttk.Checkbutton(top, text="Delta Freq")
DeltaFreq.grid(column=0, row=0)
DeltaFreq.state(['!alternate'])

ThetaFreq = ttk.Checkbutton(top, text="Theta freq")
ThetaFreq.grid(column=2, row=0)
ThetaFreq.state(['!alternate'])

AlphaFreq = ttk.Checkbutton(top, text="Alpha Freq")
AlphaFreq.grid(column=4, row=0)
AlphaFreq.state(['!alternate'])

DeltaZ = ttk.Checkbutton(top, text="Delta Z score Freq")
DeltaZ.grid(column=6, row=0)
DeltaZ.state(['!alternate'])

ThetaZ = ttk.Checkbutton(top, text="Theta Z score freq")
ThetaZ.grid(column= 0, row=2)
ThetaZ.state(['!alternate'])

AlphaZ = ttk.Checkbutton(top, text="Alpha Z score freq")
AlphaZ.grid(column=2, row=2)
AlphaZ.state(['!alternate'])

RelativePow = ttk.Checkbutton(top, text="Relative Power")
RelativePow.grid(column=4, row=2)
RelativePow.state(['!alternate'])

RelativeZ = ttk.Checkbutton(top, text="Relative Z score")
RelativeZ.grid(column=6, row=2)
RelativeZ.state(['!alternate'])


def callback():
   file_object = open('runScripts.sh', 'r+')
   file_object.write("#!/bin/bash\n")
   file_object.write("python SendData2.py &\n")
   # print (file_object)
   if (DeltaFreq.state() == ('selected',)):
      print ("DeltaFreq")
      file_object.write("python DeltaFrequencies.py &\n")

   if (ThetaFreq.state() == ('selected',)):
      print ("ThetaFreq")
      file_object.write("python Z_Scores_Visualization.py &\n")

   if (AlphaFreq.state() == ('selected',)):
      print ("AlphaFreq")
   if (DeltaZ.state() == ('selected',)):
      print ("DeltaZ")
   if (ThetaZ.state() == ('selected',)):
      print ("ThetaZ")
   if (AlphaZ.state() == ('selected',)):
      print ("AlphaZ")
   if (RelativePow.state() == ('selected',)):
      print ("RelativePow")
   if (RelativeZ.state() == ('selected',)):
      print ("RelativeZ")
   rc = subprocess.call(['chmod', '754', 'runScripts.sh'])
   tc = subprocess.call("./runScripts.sh")
   print("hello")


# print (file_object)

b = Button(top, text="RUN", command=callback, height=2, width=5)
b.grid(row = 40, column = 5)


print ("done")

top.mainloop()
