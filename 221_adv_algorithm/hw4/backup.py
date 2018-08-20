import csv
import math
import sys
import copy
import time
import numpy as np

carry = []
item = []
x = []
y = []
path = []
ori_order = []
ori_dis = []
opt_dis = []
opt_order = []
mst_bound=[]

def position(lst, k):
    return lst[k:] + lst[:k]

def Item_valid(itlist, itid):
    if itid in itlist:
        return itid
    while itid not in itlist:
        print"This item is not in the warehouse, please input a new valid item id"
        new_item = input()
        if new_item in itlist:
            return new_item


def MST_lower_bound(order, x_obj, y_obj):
    print order
    print x_obj,y_obj
    min_length = 1000
    distance = []
    sum = 0
    for i in range(0, len(order)):
        distance.append(find_distance(x_obj[0], y_obj[0], x_obj[i], y_obj[i]))
    distance.remove(np.min(distance))
    sum += np.min(distance)
    distance.remove(np.min(distance))
    sum += np.min(distance)

    print distance
    print sum

    mst = [1]
    while (len(mst) < len(order) - 1):
        for i in range(1, len(order)):
            if i not in mst:
                for j in mst:
                    length = find_distance(x_obj[j], y_obj[j], x_obj[i], y_obj[i])
                    if length < min_length:
                        min_length = length
                        min_i = i
        print min_length
        mst.append(min_i)
        sum += min_length
    return sum


def Read_in_warehouse(filename='warehouse-grid.csv'):
    csv_reader = csv.reader(open(filename))
    global item
    global x
    global y
    for row in csv_reader:
        if (len(row) == 3):
            item.append(int(row[0]))
            x.append(2 * int(math.floor(float(row[1]))) + 1)  # move 0,0 to 1,1 to make the path outside
            y.append(2 * int(math.floor(float(row[2]))) + 1)


def Read_in_orders(filename='warehouse-orders-v01.csv'):
    global ori_order
    csv_reader = open(filename)
    order_list = []
    for line in csv_reader:
        data = line.strip().split("\t")
        order_list.append(data)
    ori_order = copy.deepcopy(order_list)
    return order_list


def Back_to_unload(x_ini, y_ini, x_end=0, y_end=0):
    global carry
    print"Now bring the items back to the car at (", x_end, ",", y_end, "): "
    if y_ini < y_end and x_ini < x_end:
        if y_ini % 2 != 0:
            y_ini = y_ini + 1
            print"move from (", x_ini, ',', (y_ini - 1), ") to (", x_ini, ',', y_ini, ")"
        print"move from (", x_ini, ',', y_ini, ") to (", x_end - 1, ',', y_ini, ")"
        print"move from (", x_end - 1, ',', y_ini, ") to (", x_end - 1, ',', y_end, ")"
    elif y_ini < y_end and x_ini > x_end:
        if y_ini % 2 != 0:
            y_ini = y_ini + 1
            print"move from (", x_ini, ',', (y_ini - 1), ") to (", x_ini, ',', y_ini, ")"
        print"move from (", x_ini, ',', y_ini, ") to (", x_end + 1, ',', y_ini, ")"
        print"move from (", x_end + 1, ',', y_ini, ") to (", x_end + 1, ',', y_end, ")"
    elif y_ini > y_end and x_ini < x_end:
        if y_ini % 2 != 0:
            y_ini = y_ini - 1
            print"move from (", x_ini, ',', (y_ini - 1), ") to (", x_ini, ',', y_ini, ")"
        print"move from (", x_ini, ',', y_ini, ") to (", x_end - 1, ',', y_ini, ")"
        print"move from (", x_end - 1, ',', y_ini, ") to (", x_end - 1, ',', y_end, ")"
    else:
        if y_ini % 2 != 0:
            y_ini = y_ini - 1
            print"move from (", x_ini, ',', (y_ini + 1), ") to (", x_ini, ',', y_ini, ")"
        print"move from (", x_ini, ',', y_ini, ") to (", x_end + 1, ',', y_ini, ")"
        print"move from (", x_end + 1, ',', y_ini, ") to (", x_end + 1, ',', y_end, ")"
    print"Unload the items", carry, "in the car"
    carry = []


def find_distance(x1, y1, x2, y2):
    distance = abs(x1 - x2) + abs(y1 - y2) - 1
    average = distance + 1
    return average


def calculate_ori_dis(order, x_obj, y_obj, x_ini=0, y_ini=0, x_end=0, y_end=0):
    length = len(order)
    sum_dis = 0
    find_distance(x_ini, y_ini, x_obj[0], y_obj[0])
    for i in range(0, length):
        sum_dis = sum_dis + find_distance(x_ini, y_ini, x_obj[i], y_obj[i])
        x_ini = x_obj[i]
        y_ini = y_obj[i]
    sum_dis = sum_dis + find_distance(x_ini, y_ini, x_end, y_end)
    ori_dis.append(sum_dis)


def Find_order(order, x_ini=0, y_ini=0, x_end=0, y_end=0):
    global carry
    global item
    global x
    global y
    path=[]
    index = []
    x_obj = []
    y_obj = []
    length = len(order)
    min_path_length=1000

    for i in range(0, length):
        index.append(item.index(int(order[i])))
        x_obj.append(x[index[i]])
        y_obj.append(y[index[i]])
    calculate_ori_dis(order, x_obj, y_obj, x_ini, y_ini, x_end, y_end)
    order.append(0)
    x_obj.append(0)
    y_obj.append(0)

    for i in range(0,len(x_obj)):
        path_length=nearest_neightbor_round(order, x_obj, y_obj,i)
        if min_path_length >= path_length[0]:
            min_path_length=path_length[0]
            path=path_length[1]
    newpath=position(path,path.index(0))
    newpath.remove(0)
    mst=MST_lower_bound(newpath, x_obj, y_obj)
    print"path",newpath
    print"MST Lower bound is:", mst
    print"The order takes at least total steps of", min_path_length
    opt_order.append(newpath)
    opt_dis.append(min_path_length)
    mst_bound.append(mst)
    # Back_to_unload(x_ini, y_ini, x_end, y_end)


def local_min_algorithm(order, x_obj, y_obj, x_ini=0, y_ini=0,x_end=0,y_end=0):
    distance_sum = 0
    global path
    while x_obj != []:
        min = 1000
        length = len(x_obj)
        for i in range(0, length):
            local_min = find_distance(x_ini, y_ini, x_obj[i], y_obj[i])
            if local_min < min:
                min = local_min
                min_i = i
        distance_sum = distance_sum + min
        path.append(order[min_i])
        x_ini = x_obj[min_i]
        y_ini = y_obj[min_i]
        order.remove(order[min_i])
        x_obj.remove(x_obj[min_i])
        y_obj.remove(y_obj[min_i])
    distance_sum = distance_sum + find_distance(x_ini, y_ini, x_end, y_end)
    print "Path follow the order:", (path)
    print"The order takes total steps of", (distance_sum)
    opt_order.append(path)
    opt_dis.append(distance_sum)
    path = []


def nearest_neightbor_round(order, x_obj, y_obj,initial_i):
    distance_sum = 0
    x_ini=x_obj[initial_i]
    x_end=x_ini
    y_ini=y_obj[initial_i]
    y_end=y_ini
    path=[]
    path.append(order[initial_i])
    x_object=copy.deepcopy(x_obj)
    y_object = copy.deepcopy(y_obj)
    orders=copy.deepcopy(order)
    orders.remove(orders[initial_i])
    x_object.remove(x_object[initial_i])
    y_object.remove(y_object[initial_i])
    # print orders
    while x_object != []:
        min = 1000
        length = len(x_object)
        for i in range(0, length):
            local_min = find_distance(x_ini, y_ini, x_object[i], y_object[i])
            if local_min < min:
                min = local_min
                min_i = i
        distance_sum = distance_sum + min
        path.append(orders[min_i])
        x_ini = x_object[min_i]
        y_ini = y_object[min_i]
        orders.remove(orders[min_i])
        x_object.remove(x_object[min_i])
        y_object.remove(y_object[min_i])
    distance_sum = distance_sum + find_distance(x_ini, y_ini, x_end, y_end)

    # print "Path follow the order:", (path)
    # print"The order takes total steps of", (distance_sum)
    # opt_order.append(path)
    # opt_dis.append(distance_sum)
    return distance_sum,path


def Find_item_part1(order, x_start, y_start, x_end, y_end):
    global carry
    global item
    global x
    global y
    x_ini = int(x_start)
    y_ini = int(y_start)
    for i in range(0, len(order)):
        obj = order[i]
        obj_item = obj
        index = item.index(obj_item)
        x_obj = x[index]
        y_obj = y[index]
        print "Now you are at position", '(', x_ini, ',', y_ini, ')'
        print "The Object id is ", obj_item
        print "The object is at", '(', x_obj, ',', y_obj, ')'
        if (y_ini < y_obj):
            if (y_ini % 2 != 0):
                y_ini = y_ini + 1
                print"move from (", x_ini, ',', (y_ini - 1), ") to (", x_ini, ',', y_ini, ")"
            print"move from (", x_ini, ',', y_ini, ") to (", x_obj - 1, ',', y_ini, ")"
            print"move from (", x_obj - 1, ',', y_ini, ") to (", x_obj - 1, ',', y_obj, ")"
        else:
            if (y_ini % 2 != 0):
                y_ini = y_ini - 1
                print"move from (", x_ini, ',', (y_ini + 1), ") to (", x_ini, ',', y_ini, ")"
            print"move from (", x_ini, ',', y_ini, ") to (", x_obj - 1, ',', y_ini, ")"
            print"move from (", x_obj - 1, ',', y_ini, ") to (", x_obj - 1, ',', y_obj, ")"
        carry.append(obj_item)
        x_ini = x_obj - 1
        y_ini = y_obj
        print"Now carrying item", carry
    Back_to_unload(x_ini, y_ini, x_end, y_end)

    return


def write_result(order_list, x_start, y_start, x_end, y_end):
    global ori_order
    title = ['Order ID', 'start_x', 'start_y', 'end_x', 'end_y', 'ori_order', 'ori_distance', 'opt_order',
             'opt_distance','mst_Lower_bound']
    csvfile = open('result.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(title)
    for i in range(0, len(order_list)):
        writer.writerow([i + 1, x_start, y_start, x_end, y_end, ori_order[i], ori_dis[i], opt_order[i], opt_dis[i],mst_bound[i]])
    csvfile.close()


def main(x_start=0, y_start=0, x_end=0, y_end=0):
    t_begin=time.time()
    Read_in_warehouse()
    print "Read-in warehouse=", time.time() - t_begin, "second"
    print"Welcome to the warehouse order management system!"
    print"Do you want to use the default start location at (0,0) and end at (0,0)?"
    print"input y for Yes, n for No:"
    choice = raw_input()
    if choice == 'n':
        print"Please input the x of start_position:"
        x_start = input()
        print"Please input the y of start_position:"
        y_start = input()
        print"Please input the x of end_position:"
        x_end = input()
        print"Please input the y of end_position:"
        y_end = input()
    print"Location setting complete"

    print"Input 1 if you want to input order directly,Input 2 if you want to input a order file,Input 3 if you want to get a order in the order file:"
    version = input()

    if version == 2:
        print("please input the file name like warehouse-orders-v01.csv or by default input 0:")
        filename = raw_input()
        if filename == '0':
            filename = 'warehouse-orders-v01.csv'
        t_start = time.time()
        order_list = Read_in_orders(filename)
        for i in range(0, len(order_list)):
            order = order_list[i]
            Find_order(order, x_start, y_start, x_end, y_end)
        write_result(order_list, x_start, y_start, x_end, y_end)
        print"Job Complete"
        print("The result is stored in file named result.csv")
        print "Execution time=", time.time() - t_start, "second"

    if version == 1:
        order = []
        print("please input the item ID one by one end with return, input 0 when finished:")
        id = input()
        while id != 0:
            id = Item_valid(item, id)
            order.append(id)
            print order
            id = input()
        t_start = time.time()
        Find_order(order, x_start, y_start, x_end, y_end)
        print opt_order[0]
        Find_item_part1(opt_order[0], x_start, y_start, x_end, y_end)
        print"Job Complete"
        print "Execution time=", time.time() - t_start, "second"

    if version == 3:
        print("please input the file name like warehouse-orders-v01.csv or by default input 0:")
        filename = raw_input()
        if filename == '0':
            filename = 'warehouse-orders-v01.csv'
        print("please input the order ID:")
        i = input()-1
        t_start = time.time()
        order_list = Read_in_orders(filename)
        print "Read-in orders time=", time.time() - t_start, "second"
        order = order_list[i]
        Find_order(order, x_start, y_start, x_end, y_end)
        print"Job Complete"
        print "Execution time=", time.time() - t_start, "second"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(sys.argv[0])
        main()
