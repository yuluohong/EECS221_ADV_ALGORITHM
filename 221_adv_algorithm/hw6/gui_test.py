#!/usr/bin/env python
# coding:utf-8


import numpy as np
from Tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ----------------------------------------------------------------------



def drawPic():
    try:
        sampleCount = int(inputEntry.get())
    except:
        sampleCount = 50
        print 'interger'
        inputEntry.delete(0, END)
        inputEntry.insert(0, '50')
    drawPic.f.clf()
    drawPic.a = drawPic.f.add_subplot(111)

    x=[0,0,1,2,3,4,5,6,6]
    y=[1,2,2,2,2,2,2,2,3]
    color = ['b', 'r', 'y', 'g']
    drawPic.a.scatter(x, y, s=3, color=color[np.random.randint(len(color))])

    drawPic.a.set_title('The Optimal Path')
    drawPic.canvas.show()


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    root = Tk()

    drawPic.f = Figure(figsize=(5, 4), dpi=100)
    drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
    drawPic.canvas.show()
    drawPic.canvas.get_tk_widget().grid(row=0, columnspan=3)

    Label(root, text='Please input the order ID：').grid(row=1, column=0)
    inputEntry = Entry(root)
    inputEntry.grid(row=1, column=1)
    inputEntry.insert(0, '1')
    Button(root, text='Find', command=drawPic).grid(row=1, column=2, columnspan=3)

    root.mainloop()
