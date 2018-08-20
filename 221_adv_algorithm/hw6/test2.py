import Tkinter

import numpy as np

from part5 import find_distance

# dimensions_order=np.loadtxt('dimensions.txt',skiprows=1) #ID,length,width,height,weight
dimensions_order = np.loadtxt('item-dimensions-tabbed.txt', skiprows=1)  # ID,length,width,height,weight

print np.shape(dimensions_order)

dim = np.transpose(dimensions_order)
print np.shape(dim)
a = np.where(dim[0, :] == 37065)
print a
print dim[4, a][0][0]
top = Tkinter.Tk()


# top.mainloop()
def calculate_effort(order, x_obj, y_obj, path, dim, end_x, end_y):
    effort = 0
    weight = 0
    distance = 0
    for i in range(0, len(path) - 1):
        i1 = order.index(path[i])
        i2 = order.index(path[i + 1])
        location = np.where(dim[0, :] == path[i])
        weight += dim[4, location][0][0]
        distance = find_distance(x_obj[i1], y_obj[i1], x_obj[i2], y_obj[i2])
        effort += weight * distance
        print weight
        print distance
        print effort
    location = np.where(dim[0, :] == path[-1])
    weight += dim[4, location][0][0]
    distance = find_distance(end_x, end_y, x_obj[i2], y_obj[i2])
    effort += weight * distance
    print weight
    print distance
    print effort
    return effort


# print np.max(dimensions_order[0])
a=[2,4,6,9]
for i in range(len(a)-1,-1,-1):
    if a[i]<5:
        del a[i]

print a
print len(a)