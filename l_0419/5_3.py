"""
演示while循环的基础案例 - 猜数字
"""

import random
num = random.randint(1, 100)
count = 0

# 通过一个布尔类型的变量，做循环是否继续的标记
flag = True
while flag:
    guess_num = int(input("请输入你要猜测的数字:"))
    count += 1
    if guess_num == num:
        print("猜中了")
        # 设置标记为False，结束循环
        flag = False
    else:
        if guess_num > num:
            print("你猜的数字大了")
        else:
            print("你猜的数字小了")

print(f"你总共猜了{count}次")
 

