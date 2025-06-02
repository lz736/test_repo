# tup1 = ()
# print(type(tup1))

# #tup2 = (50,)
# tup2 =(50,60,70)
# print(type(tup2))   #class 'tuple'

# tup1 = ("abc","def",2020,2021,666,777,888)
# print(tup1[0])
# print(tup1[-1])   #访问最后一个元素
# print(tup1[1:5])   #左闭右开,进行切片

#增加
# tup1 = (12,34,56)
# tup2 = ("abc","xyz")

# tup = tup1 + tup2
# print(tup)

#删除
tup1 = (12,34,56)
print(tup1)
del tup1
print("删除后：")   #删除元组tup1
print(tup1)

