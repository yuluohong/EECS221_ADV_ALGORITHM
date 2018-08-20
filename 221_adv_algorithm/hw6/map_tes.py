#!/usr/bin/env python
# coding:utf-8

import numpy as np
from Tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
all_x=[]
all_y=[]

def map_single_order(x_now,y_now,x_next,y_next):
    global all_x
    global all_y
    map_x=[]
    map_y=[]
    if (y_now < y_next):
        if (y_now % 2 != 0):
            y_now = y_now + 1
            map_y.append(y_now)
            map_x.append(x_now)
        if(x_now<x_next):
            while(x_now<x_next-1):
                x_now=x_now+1
                map_y.append(y_now)
                map_x.append(x_now)
            while(y_now<y_next):
                y_now=y_now+1
                map_y.append(y_now)
                map_x.append(x_now)
        elif (x_now > x_next):
            while (x_now > x_next + 1):
                x_now = x_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
            while (y_now < y_next):
                y_now=y_now+1
                map_y.append(y_now)
                map_x.append(x_now)
        else:
            while(y_now<y_next):
                y_now=y_now+1
                map_y.append(y_now)
                map_x.append(x_now)
    else:
        if (y_now % 2 != 0):
            y_now = y_now - 1
            map_y.append(y_now)
            map_x.append(x_now)
        if (x_now < x_next):
            while (x_now < x_next - 1):
                x_now = x_now + 1
                map_y.append(y_now)
                map_x.append(x_now)
            while (y_next < y_now):
                y_now=y_now-1
                map_y.append(y_now)
                map_x.append(x_now)
        elif (x_now > x_next):
            while (x_now > x_next + 1):
                x_now = x_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
            while (y_now > y_next):
                y_now=y_now-1
                map_y.append(y_now)
                map_x.append(x_now)
        else:
            while (y_now > y_next):
                y_now=y_now-1
                map_y.append(y_now)
                map_x.append(x_now)

    for i in range(len(map_x)):
        print(map_x[i],map_y[i])
    print 'end'
    # all_x=all_x+map_x
    # all_y=all_y+map_y
    all_x.append(map_x)
    all_y.append(map_y)
    return x_now,y_now


def map_to_point(path,x_start=0, y_start=0, x_end=0, y_end=0):
    index=[]
    # x_obj=[3,7]
    # y_obj=[3,9]
    x_obj = [ 3, 7, 13, 7, 5, 9]
    y_obj = [ 3, 9, 5, 15, 3, 5]
    map_y=[]
    map_x=[]

    # map_x.append(x_start)
    # map_y.append(y_start)


    # for i in range(0, length):
    #     index.append(item.index(int(path[i])))
    #     x_obj.append(x[index[i]])
    #     y_obj.append(y[index[i]])
    x_obj.insert(0, x_start)
    y_obj.insert(0, y_start)
    x_obj.append(x_end)
    y_obj.append(y_end)
    length = len(x_obj)
    now_x = x_obj[0]
    now_y = y_obj[0]

    print x_obj
    for i in range(1,length):
        now_x,now_y=map_single_order(now_x,now_y,x_obj[i],y_obj[i])


path=[1]

# map_single_order(6,5,3,3)
# map_to_point(path)

def drawPic():
    global all_x
    global all_y
    try:
        orderid = int(inputEntry.get())
    except:
        orderid = 50
        print 'interger'
        inputEntry.delete(0, END)
        inputEntry.insert(0, '50')
    drawPic.f.clf()
    drawPic.a = drawPic.f.add_subplot(111)

    # x=[0,0,1,2,3,4,5,6,6]
    # y=[1,2,2,2,2,2,2,2,3]
    x=all_x
    y=all_y
    color = ['b', 'r', 'y', 'g','black','purple','orange']
    for i in range(len(x)):

        drawPic.a.scatter(x[i], y[i], s=50, color=color[np.random.randint(len(color))])
    x_obj=[0,3,7,13,7,5,9,0]
    y_obj=[0,3,9,5,15,3,5,0]
    # drawPic.a.scatter(x_obj, y_obj, s=5, color=color[np.random.randint(len(color))])
    drawPic.a.scatter(x_obj, y_obj, s=200, color=color[np.random.randint(len(color))])



    drawPic.a.set_title('The Optimal Path')
    drawPic.canvas.show()


if __name__ == '__main__':
    map_to_point(path)
    print all_x
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