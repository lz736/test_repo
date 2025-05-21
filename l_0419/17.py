#namelist = []  #定义一个空的列表

namelist = ["小李","小王","小张"]
# print(namelist[0:3])

# testlist = [1,"测试"]          #列表可以存储不同类型的数据
# print(type(testlist[0]))
# print(type(testlist[1]))

# for name in namelist:
#     print(name)

#print(len(namelist))    #len()函数可以获取列表的长度

# i = 0

# one = len(namelist)

# while i < one:
#     print(namelist[i])
#     i += 1

#增加 【append】

# print("-----增加前,名单的列表数据-----------")
# for name in namelist:
#     print(name)

# namertemp = input("请添加学生的姓名:")
# namelist.append(namertemp)   #在末尾添加一个元素

# print("-----增加后,名单的列表数据-----------")
# for name in namelist:
#     print(name)

# 增extend
# a = [1,2]
# b = [3,4]
# a.append(b)   #将列表的一个元素，加到a列表中
# print(a)

# a.extend(b)    #将b列表中的元素，逐一加到a列表中
# print(a)

#增 insert
# a = [0,1,2]
# a.insert(1,3)          #第一个变量表示插入的位置，第二个变量表示插入的元素
# print(a)               #指定位置插入元素


#删  【del】   【pop】  【remove】
# mvname = ["葫芦娃","图图","杀死比尔","再来一次"]
# print("-----删除前,电影的列表数据-----------")
# for name in mvname:
#     print(name)

# #del mvname[2]       #删除指定位置的元素  
# #mvname.pop()         #删除末尾最后一个元素
# mvname.remove("图图")   #删除指定元素

# print("-----删除后,电影的列表数据-----------")
# for name in mvname:
#     print(name)

#改  :
# print("-----增加前,名单的列表数据-----------")
# for name in namelist:
#     print(name)

# namelist[1] = "小明"   #修改指定位置的元素

# print("-----增加后,名单的列表数据-----------")
# for name in namelist:
#     print(name)

#查  :【in,not in】

# findname = input("请输入你要查找的学生姓名:")

# if findname in namelist:
#     print("找到了")
# else:
#     print("没有找到")

mylist = ["a","b","c","d","a","e"]

# print(mylist.index("a",1,5))  #可以查找指定范围内的元素，并返回找到对应数据的位置
# print(mylist.index("a",1,4))  #范围区间，左闭右开  [1,3)   找不到区间会报错

#print(mylist.count("a"))  #统计元素出现的次数
#排序和反转
# a = [1,6,2,3]
# print(a)

# a.reverse()  #反转列表
# print(a)

# a.sort()  #排序   升序
# print(a)

# a.sort(reverse=True)  #降序
# print(a)

#schoolname = [[],[],[]]   #有桑元素的空列表,每一个元素都是一个空列表

schoolname = [["北京大学,清华大学"],["复旦大学,南开大学,师范大学"],["浙江大学,大专"]]

print(schoolname[0][0])

