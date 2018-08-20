import csv
import math
import sys
import copy

carry = []
item = []
x = []
y = []
path=[]
ori_order=[]
ori_dis=[]
opt_dis=[]
opt_order=[]


def Item_valid(itlist,itid):
    if itid in itlist:
        return itid
    while itid not in itlist:
        print"This item is not in the warehouse, please input a new valid item id"
        new_item=input()
        if new_item in itlist:
            return new_item


def Read_in_warehouse():
    csv_reader = csv.reader(open('warehouse-grid.csv'))
    global item
    global x
    global y
    for row in csv_reader:
        if(len(row)==3):
            item.append(int(row[0]))
            x.append(2 * int(math.floor(float(row[1])))+1) #move 0,0 to 1,1 to make the path outside
            y.append(2 * int(math.floor(float(row[2])))+1)


def Read_in_orders():
    global  ori_order
    csv_reader = open('warehouse-orders-v01.csv')
    order_list=[]
    count=0
    for line in csv_reader:
        data = line.strip().split("\t")
        order_list.append(data)
    ori_order=copy.deepcopy(order_list)
    return order_list


def Back_to_unload(x_ini,y_ini,x_end=0,y_end=0):
    global carry
    print"Now bring the items back to the car at (0,0): "
    print"move from (", x_ini, ',', (y_ini), ") to (", x_ini, ',0', ")"
    print"move from (", x_ini, ',0', ") to (", 0, ',', 0, ")"
    print"Put the items", carry, "in the car"
    carry = []
    print"Round finished"


def find_distance(x1,y1,x2,y2):
    distance = abs(x1 - x2) + abs(y1 - y2) - 1
    average=distance+1
    return average


def calculate_ori_dis(order,x_obj,y_obj,x_ini=0,y_ini=0,x_end=0,y_end=10):
    length=len(order)
    sum_dis=0
    find_distance(x_ini,y_ini,x_obj[0],y_obj[0])
    for i in range(0,length):
        sum_dis= sum_dis+find_distance(x_ini,y_ini,x_obj[i],y_obj[i])
        x_ini=x_obj[i]
        y_ini=y_obj[i]
    sum_dis=sum_dis+find_distance(x_ini,y_ini,x_end,y_end)
    ori_dis.append(sum_dis)



def Find_order(order,x_ini=0,y_ini=0,x_end=0,y_end=10):
    global carry
    global item
    global x
    global y
    index=[]
    x_obj=[]
    y_obj=[]
    length=len(order)
    path=[]


    for i in range(0,length):
        index.append(item.index(int(order[i])))
        x_obj.append(x[index[i]])
        y_obj.append(y[index[i]])
    calculate_ori_dis(order, x_obj, y_obj, x_ini, y_ini, x_end, y_end)
    local_min_algorithm(order,x_obj,y_obj,x_ini,y_ini,x_end,y_end)

    # Back_to_unload(x_ini, y_ini, x_end, y_end)


def local_min_algorithm(order,x_obj,y_obj,x_ini=0,y_ini=0,x_end=0,y_end=10):
    length = len(order)
    # print order
    # print x_obj
    distance_sum=0
    global path
    while x_obj!=[]:
        min = 1000
        length = len(x_obj)
        for i in range(0,length):
            local_min=find_distance(x_ini,y_ini,x_obj[i],y_obj[i])
            if(local_min<min):
                min=local_min
                min_i=i
        distance_sum=distance_sum+min
        path.append(order[min_i])
        x_ini=x_obj[min_i]
        y_ini=y_obj[min_i]
        order.remove(order[min_i])
        x_obj.remove(x_obj[min_i])
        y_obj.remove(y_obj[min_i])
    distance_sum=distance_sum+find_distance(x_ini,y_ini,x_end,y_end)
    print "Path follow the order:",(path)
    print"The order takes total steps of",(distance_sum)
    opt_order.append(path)
    opt_dis.append(distance_sum)
    path=[]


def Find_item_part1(obj=290,x_start=0,y_start=0,x_end=0,y_end=0):
    global carry
    global item
    global x
    global y
    x_ini = int(x_start)
    y_ini = int(y_start)
    x_obj = 1000
    y_obj = 1000
    obj_item = Item_valid(item, obj)
    index = item.index(obj_item)
    x_obj = x[index]
    y_obj = y[index]
    distance = abs(x_obj - x_ini) + abs(y_obj - y_ini) - 1
    print "Now you are at position", '(', x_ini, ',', y_ini, ')'
    print "The Object id is ", obj_item
    print "The object is at", '(', x_obj, ',', y_obj, ')'
    print"start tracing......"

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
    print"How many items", obj_item, "do you want?"
    num = input()
    for i in range(0, num):
        carry.append(obj_item)
    print "Object acquired"
    print"Total step takes", distance, "moves."
    print"Now is at ", "(", x_obj - 1, ',', y_obj, ") "
    x_ini = x_obj - 1
    y_ini = y_obj
    print"Now carrying item", carry
    print "Please show the next item you want to get,if done,input 0"
    a = input()
    if a == 0:
        print"Picking Done"
        print"Now bring the items back to the car at (0,0): "
        print"move from (", x_ini, ',', (y_ini), ") to (", x_ini, ',0', ")"
        print"move from (", x_ini, ',0', ") to (", 0, ',', 0, ")"
        print"Put the items", carry, "in the car"
        carry = []
        print"Round finished"
        print"Do you want to pick any other items? input item id or input 0 if no more items."
        b = input()
        if b == 0:
            print"Job Complete"
            return
        main(b, 0, 0, x_end, y_end)

        return
    main(int(a), x_obj - 1, y_obj, x_end, y_end)
    return

def write_result(order_list, x_start, y_start,x_end,y_end):
    global ori_order
    title=['Order ID','start_x','start_y','end_x','end_y','ori_order','ori_distance','opt_order','opt_distance']
    csvfile = open('result.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(title)
    for i in range(0,len(order_list)):
        writer.writerow([i+1,x_start, y_start,x_end,y_end,ori_order[i],ori_dis[i],opt_order[i],opt_dis[i]])
    csvfile.close()

def main(obj=290,x_start=0,y_start=0,x_end=0,y_end=10):
   Read_in_warehouse()
   order_list=Read_in_orders()
   # print len(order_list)
   for i in range(0,len(order_list)):
       order=order_list[i]
       Find_order(order, x_start, y_start,x_end,y_end)
   write_result(order_list, x_start, y_start,x_end,y_end)









if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(sys.argv[0])
        main()
    if len(sys.argv) == 2:
        obj = sys.argv[1]  # item id
        main(obj)
    if len(sys.argv) == 4:
            obj = int(sys.argv[1])  # item id
            x_start= int(sys.argv[2])  # initial x coordinate
            y_start = int(sys.argv[3])  # initial y coordinate
            main(obj, x_start, y_start)
    if len(sys.argv) == 6:
            obj = int(sys.argv[1])  # item id
            x_start = int(sys.argv[2])  # initial x coordinate
            y_start = int(sys.argv[3])  # initial y coordinate
            x_end = int(sys.argv[4])  # initial x coordinate
            y_end = int(sys.argv[5])  # initial y coordinate
            main(obj,x_start,y_start,x_end,y_end)
    if len(sys.argv)!=2 and len(sys.argv)!=4 and len(sys.argv)!=6:
        print "Please give the command as (object_id,x of initial position,y of initial position,x of end position,y of end position) " "or the default will be (290,0,0,0,10)"
