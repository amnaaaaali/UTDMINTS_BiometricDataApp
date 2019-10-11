from tkinter import *
from tkinter import ttk
from functools import partial
import subprocess

WINDOW_SIZE="800x400"

top = Tk()
top.geometry(WINDOW_SIZE)
top.resizable(False,False)
top.title('UTD MINTS')
top.columnconfigure(0, weight=1)   # Which column should expand with window
top.rowconfigure(0, weight=1)

canvas = Canvas(top,bg="black")
canvas.grid(sticky=NSEW)


def deltaZscores():
   print ("Below is the output from the shell script in terminal")
   subprocess.call('./testrun.sh', shell=True)

def delta():
   print ("Below is the output from the shell script in terminal")
   subprocess.call('./deltaOnly.sh', shell=True)

def Zscores():
   print ("Below is the output from the shell script in terminal")
   subprocess.call('./zscoreOnly.sh', shell=True)


B = ttk.Button(top, text ="Delta & Z Scores", command = deltaZscores)
canvas.create_window(0,0, anchor=NW, height=50,width=100,window=B)

C = ttk.Button(top, text ="Delta Only", command = delta)
canvas.create_window(55,150, anchor=NW, height=50,width=100,window=C)

D = ttk.Button(top, text ="Z Scores", command = Zscores)
canvas.create_window(600,200, anchor=NW, height=50,width=100,window=D)

#B.pack()
#C.pack()
#D.pack()
top.mainloop()
