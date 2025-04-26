# 练习
# 定义一个数字 
num = 10

if int(input("请猜一个数字：")) == num:
    print("恭喜你第一次就猜对了")
elif int(input("猜错了,再猜一次：")) == num:
    print("猜对了")
elif int(input("猜错了,再猜一次:")) == num:
    print("恭喜,最后一次机会,你猜对了")
else:
    print("很遗憾,你猜错了")