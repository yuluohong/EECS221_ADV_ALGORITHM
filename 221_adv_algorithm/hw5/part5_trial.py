import csv
import math
import sys
import copy
import time
import numpy as np

dim = []
dim = np.mat(dim)
carry = []
item = []
x = []
y = []
path = []
ori_order = []
ori_dis = []
opt_dis = []
opt_order = []
mst_bound = []
bab_order = []
bab_dis = []


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
    all_sum = 0
    if len(order) == 2:
        all_sum = 2 * find_distance(x_obj[0], y_obj[0], x_obj[1], y_obj[1])
        return all_sum
    for k in range(0, len(order)):
        min_length = 1000
        distance = []
        sum = 0
        for i in range(0, len(order)):
            if i != k:
                distance.append(find_distance(x_obj[k], y_obj[k], x_obj[i], y_obj[i]))
        # print distance

        sum += np.min(distance)
        # print np.min(distance)
        distance.remove(np.min(distance))
        sum += np.min(distance)
        # print np.min(distance)
        # print distance
        # print distance
        # print sum

        mst = []
        if k != 1:
            mst.append(1)
        else:
            mst.append(2)

        while (len(mst) < len(order) - 1):
            for i in range(0, len(order)):
                if i not in mst and i != k:
                    for j in mst:
                        length = find_distance(x_obj[j], y_obj[j], x_obj[i], y_obj[i])
                        if length < min_length:
                            min_length = length
                            min_i = i
            mst.append(min_i)
            sum += min_length
            # print sum
            # print sum
        if sum > all_sum:
            all_sum = sum
    return all_sum


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


def read_in_dim(filename='item-dimensions-tabbed.txt'):
    global dim
    dimensions_order = np.loadtxt(filename, skiprows=1)  # ID,length,width,height,weight
    # print np.shape(dimensions_order)
    dim = np.transpose(dimensions_order)
    return dim


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
    global dim
    path = []
    index = []
    x_obj = []
    y_obj = []
    effort = 0
    length = len(order)
    min_path_length = 1000

    for i in range(0, length):
        index.append(item.index(int(order[i])))
        x_obj.append(x[index[i]])
        y_obj.append(y[index[i]])
    calculate_ori_dis(order, x_obj, y_obj, x_ini, y_ini, x_end, y_end)

    order.insert(0, 0)
    x_obj.insert(0, x_ini)
    y_obj.insert(0, y_ini)
    print "Please choose the algorithm you want to use. Input 1 for nearest-neighbor and others for B&B:"
    choice = input()
    if choice != 1:
        bab_path = []
        bab_path_length = 0
        bab_path, bab_path_length = branch_and_bound(order, x_obj, y_obj, x_end, y_end)
        bab_path.remove(0)

        bab_order.append(bab_path)
        bab_path_length = bab_path_length
        bab_dis.append(bab_path_length)
        print 'bab_order', bab_path
        print 'bab_steps:', bab_path_length
        # effort = calculate_effort(order, x_obj, y_obj, bab_path, dim, x_end, y_end)
        # print 'effort', effort
    else:
        order.remove(0)
        x_obj.remove(x_ini)
        y_obj.remove(y_ini)

        order.append(0)
        x_obj.append(x_end)
        y_obj.append(y_end)
        # print y_end
        for i in range(0, len(x_obj)):
            path_length = nearest_neightbor_round(order, x_obj, y_obj, i)
            if min_path_length >= path_length[0]:
                min_path_length = path_length[0]
                path = path_length[1]
        newpath = position(path, path.index(0))
        newpath.remove(0)
        print"path", newpath
        print"The order takes at least total steps of", min_path_length
        opt_order.append(newpath)
        opt_dis.append(min_path_length)
        effort = calculate_effort(order, x_obj, y_obj, newpath, dim, x_end, y_end)
        print 'effort', effort
    mst = MST_lower_bound(order, x_obj, y_obj)
    mst_bound.append(mst)
    print"MST Lower bound is:", mst

    # Back_to_unload(x_ini, y_ini, x_end, y_end)


def local_min_algorithm(order, x_obj, y_obj, x_ini=0, y_ini=0, x_end=0, y_end=0):
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


def nearest_neightbor_round(order, x_obj, y_obj, initial_i):
    distance_sum = 0
    x_ini = x_obj[initial_i]
    x_end = x_ini
    y_ini = y_obj[initial_i]
    y_end = y_ini
    path = []
    path.append(order[initial_i])
    x_object = copy.deepcopy(x_obj)
    y_object = copy.deepcopy(y_obj)
    orders = copy.deepcopy(order)
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
    return distance_sum, path


class Order_mat:
    def __init__(self, mat, cost, order):
        self.mat = mat
        self.cost = cost
        self.order = []
        self.order = order
        self.tried_order = copy.deepcopy(order)


def demo(lst, k):
    return lst[k:] + lst[:k]


def branch_and_bound(order, x_obj, y_obj, x_end, y_end):
    upperorder,uppercost=upper_bound(order,x_obj,y_obj)
    print 'upper',uppercost
    renew_flag=0
    # glob_min_cost=float('inf')
    glob_min_cost=uppercost+1-19
    ini_matrix = []
    all_mat = []
    length = len(order)
    for j in range(0, len(order)):
        row = []
        for i in range(0, len(order)):
            if j == i:
                row.append(float('inf'))
            else:
                row.append(find_distance(x_obj[j], y_obj[j], x_obj[i], y_obj[i]))
        ini_matrix.append(row)
    ini_matrix = np.mat(ini_matrix)
    # print ini_matrix
    cost = 0
    ini_mat, cost = matrix_process(ini_matrix, length, cost)
    all_mat.append(Order_mat(ini_mat, cost, [0]))
    # print 'initial cost',cost
    # print 'initial matrix'
    # print ini_mat
    loop_count = 0

    while (1):
        min_i = 0
        loop_count=loop_count+1
        min_cost = float('inf')
        # print len(all_mat)
        if len(all_mat) > 1000 and loop_count>500:
            loop_count=0
            for i in range(len(all_mat) - 1, -1, -1):
                if len(all_mat[i].order) < len(all_mat[i].tried_order):
                    del all_mat[i]
            for i in range(len(all_mat) - 1, -1, -1):
                if all_mat[i].cost > glob_min_cost:
                    del all_mat[i]

        for i in range(0, len(all_mat)):
            if len(all_mat[i].tried_order) < length:
                cost = all_mat[i].cost
                    # print 'mat',i, 'cost',cost
                if cost==min_cost:
                    if len(all_mat[i].order)>len(all_mat[min_i].order):
                        min_cost=cost
                        min_i=i
                if cost < min_cost:
                    min_cost = cost
                    min_i = i
                        # print 'choose',min_i,'cost',min_cost
        # else:
            # for i in range(len(all_mat) - 1000, len(all_mat)):
            #     if len(all_mat[i].tried_order) < length and all_mat[i].cost < min_cost:
            #         min_cost = all_mat[i].cost
            #         min_i = i
        q = []

        for i in range(0, length):
            if i not in all_mat[min_i].tried_order:
                q.append(i)
        if q != []:
            # print len(all_mat)
            # print q[0]
            while q != []:
                all_mat[min_i].tried_order.append(q[0])
                # print all_mat[min_i].order
                now_mat, cost = process(all_mat[min_i].mat, length, all_mat[min_i].cost, all_mat[min_i].order[-1], q[0])
                if cost<glob_min_cost:
                    new_order = copy.deepcopy(all_mat[min_i].order)
                    new_order.append(q[0])
                    if len(all_mat[min_i].order) != length - 2:
                        all_mat.append(Order_mat(now_mat, cost, new_order))
                    else:
                        for i in range(0, length):
                            if i not in new_order:
                                now_mat, cost = process(now_mat, length, cost,new_order[-1], i)
                                if cost < glob_min_cost:
                                    new_order.append(i)
                                    all_mat.append(Order_mat(now_mat, cost, new_order))

                        if glob_min_cost>all_mat[-1].cost:
                            glob_min_cost=all_mat[-1].cost
                            renew_flag=1



                q.remove(q[0])

            if renew_flag==1:
                renew_flag=0
                for i in range(len(all_mat) - 1, -1, -1):
                    if all_mat[i].cost > glob_min_cost:
                        del all_mat[i]
                for i in range(len(all_mat) - 1, -1, -1):
                    if len(all_mat[i].order) < len(all_mat[i].tried_order):
                        del all_mat[i]


            #print len(all_mat)
            print all_mat[-1].order
            #print 'cost', cost
            print 'glocost', glob_min_cost

        else:
            min_to_last=float('inf')
            min_cost = float('inf')
            for i in range(0, len(all_mat)):
                # print all_mat[i].order
                if len(all_mat[i].order) == length:
                    last_distance = find_distance(x_end, y_end, x_obj[all_mat[i].order[-1]],
                                                  y_obj[all_mat[i].order[-1]])
                    # print 'last',last_distance
                    if all_mat[i].cost + last_distance < min_cost:
                        min_cost = all_mat[i].cost + last_distance
                        min_i = i
                        min_to_last = last_distance
                        # print all_mat[i].order,all_mat[i].cost,last_distance
            new_order = []
            ds = find_true_distance(x_obj, y_obj, all_mat[min_i].order) + min_to_last
            # print 'final mat:'
            # print all_mat[min_i].mat
            # print ds
            for i in range(0, len(all_mat[min_i].order)):
                new_order.append(order[all_mat[min_i].order[i]])

            # print new_order
            return new_order, ds


def matrix_process(matrix, length, c):
    ini_matrix = copy.deepcopy(matrix)
    for i in range(0, length):
        if np.min(ini_matrix[i]) != float('inf'):
            c += np.min(ini_matrix[i])
            ini_matrix[i] -= np.min(ini_matrix[i])
    for j in range(0, length):
        if np.min(ini_matrix[:, j]) != float('inf'):
            c += np.min(ini_matrix[:, j])
            ini_matrix[:, j] -= np.min(ini_matrix[:, j])
    return ini_matrix, c


def matrix_preprocess(mat, last_node, next_node):
    ini_mat = copy.deepcopy(mat)
    ini_mat[last_node] += float('inf')
    ini_mat[:, next_node] += float('inf')
    ini_mat[next_node, last_node] = float('inf')
    return ini_mat


def process(matrix, length, c, last_node, next_node):
    infinity = float('inf')
    # infinity=10000
    ini_mat = copy.deepcopy(matrix)
    ini_mat[last_node] += infinity
    ini_mat[:, next_node] += infinity
    ini_mat[next_node, last_node] = infinity
    for i in range(0, length):
        if np.min(ini_mat[i]) != infinity:
            c += np.min(ini_mat[i])
            ini_mat[i] -= np.min(ini_mat[i])
    for j in range(0, length):
        if np.min(ini_mat[:, j]) != infinity:
            c += np.min(ini_mat[:, j])
            ini_mat[:, j] -= np.min(ini_mat[:, j])
    return ini_mat, c

def upper_bound(order, x_obj, y_obj):
    ini_matrix = []
    length = len(order)
    for j in range(0, len(order)):
        row = []
        for i in range(0, len(order)):
            if j == i:
                row.append(float('inf'))
            else:
                row.append(find_distance(x_obj[j], y_obj[j], x_obj[i], y_obj[i]))
        ini_matrix.append(row)
    ini_matrix = np.mat(ini_matrix)
    cost = 0
    ini_mat, cost = matrix_process(ini_matrix, length, cost)
    next_mat = ini_mat
    now_cost = cost
    # print ini_matrix
    # print now_cost
    nn_order = []
    nn_order.append(0)

    while (len(nn_order) < len(order)):
        min_i = 0
        min_cost = float('inf')
        q = []

        for i in range(0, len(order)):
            if i not in nn_order:
                q.append(i)
        for i in range(0, len(q)):
            now_mat, cost = process(next_mat, length, now_cost, nn_order[-1], q[i])
            # print 'now', q[i]
            # print 'cost', cost
            # print now_mat
            if cost < min_cost:
                min_cost = cost
                min_i = i
                min_mat = now_mat
        next_mat = min_mat
        nn_order.append(q[min_i])
        # print 'next'
        # print q[min_i]
        # print next_mat
        now_cost = min_cost
    return nn_order, min_cost

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
             'opt_distance', 'mst_Lower_bound', 'bab_order', 'bab_distance']
    csvfile = open('result.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(title)
    for i in range(0, len(order_list)):
        writer.writerow(
            [i + 1, x_start, y_start, x_end, y_end, ori_order[i], ori_dis[i], opt_order[i], opt_dis[i], mst_bound[i],
             bab_order[i], bab_dis[i]])
    csvfile.close()


def find_true_distance(x_obj, y_obj, order):
    distance = 0
    for i in range(0, len(order) - 1):
        distance += find_distance(x_obj[order[i]], y_obj[order[i]], x_obj[order[i + 1]], y_obj[order[i + 1]])
    return distance


def calculate_effort(order, x_obj, y_obj, path, dim, end_x, end_y):
    effort = 0
    weight = 0
    distance = 0
    for i in range(0, len(path) - 1):
        i1 = order.index(path[i])
        i2 = order.index(path[i + 1])
        # print int(path[i])
        # print i1
        # print x_obj[i1]
        if int(path[i]) not in dim[0]:
            print 'can not find the weight of item', path[i]
        else:
            location = np.where(dim[0, :] == int(path[i]))
            weight += dim[4, location][0][0]
        distance = find_distance(x_obj[i1], y_obj[i1], x_obj[i2], y_obj[i2])
        effort += weight * distance
        print weight
        print distance
        print effort
    if int(path[-1]) not in dim[0]:
        print 'can not find the weight of', path[-1]
    else:
        location = np.where(dim[0, :] == int(path[-1]))
        weight += dim[4, location][0][0]
    distance = find_distance(end_x, end_y, x_obj[i2], y_obj[i2])
    effort += weight * distance
    print weight
    print distance
    print effort
    return effort


def main(x_start=0, y_start=0, x_end=0, y_end=0):
    t_begin = time.time()
    Read_in_warehouse()
    read_in_dim()
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
        i = input() - 1
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
