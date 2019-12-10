#!/bin/bash
#created a local variable 'a' and set the path for the python that the Tobii video streaming uses.
#This can be changed in the future depending on the OS as needed.
#we just reference the a variable and use it as a command to run the tobii_gui python file. 
a='C:/msys64/mingw64/bin/python.exe'
$a tobii_gui.py
