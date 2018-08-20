from part5_trial import *

order = [0, 11, 2, 4]
x_obj = [0, 3, 11, 7]
y_obj = [0, 1, 17, 13]


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
    print ini_matrix
    print now_cost
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
            now_mat, cost = process(next_mat, length, int(now_cost), nn_order[-1], q[i])
            print 'now', q[i]
            print 'cost', cost
            print now_mat
            if cost < min_cost:
                min_cost = cost
                min_i = i
                min_mat = now_mat
        next_mat = min_mat
        nn_order.append(q[min_i])
        print 'next'
        print q[min_i]
        print next_mat
        now_cost = min_cost
    return nn_order, min_cost


n = []
n, mc = upper_bound(order, x_obj, y_obj)
print n
print mc
