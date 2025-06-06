# f = open("test.txt","w")  #打开文件,w模式,如果文件不存在,则创建文件

# f.write("hello word,i am here!")        #将字符串写入文件中

# f.close()  #关闭文件

#read方法,读取指定的字符，开始是定位在文件头部，每执行一次向后移动指定字符数
# f = open("test.txt","r")

# content = f.read(5)

# print(content)


# content = f.read(5)

# print(content)

# f.close()

# f = open("test.txt","r")

# content = f.readlines()    #一次性读完全部文件为列表，每行应该字符串元素

# print(content)

# i = 1
# for temp in content:
#     print("%d:%s"%(i,temp))
#     i += 1

# f.close()


# f = open("test.txt","r")

# content = f.readline() 
# print("1:%s"%content)

# content = f.readline()
# print("2:%s"%content)

# f.close()

import os   #文件重命名

os.rename("test.txt","test1.txt")
