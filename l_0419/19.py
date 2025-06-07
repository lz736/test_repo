#不允许修改
#增
# tup1 = (12,34,5)
# tup2 = ("abc","def")

# tup = tup1 + tup2
# print(tup)

# #删
'''
tup1 = (12,34,56)
print(tup1)
def tup1   #删除了整个元组变量
print("删除后：")
print(tup1)
'''

# #字典的定义
info = {"name":"小李","age":18}

# #字典的访问
# print(info["name"])
# print(info["age"])

# #访问了不存在的
# #print(info["gender"])    #直接访问会报错

# #print(info.get("gender"))    #使用get访问不会报错,默认返回Nome

# print(info.get("age","20"))
# print(info.get("gender","m"))   #没找到的时候，可以设定默认值

#增
# newID = input("请输入新的学号：")
# info["id"] = newID

# print(info["id"])

#删
# info = {"name":"小李","age":18}
# print("删除前：%s"%info["name"])

# del info["name"]

#print("删除后：%s"%info["name"])   #删除后，name不存在，会报错因为没有指定值了
# info = {"name":"小李","age":18}

# print("清空前：%s"%info)

# info.clear()

# print("清空后：%s"%info)



#改
# info = {"name":"小李","age":18}

# info["age"] = 20

# print(info["age"])

#查    (遍历)

info = {"id":1,"name":"小李","age":18}
# print(info.keys())   #得到所有的键

# print(info.values())  #得到所有的值

# print(info.items())  #得到所有的键值对 每个值对是元组

#遍历所有的键
# for key in info.keys():
#     print(key)

# #遍历所有的值
# for value in info.values():
#     print(value)

#遍历所有的键值对
# for key,value in info.items():
#     print("key=%s,value=%s"%(key,value))
    
mylist = ["a","b","c"]

for i,x in enumerate(mylist):
    print(i+1,x)
