"""
演示函数使用参数
"""

# def add(x, y):
#     result = x + y
#     print(f"{x}+{y}的计算结果是{result}")

# add(1, 2)

# 练习
def check(num):
    print("请示你的健康码以及72小时的核酸证明,并配合则量体温！")
    if num <= 37.5:
        print(f"体温测量中,你的体温是: {num}度, 体温正常请进！")
    else:
        print(f"体温测量中,你的体温是: {num}度, 体温异常,请离开！")

check(37.3)