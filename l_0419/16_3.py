i = 0
while i <= 9:
    a = 1
    while a <= i:
        print(f"{a}*{i}={a*i}",end="\t")
        a += 1
    i += 1
    print()