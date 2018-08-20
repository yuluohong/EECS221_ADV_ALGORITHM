import csv
import math
import sys

carry = []

def main(obj=290,x_start=0,y_start=0):
    global carry
    x_ini=int(x_start)
    y_ini=int(y_start)
    x_obj=1000
    y_obj=1000
    obj_item=int(obj)
    csv_reader = csv.reader(open('warehouse-grid.csv'))
    item = []
    x = []
    y = []

    index=-1

    for row in csv_reader:
        if(len(row)==3):
            item.append(int(row[0]))
            x.append(2 * int(math.floor(float(row[1])))+1) #move 0,0 to 1,1 to make the path outside
            y.append(2 * int(math.floor(float(row[2])))+1)
    index=item.index(obj_item)
    # print(index)
    # if index==-1:
    #     print"The item is not in this warehouse"
    #     return
    x_obj=x[index]
    y_obj=y[index]
    distance=abs(x_obj-x_ini)+abs(y_obj-y_ini)-1
    print "Now you are at position", '(',x_ini,',',y_ini,')'
    print "The Object id is ",obj_item
    print "The object is at", '(',x_obj,',',y_obj,')'
    print"start tracing......"

    if(y_ini<y_obj):
        if(y_ini%2!=0):
            y_ini=y_ini+1
            print"move from (",x_ini,',',(y_ini-1),") to (", x_ini ,',',y_ini,")"
        print"move from (", x_ini, ',', y_ini, ") to (", x_obj-1, ',', y_ini, ")"
        print"move from (", x_obj-1, ',', y_ini, ") to (", x_obj - 1, ',', y_obj, ")"
    else:
        if (y_ini % 2 != 0):
            y_ini = y_ini - 1
            print"move from (", x_ini, ',', (y_ini + 1), ") to (", x_ini, ',', y_ini, ")"
        print"move from (", x_ini, ',', y_ini, ") to (", x_obj - 1, ',', y_ini, ")"
        print"move from (", x_obj - 1, ',', y_ini, ") to (", x_obj - 1, ',', y_obj, ")"
    print"How many items ",obj,"do you want?"
    num=input()
    for i in range (0,num):
        carry.append(obj)
    print "Object acquired"
    print"Total step takes",distance,"moves."
    print"Now is at ","(", x_obj - 1, ',', y_obj, ") "
    x_ini=x_obj-1
    y_ini=y_obj
    print"Now carryting item",carry
    print "Please show the next item you want to get,if done,input 0"
    a=input()
    if a==0:
        print"Picking Done"
        print"Now bring the items back to the car at (0,0): "
        print"move from (", x_ini, ',', (y_ini), ") to (", x_ini, ',0', ")"
        print"move from (", x_ini, ',0', ") to (",0,',',0,")"
        print"Put the items",carry,"in the car"
        carry=[]
        print"Round finished"
        print"Do you want to pick any other items? input item id or input 0 if no more items."
        b=input()
        if b==0:
            print"Job Complete"
            return
        main(b,0,0)

        return
    main(int(a),x_obj-1,y_obj)
    return





if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(sys.argv[0])
        main()
    if len(sys.argv) == 2:
        obj = sys.argv[1]  # item id
        main(obj)
    if len(sys.argv) == 4:
            obj = sys.argv[1]  # item id
            x_start= sys.argv[2]  # initial x coordinate
            y_start = sys.argv[3]  # initial y coordinate
            main(obj,x_start,y_start)
    if len(sys.argv)!=2 and len(sys.argv)!=4:
        print "Please give the command as (object_id,x of initial position,y of initial position) or the default will be (290,0,0)"
