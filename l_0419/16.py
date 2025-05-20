# if True:
#     print("True")
#     print("Answer")
# else:
#     print("False")
# print("end")

# num = 100

# if num >= 90 and num <= 100:
#     print("本次考试,成绩为A")
# elif num >= 80 and num < 90:
#     print("本次考试,成绩为B")
# else:
#     print("本次考试,成绩为C")

# xinbie = 1     #1代表男生,0代表女生
# danshen = 1    #1代表单身,0代表有男/女朋友

# if xinbie == 0 :
#     print("男生")
#     if danshen == 1:
#         print("我给你介绍一个把？")
#     else:
#         print("你给我介绍一下把？")
# else:
#     print("女生")
#     if danshen == 0:
#         print("我给你介绍一个把？")
#     else:
#         print("你给我介绍一下把？")


#练习
import random
#0代表剪刀,1代表石头,2代表布
a = random.randint(0,2)
b = int(input("输入："))

if b == a:
    print("平局")

elif (b > a and b-a == 1) or (b < a and b-a == -2):
    print("你赢了")

else:
    print("你输了")
