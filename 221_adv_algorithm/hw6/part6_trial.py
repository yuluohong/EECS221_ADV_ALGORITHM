import csv
import math
import copy
import time
import numpy as np
from Tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

all_x = []
all_y = []
inputEntry = 0
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
distance_flag = 0
eft_bb=[]
eft_nn=[]


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


def Read_in_orders(filename='warehouse-orders-v02-tabbed.txt'):
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
    global distance_flag
    # 0 for left and 1 for right
    if (x1 < x2):
        distance = abs(x1 - x2) + abs(y1 - y2) - distance_flag * 2
        distance_flag = 0
    elif (x1 > x2):
        distance = abs(x1 - x2) + abs(y1 - y2) - distance_flag * 2
        distance_flag = 1
    else:
        distance = abs(x1 - x2) + abs(y1 - y2)
    if y1 == y2:
        distance = distance + 2

    return distance


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
    global eft_bb
    global eft_nn
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
    # print "Please choose the algorithm you want to use. Input 1 for nearest-neighbor and others for B&B:"
    # choice = input()
    choice=3
    if choice == 2:
        bab_path = []
        bab_path_length = 0
        bab_path, bab_path_length = branch_and_bound(order, x_obj, y_obj, x_end, y_end)
        bab_path.remove(0)

        bab_order.append(bab_path)
        bab_dis.append(bab_path_length)
        print 'bab_order', bab_path
        print 'bab_steps:', bab_path_length
        effort = calculate_effort(order, x_obj, y_obj, bab_path, dim, x_end, y_end)
        print 'effort', effort
    elif choice == 1:
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
        # gui()
        # os.system("python map_tes.py")
        effort = calculate_effort(order, x_obj, y_obj, newpath, dim, x_end, y_end)
        print 'effort', effort
    else:
        bab_path = []
        bab_path_length = 0
        bab_path, bab_path_length = branch_and_bound(order, x_obj, y_obj, x_end, y_end)
        bab_path.remove(0)

        bab_order.append(bab_path)
        bab_dis.append(bab_path_length)
        print 'bab_order', bab_path
        print 'bab_steps:', bab_path_length
        effort = calculate_effort(order, x_obj, y_obj, bab_path, dim, x_end, y_end)
        eft_bb.append(effort)
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
        eft_nn.append(effort)
        # print 'effort', effort

    mst = MST_lower_bound(order, x_obj, y_obj)
    mst_bound.append(mst)
    # print"MST Lower bound is:", mst

    # Back_to_unload(x_ini, y_ini, x_end, y_end)


def Find_order_for_gui(order, x_ini=0, y_ini=0, x_end=0, y_end=0):
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
    return newpath,x_obj,y_obj


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


def branch_and_bound(order, x_obj, y_obj, x_end, y_end):
    ts = time.time()
    upperorder, uppercost = upper_bound(order, x_obj, y_obj)
    # print 'upper', uppercost,upperorder
    renew_flag = 0
    end_flag = 0
    # glob_min_cost=float('inf')
    glob_min_cost = uppercost + 1
    dnm_upper = uppercost+1
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
    loop_count = 0

    while (1):
        min_i = 0
        loop_count = loop_count + 1
        min_cost = float('inf')
        # print len(all_mat)
        if len(all_mat) > 1000 and loop_count > 100:
            loop_count = 0
            for i in range(len(all_mat) - 1, -1, -1):
                if len(all_mat[i].order) < len(all_mat[i].tried_order):
                    del all_mat[i]
            for i in range(len(all_mat) - 1, -1, -1):
                if all_mat[i].cost > glob_min_cost:
                    del all_mat[i]
            nowmat = copy.deepcopy(all_mat[-1])
            if len(nowmat.order) != length:
                dnm_upper = dynamic_upper(nowmat, order, x_obj, y_obj)
                # print 'dnm_upper', dnm_upper
                if dnm_upper < glob_min_cost:
                    glob_min_cost = dnm_upper

        for i in range(0, len(all_mat)):
            # if len(all_mat[i].tried_order) < length:
            if len(all_mat[i].order) == len(all_mat[i].tried_order):
                cost = all_mat[i].cost
                # print 'mat',i, 'cost',cost
                if cost == min_cost:
                    if len(all_mat[i].order) > len(all_mat[min_i].order):
                        min_cost = cost
                        min_i = i
                if cost < min_cost:
                    min_cost = cost
                    min_i = i
        if len(all_mat[min_i].order) == length:
            end_flag = 1

        q = []

        for i in range(0, length):
            if i not in all_mat[min_i].tried_order:
                q.append(i)
        if time.time() - ts < 30:
            if q != [] and end_flag != 1:
                # print len(all_mat)
                # print q[0]
                while q != []:
                    all_mat[min_i].tried_order.append(q[0])
                    # print all_mat[min_i].order
                    now_mat, cost = process(all_mat[min_i].mat, length, all_mat[min_i].cost, all_mat[min_i].order[-1],
                                            q[0])
                    # print cost
                    # print 'min',glob_min_cost
                    if cost <= glob_min_cost:
                        new_order = copy.deepcopy(all_mat[min_i].order)
                        new_order.append(q[0])
                        if len(all_mat[min_i].order) != length - 2:
                            all_mat.append(Order_mat(now_mat, cost, new_order))
                        else:
                            for i in range(0, length):
                                if i not in new_order:
                                    now_mat, cost = process(now_mat, length, cost, new_order[-1], i)
                                    if cost <= glob_min_cost:
                                        new_order.append(i)
                                        all_mat.append(Order_mat(now_mat, cost, new_order))

                            if glob_min_cost > all_mat[-1].cost:
                                glob_min_cost = all_mat[-1].cost
                                renew_flag = 1

                    q.remove(q[0])

                if renew_flag == 1:
                    renew_flag = 0
                    for i in range(len(all_mat) - 1, -1, -1):
                        if all_mat[i].cost > glob_min_cost:
                            del all_mat[i]
                    for i in range(len(all_mat) - 1, -1, -1):
                        if len(all_mat[i].order) < len(all_mat[i].tried_order):
                            del all_mat[i]

                            # print len(all_mat)
                            # print all_mat[-1].order
                            # print 'cost', cost
                            # print 'glocost', glob_min_cost

            else:
                min_to_last = float('inf')
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
                # print all_mat[min_i].order
                if all_mat[min_i].order==[0]:
                    all_mat[min_i].order=upperorder
                    min_to_last=find_distance(x_end, y_end, x_obj[all_mat[min_i].order[-1]],
                                  y_obj[all_mat[min_i].order[-1]])
                new_order = []
                ds = find_true_distance(x_obj, y_obj, all_mat[min_i].order) + min_to_last
                # print 'final mat:'
                # print all_mat[min_i].mat
                # print ds
                for i in range(0, len(all_mat[min_i].order)):
                    new_order.append(order[all_mat[min_i].order[i]])

                # print new_order
                # print 'gg'
                return new_order, ds

        else:
            nn_order = all_mat[min_i].order
            next_mat = all_mat[min_i].mat
            now_cost = all_mat[min_i].cost
            while (len(nn_order) < len(order)):
                min_cost = float('inf')
                for i in range(0, len(q)):
                    now_mat, cost = process(next_mat, length, now_cost, nn_order[-1], q[i])

                    if cost < min_cost:
                        min_cost = cost
                        min_i = i
                        min_mat = now_mat
                next_mat = min_mat
                nn_order.append(q[min_i])
                now_cost = min_cost
                q.remove(q[min_i])
            ds = find_true_distance(x_obj, y_obj, nn_order) + find_distance(x_end, y_end, x_obj[nn_order[-1]],
                                                                            y_obj[nn_order[-1]])
            final_order = []
            for i in range(0, len(order)):
                final_order.append(order[nn_order[i]])
            # print 'final',final_order
            return final_order, ds


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


def dynamic_upper(nowmin_mat, order, x_obj, y_obj):
    ini_matrix = []
    length = len(order)

    cost = 0
    ini_mat = copy.deepcopy(nowmin_mat.mat)
    cost = copy.deepcopy(nowmin_mat.cost)
    next_mat = ini_mat
    now_cost = cost
    # print ini_matrix
    # print now_cost
    nn_order = copy.deepcopy(nowmin_mat.order)

    while (len(nn_order) < len(order)):
        min_i = 0
        min_cost = float('inf')
        q = []

        for i in range(0, len(order)):
            if i not in nn_order:
                q.append(i)
        for i in range(0, len(q)):
            now_mat, cost = process(next_mat, length, int(now_cost), nn_order[-1], q[i])
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
    return min_cost


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


def map_single_order(x_now, y_now, x_next, y_next):
    global all_x
    global all_y
    map_x = []
    map_y = []
    if (y_now < y_next):
        if (y_now % 2 != 0):
            y_now = y_now + 1
            map_y.append(y_now)
            map_x.append(x_now)
        if (x_now < x_next):
            while (x_now < x_next - 1):
                x_now = x_now + 1
                map_y.append(y_now)
                map_x.append(x_now)
            while (y_now < y_next):
                y_now = y_now + 1
                map_y.append(y_now)
                map_x.append(x_now)
        elif (x_now > x_next):
            while (x_now > x_next + 1):
                x_now = x_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
            while (y_now < y_next):
                y_now = y_now + 1
                map_y.append(y_now)
                map_x.append(x_now)
        else:
            while (y_now < y_next):
                y_now = y_now + 1
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
                y_now = y_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
        elif (x_now > x_next):
            while (x_now > x_next + 1):
                x_now = x_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
            while (y_now > y_next):
                y_now = y_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
        else:
            while (y_now > y_next):
                y_now = y_now - 1
                map_y.append(y_now)
                map_x.append(x_now)
    print"Follow the path to the next item:"
    for i in range(len(map_x)):

        print(map_x[i], map_y[i])
    print 'Item Reached'
    # all_x=all_x+map_x
    # all_y=all_y+map_y
    all_x.append(map_x)
    all_y.append(map_y)
    return x_now, y_now


def map_to_point(path, x_obj,y_obj,x_start=0, y_start=0, x_end=0, y_end=0):

    x_obj.insert(0, x_start)
    y_obj.insert(0, y_start)

    length = len(x_obj)
    now_x = x_obj[0]
    now_y = y_obj[0]

    # print x_obj
    for i in range(1, length):
        now_x, now_y = map_single_order(now_x, now_y, x_obj[i], y_obj[i])


def drawPic( x_ini=0, y_ini=0, x_end=0, y_end=0):
    global all_x
    global all_y
    # global root
    # global inputEntry
    # inputEntry = Entry(root)
    try:
        orderid = int(inputEntry.get())
    except:
        orderid = 50
        print 'interger'
        inputEntry.delete(0, END)
        inputEntry.insert(0, '50')
    drawPic.f.clf()
    # drawPic.f.clf()

    drawPic.a = drawPic.f.add_subplot(111)
    print "Now showing the path to collect order number:",orderid
    order_list = Read_in_orders()
    order = order_list[orderid-1]
    path,x_obj,y_obj=Find_order_for_gui(order, x_ini, y_ini, x_end, y_end)
    map_to_point(path,x_obj,y_obj,x_ini,y_ini,x_end,y_end)
    # print all_x
    x = all_x
    y = all_y
    color = ['b', 'r', 'y', 'g', 'black', 'purple', 'orange']
    for i in range(len(x)):
        drawPic.a.scatter(x[i], y[i], s=50, color=color[np.random.randint(len(color))])

    drawPic.a.scatter(x_obj, y_obj, s=200, color=color[np.random.randint(len(color))])

    drawPic.a.set_title('The Optimal Path')
    drawPic.canvas.show()
    all_x=[]
    all_y=[]


def gui():
    global inputEntry
    global root

    # matplotlib.use('TkAgg')
    root = Tk()

    drawPic.f = Figure(figsize=(5, 4), dpi=100)
    drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
    drawPic.canvas.show()
    drawPic.canvas.get_tk_widget().grid(row=0, columnspan=3)

    Label(root, text='Please input the order ID:').grid(row=1, column=0)
    inputEntry = Entry(root)
    inputEntry.grid(row=1, column=1)
    inputEntry.insert(0, '1')
    Button(root, text='Find', command=drawPic).grid(row=1, column=2, columnspan=3)

    root.mainloop()


def write_result(order_list, x_start, y_start, x_end, y_end):
    global ori_order
    title = ['Order ID', 'start_x', 'start_y', 'end_x', 'end_y', 'ori_order', 'ori_distance', 'nn_order',
             'nn_distance', 'nn_effort','mst_Lower_bound', 'bab_order', 'bab_distance','bab_effort']
    csvfile = open('result.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(title)
    for i in range(0, len(order_list)):
        writer.writerow(
            [i + 1, x_start, y_start, x_end, y_end, ori_order[i], ori_dis[i], opt_order[i], opt_dis[i],eft_nn[i], mst_bound[i],
             bab_order[i], bab_dis[i],eft_bb[i]])
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
    i1=0
    i2=0
    if(path!=[]):
        for i in range(0, len(path) - 1):
            i1 = order.index(path[i])
            i2 = order.index(path[i + 1])
            if len(path)==1:
                i2 = 0
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
            # print weight
            # print distance
            # print effort
        if int(path[-1]) not in dim[0]:
            print 'can not find the weight of', path[-1]
        else:
            location = np.where(dim[0, :] == int(path[-1]))
            weight += dim[4, location][0][0]
        distance = find_distance(end_x, end_y, x_obj[i2], y_obj[i2])
        effort += weight * distance
        # print weight
        # print distance
        # print effort
        return effort
    else:
        return 0

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
        print("please input the file name like warehouse-orders-v02-tabbed.txt or by default input 0:")
        filename = raw_input()
        if filename == '0':
            # filename = 'warehouse-orders-v01.csv'
            filename = 'warehouse-orders-v02-tabbed.txt'

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
        print("please input the file name like warehouse-orders-v02-tabbed.txt or by default input 0:")
        filename = raw_input()
        if filename == '0':
            filename = 'warehouse-orders-v02-tabbed.txt'
        print("Do you want to use the GUI to show the path? 1 for yes and others for no:")
        GUI=input()
        if GUI==1:
            gui()
        else:
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
