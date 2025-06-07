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

# import os   #文件重命名

# os.rename("test.txt","test1.txt")




#捕获异常
'''
try:
    print("--------test------------1---")

    f = open("123.txt","r")

    print("--------test------------2---")

except IOError:   #文件没找到，部署ID异常（输入输出异常）
    pass          #捕获异常后执行的代码
'''

'''
try:
    print(num)
#except IOError:
except NameError:
    print("产生错误了")
'''

#捕获所有异常
'''
try:
    print("--------test------------1---")
    f = open("123.txt","r")
    print("--------test------------2---")

    print(num)
except Exception as result:          #Exception可以承接所有异常
    print("产生错误了")
    print(result)
'''

#try...finally...和嵌套

import time
try:
    f = open("test.txt","r")

    try:
        while True:
            content = f.readline()
            if len(content) == 0:
                break
            time.sleep(2)
            print(content)
    finally:
        f.close()
        print("文件关闭")



except Exception as result:
    print("发生异常...")
