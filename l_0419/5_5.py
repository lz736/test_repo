"""
演示使用while的嵌套使用
打印出九九乘法表
"""

# 定义完成循环的控制变量
i= 1
while i <= 9:
     
    # 定义内层循环的控制变量
    j = 1
    while j <= i:
        # 内层循环的print语句, 不要换行,通过\t制表符来实现
        print(f"{j}*{i} = {j * i} \t",end='')
        j += 1

    i += 1
    print() 