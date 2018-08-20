import csv



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
a.show_num()
# a.show_num(2)

