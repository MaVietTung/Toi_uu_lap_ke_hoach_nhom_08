import time
import random
def input(filename):
    with open(filename, 'r') as file_read:

        N, A, C = [int(x) for x in file_read.readline().split()]
        c = [int(x) for x in file_read.readline().split()]
        a = [int(x) for x in file_read.readline().split()]
        f = [int(x) for x in file_read.readline().split()]
        m = [int(x) for x in file_read.readline().split()]
    return N, A, C, c, a, f, m
N, A, C, c, a, f, m = input('data/miniproject-6/data.txt')


loiNhuan = 0
result = [0 for i in range(N)]
step = 0
x = [0 for i in range(N)]
canTren = [min(A // a[i], C // c[i])for i in range(N)]


def check(k, j):
    sumChiphi = j * c[k]
    sumDienTich = j * a[k]
    for i in range(k):
        sumChiphi += x[i] * c[i]
        sumDienTich += x[i] * a[i]
    if sumChiphi > C or sumDienTich > A:
        return False
    else:
        return True


def updateBest():
    sumLoiNhuan = 0
    for i in range(N):
        sumLoiNhuan += x[i] * f[i]
    return sumLoiNhuan


def Try(k):
    global loiNhuan
    global step
    x[k] = 0
    if k == N-1:
        sumLoiNhuan = updateBest()
        if loiNhuan < sumLoiNhuan:
           
            for i in range(N):
                result[i] = x[i]
            loiNhuan = sumLoiNhuan
            # print(f"step {step}: {loiNhuan}")
            
            # print(result)

    else:
        Try(k + 1)

    for j in range(m[k], canTren[k]+1):
        x[k] = j
        if check(k, j):
            if k == N-1:

                sumLoiNhuan = updateBest()
                if loiNhuan < sumLoiNhuan:
                    step += 1
                    loiNhuan = sumLoiNhuan
                    for i in range(N):
                        result[i] = x[i]
                    # print(f"step {step}: {loiNhuan}")
                
                    # print(result)
            else:
                Try(k + 1)

start = time.time()
Try(0)
end = time.time() - start

print("gia tri lon nhat: ", loiNhuan)
print("------------")
print("don vi cua moi thua ruong lan luot la: ", result)
print(f"time thuc thi {end}")
