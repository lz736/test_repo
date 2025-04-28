"""
练习案例： 发工资
"""

#工资余额
money = 10000
#for循环对员工发工资
for i in range(1, 21):
    import random
    score = random.randint(1, 10)

    if score < 5:
        print(f"员工{i}绩效分{score},不满足,不发工资,下一位")
        continue

#判断工资余额是否充足
    if money >= 1000:
        money -= 1000
        print(f"员工{i},满足条件发工资1000,,公司余额:{money}")
    else:
        print(f"余额不足,当前余额:{money}元,不足以发工资,不发了,下个月再来")
        #break结束发放
        break
