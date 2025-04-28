"""
演示嵌套应用for循环
"""

# 坚持表白一百天，每天都送十朵花

# i = 0
# for i in range(1,101):
#     print(f"今天是第{i}天,准备表白....")
#     # 内层循环
#     for j in range(1,11):
#         print(f"送给小美第{j}朵花")

#     print("小美,我喜欢你")

# print(f"第{i}天,表白成功")

"""
# 用for写出九九乘法表
"""

for i in range(1,10):
    for j in range(1,i+1):
        print(f"{j}*{i} = {j * i} \t",end='')
        
    print()
