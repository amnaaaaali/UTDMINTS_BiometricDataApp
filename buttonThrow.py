from tkinter import *
from tkinter import ttk
from functools import partial

root = Tk()
root.title('test')
root.resizable(False, False)
root.geometry('800x400')
root.columnconfigure(0, weight=1)   # Which column should expand with window
root.rowconfigure(0, weight=1)      # Which row should expand with window

items = [{'name' : '1', 'text' : '0000', 'x': 0, 'y': 0},
         {'name' : '2', 'text' : '0020', 'x': 55, 'y': 150},
         {'name' : '3', 'text' : '0040', 'x': 600, 'y': 200}]

canvas = Canvas(root, bg='khaki')   # To see where canvas is
canvas.grid(sticky=NSEW)

for item in items:
    widget = ttk.Button(root, text=item['text'],
                        command=partial(print,item['text']))
    # Place widget on canvas with: create_window
    canvas.create_window(item['x'], item['y'], anchor=NW, 
                         height=25, width=70, window=widget)

root.mainloop()
