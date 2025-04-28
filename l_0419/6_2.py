"""
练习
"""

num = 101
count = 0
for x in range(1,num):
    if x % 2 == 0:
        count += 1
print(f"1到101之间有{count}个偶数")