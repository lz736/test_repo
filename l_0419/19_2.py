# #函数的定义
# def printinfo():
#     print("-------------------")
#     print("人生苦短,我用python")
#     print("-------------------")

# #函数的调用
# printinfo()
# printinfo()


#带参数的函数
# def add2Num(a,b):
#     c = a + b
#     print(c)

# add2Num(11,22)

#带返回值的函数

# def add2Num(a,b):
#     return a+b   #通过return返回计算结果

# reture = add2Num(11,22)
# print(reture)
# print(add2Num(11,22))     

#返回多个值的函数
# def divid(a,b):
#     shang = a//b
#     yushu = a%b
#     return shang,yushu

# sh, yu = divid(5,2)   #需要多个值来保存返回值

# print("商: %d,余数: %d"%(sh,yu))

#练习  1.打印一条横线的函数
# def henxian():
#     print("----------------------")

# henxian()

#练习  2.根据输入的参数打印自定义条的横线
# def henxian():
#     print("--------------")

# def zhixian(num):
#     i = 0
#     while i < num:
#         henxian()
#         i += 1

# zhixian(5)
#练习  3.写一个函数求三个数的和
# def he(a,b,c):
#     return a+b+c

# reture = he(50,54,45)
# print(reture)

#练习   4.求三个数的平均值
# def he(a,b,c):
#     return (a+b+c)/3

# reture = he(50,54,45)
# print(reture)

#全局变量和局部变量
# def test1():
#     a = 300    #局部变量
#     print("test1-----修改前:a=%d"%a)
#     a = 100
#     print("test1-----修改后:a=%d"%a)

# def test2():
#     a = 500    #不同的函数可以定义相同的名字，彼此无关
#     print("test2-----:a=%d"%a)

# test1()
# test2()

#全局变量和局部变量相同名字
# a = 200   #全局变量


# def test1():
#     a = 300    #局部变量优先使用
#     print("test1-----修改前:a=%d"%a)
#     a = 100
#     print("test1-----修改后:a=%d"%a)

# def test2():
#     a = 500    #不同的函数可以定义相同的名字，彼此无关
#     print("test2-----:a=%d"%a)

# test1()
# test2()

#在函数中修改全局变量
a = 200   

def test1():
    global a    #声明全局变量在函数中的标识符
    print("test1-----修改前:a=%d"%a)
    a = 100
    print("test1-----修改后:a=%d"%a)

def test2():
    a = 500    #不同的函数可以定义相同的名字，彼此无关
    print("test2-----:a=%d"%a)

test1()
test2()






