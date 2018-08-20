import csv
import numpy as np
from part3 import find_distance


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




a=Test(2,3)
# a.show_num()
# a.show_num(2)

li=[0,1,2,3,5,7,9,15]
def demo(lst, k):
    return lst[k:] + lst[:k]
# print(demo(li,li.index(7)))


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

order=[0,1,2,4]
x_obj=[0,3,7,17]
y_obj=[0,1,13,11]
print MST_lower_bound(order,x_obj,y_obj)