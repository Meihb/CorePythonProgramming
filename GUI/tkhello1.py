#!/usr/local/bin/python3

import  tkinter

top = tkinter.Tk()
label = tkinter.Label(top,text='Hello World!')
label.pack()

button = tkinter.Button(top,text='Hello World!',command=top.quit)
button.pack()

tkinter.mainloop()