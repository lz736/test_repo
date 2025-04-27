"""
演示判断语句的实战案例:终极猜数字
"""

#1.del 构建一个随机的数字变量
import random
num = random.randint(1, 10)

guess_num = int(input("请输入你要猜测的数字:"))

#2. 通过if判断语句进行数字的猜测
if guess_num == num:
    print("恭喜你第一次就猜对了.")
else:
    if guess_num > num:
        print("你猜的数字大了.")
    else:
        print("你猜的数字小了.")

    guess_num = int(input("再次输入你要猜测的数字:"))  

    if guess_num == num:
        print("恭喜你,第二次猜对了.")  
    else:    
        if guess_num > num:            
            print("你猜的数字大了.")
        else:
            print("你猜的数字小了.")  

        guess_num = int(input("第三次输入你要猜测的数字:")) 
            
        if guess_num == num:
            print("恭喜你,第三次猜对了.")  
        else:
            if guess_num > num:            
                print("你猜的数字大了.")
            else:
                print("你猜的数字小了.")  

            guess_num = int(input("第四次输入你要猜测的数字:")) 

            if guess_num == num:
                print("恭喜你,第四次猜对了")
            else:
                print("四次机会用完了,没有猜中.")    
