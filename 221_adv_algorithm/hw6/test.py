import csv
import numpy as np
from part5 import find_distance
import copy
import time

# a = [1, 2]
# csvfile = open('test.csv', 'wb')
# writer = csv.writer(csvfile)
# writer.writerow(a)
#
# data = [
#     ('2', '25'),
#     ('33', '18')
# ]
# writer.writerows(data)
#
# csvfile.close()
class Test:
    def __init__(self,a,b):
        self.first=a
        self.second=b


    def show_num(self):
        print(self.first+self.second)
a=1.1
b=int(a)
print b

# a.show_num()
# a.show_num(2)

class Order_mat:
    def __init__(self,mat,cost,order):
        self.mat=mat
        self.cost=cost
        self.order=[]
        self.order=order
        self.tried_order=copy.deepcopy(order)



def demo(lst, k):
    return lst[k:] + lst[:k]

def MST_lower_bound(order, x_obj, y_obj):
    all_sum=0
    if len(order)==2:
        all_sum=2*find_distance(x_obj[0], y_obj[0], x_obj[1], y_obj[1])
        return all_sum
    for k in range(0,len(order)):
        min_length = 1000
        distance = []
        sum = 0
        for i in range(0, len(order)):
            if i!=k:
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
        if k!=1:
            mst.append(1)
        else:mst.append(2)

        while (len(mst) < len(order) - 1):
            for i in range(0, len(order)):
                if i not in mst and i!=k:
                    for j in mst:
                        length = find_distance(x_obj[j], y_obj[j], x_obj[i], y_obj[i])
                        if length < min_length:
                            min_length = length
                            min_i = i
            mst.append(min_i)
            sum += min_length
        # print sum
            # print sum
        if sum>all_sum:
            all_sum=sum
    return all_sum

order=[0,11,2,4,5,6,21,29,2,3,99]
x_obj=[0,3,11,7,1,21,1,30,5,6,7]
y_obj=[0,1,17,13,3,4,1,10,8,9,10]

def branch_and_bound(order,x_obj,y_obj):

    ini_matrix=[]
    all_mat=[]
    length = len(order)
    for j in range(0,len(order)):
        row = []
        for i in range(0,len(order)):
            if j==i:
                row.append(float('inf'))
            else:row.append(find_distance(x_obj[j],y_obj[j],x_obj[i],y_obj[i]))
        ini_matrix.append(row)
    ini_matrix=np.mat(ini_matrix)
    # print ini_matrix
    cost=0
    ini_mat,cost = matrix_process(ini_matrix,length,cost)
    all_mat.append(Order_mat(ini_mat,cost,[0]))
    print ini_mat
    # print cost
    # print all_mat[0].order

    while(1):
        t1=time.time()
        min_i = 0
        min_cost = float('inf')
        if len(all_mat)<500:
            for i in range(0,len(all_mat)):
                if len(all_mat[i].tried_order)<length and all_mat[i].cost<min_cost:
                    min_cost=all_mat[i].cost
                    min_i=i
        else:
            for i in range(len(all_mat)-100,len(all_mat)):
                if len(all_mat[i].tried_order)<length and all_mat[i].cost<min_cost:
                    min_cost=all_mat[i].cost
                    min_i=i
        # print min_i
        q=[]
        t2=time.time()
        print '1st',t2-t1
        print len(all_mat)
        for i in range(0,length):
            if i not in all_mat[min_i].tried_order:
                q.append(i)
        if q!=[]:
            # print q[0]

            all_mat[min_i].tried_order.append(q[0])
            t3=time.time()
            print '2nd',t3-t2
            # print all_mat[min_i].order
            # now_mat=matrix_preprocess(all_mat[min_i].mat,all_mat[min_i].order[-1],q[0])
            now_mat,cost = process(all_mat[min_i].mat, length, all_mat[min_i].cost,all_mat[min_i].order[-1],q[0])
            # print now_mat
            # print cost
            # new_order=copy.deepcopy(all_mat[min_i].order)
            # new_order.append(q[0])
            # print 'new',new_order
            t4=time.time()
            print '3rd', t4 - t3
            all_mat.append(Order_mat(now_mat,cost,all_mat[min_i].order+[q[0]]))
            t5 = time.time()
            print '4th', t5 - t4

        else:
            min_cost=float('inf')
            for i in range(0,len(all_mat)):
                # print all_mat[i].order
                if len(all_mat[i].order)==length:
                    if cost < min_cost:
                        min_cost = cost
                        min_i = i
                # print all_mat[i].mat
            new_order = []
            for i in range(0, len(all_mat[min_i].order)):
                new_order.append(order[all_mat[min_i].order[i]])
            return new_order,all_mat[min_i].cost
        # # len(all_mat[0].order)
        # # print ini_mat
        # # print cost
        # start_node=0
        # next_node=1
        #
        # for i in range(1,length):
        #     next_node=i
        #     now_mat = matrix_preprocess(ini_mat, start_node, next_node)
        #     now_mat, cost = matrix_process(now_mat, length, cost)
        #     if cost<min_cost:
        #         min_cost=cost
        #         min_i=i
        #
        # now_mat=matrix_preprocess(ini_mat,start_node,next_node)
        # now_mat,cost=matrix_process(now_mat,length,cost)
        # # print now_mat
        # # print cost
        # last_node=next_node
        # next_node=2
        # now_mat = matrix_preprocess(now_mat, start_node, next_node)
        # now_mat, cost = matrix_process(now_mat, length, cost)
        # # print now_mat
        # # print cost


def matrix_process(matrix,length,c):
    ini_matrix=copy.deepcopy(matrix)
    for i in range(0, length):
        if np.min(ini_matrix[i])!=float('inf'):
            c += np.min(ini_matrix[i])
            ini_matrix[i] -= np.min(ini_matrix[i])
    for j in range(0, length):
        if np.min(ini_matrix[:, j])!=float('inf'):
            c += np.min(ini_matrix[:, j])
            ini_matrix[:, j] -= np.min(ini_matrix[:, j])
    return ini_matrix,c


def matrix_preprocess(mat,last_node,next_node):
    ini_mat=copy.deepcopy(mat)
    ini_mat[last_node] += float('inf')
    ini_mat[:, next_node] += float('inf')
    ini_mat[next_node,last_node]=float('inf')
    return ini_mat

def process(matrix,length,c,last_node,next_node):
    infinity=float('inf')
    # infinity=10000
    t1 = time.time()
    ini_mat = copy.deepcopy(matrix)
    t2 = time.time()
    ini_mat[last_node] +=infinity
    ini_mat[:, next_node] += infinity
    ini_mat[next_node, last_node] = infinity
    t3 = time.time()
    for i in range(0, length):
        if np.min(ini_mat[i])!=infinity:
            c += np.min(ini_mat[i])
            ini_mat[i] -= np.min(ini_mat[i])
    for j in range(0, length):
        if np.min(ini_mat[:, j])!=infinity:
            c += np.min(ini_mat[:, j])
            ini_mat[:, j] -= np.min(ini_mat[:, j])
    t4 = time.time()
    print '3', t4 - t3
    return ini_mat,c


t=time.time()
# a,b=branch_and_bound(order,x_obj,y_obj)
t2=time.time()-t
# print a
# print b

def find_true_distance(order):
    distance = 0
    for i in range(0,len(order)-1):
        distance+=find_distance(x_obj[order[i]],y_obj[order[i]],x_obj[order[i+1]],y_obj[order[i+1]])
    return distance