# contraint statifaction programming
from ortools.sat.python import cp_model
import time
import random
model = cp_model.CpModel()
# dat bien x[i]
# Ghi N, A(dien tich), C(price)
# ghi c(1), c(2), …, c(N) <= C
# ghi a(1), a(2), …, a(N) <= a
# hi f(1), f(2), …, f(N) (loi nhuan)
# ghi m(1), m(2), …, m(N) =0 OR >= m(i)

def input(filename):
    with open(filename, 'r') as file_read:

        N, A, C = [int(x) for x in file_read.readline().split()]
        c = [int(x) for x in file_read.readline().split()]
        a = [int(x) for x in file_read.readline().split()]
        f = [int(x) for x in file_read.readline().split()]
        m = [int(x) for x in file_read.readline().split()]
    return N, A, C, c, a, f, m
N, A, C, c, a, f, m = input('data/miniproject-6/data.txt')


infinity = 99999999
start = time.time()
# 0 neu san pham i khong duoc chon,  1 neu san pham i duoc chon
t = [model.NewIntVar(0, 1, 't(' + str(i) + ')') for i in range(N)]
#  so don vi moi loai
x = [model.NewIntVar(m[i], infinity, 'x(' + str(i) + ')') for i in range(N)]
# gia tri la 0 hoac lon hoac bang m[i]
u = [model.NewIntVar(0, infinity, 'u(' + str(i) + ')') for i in range(N)]

# if t[i] == 0 => u[i] == 0
first = [model.NewBoolVar('first(' + str(i) + ')') for i in range(N)]
for i in range(N):
    model.Add(t[i] == 0).OnlyEnforceIf(first[i])
    model.Add(t[i] != 0).OnlyEnforceIf(first[i].Not())
    model.Add(u[i] == 0).OnlyEnforceIf(first[i])

# if t[i] == 1 => u[i] == x[i]
second = [model.NewBoolVar('second(' + str(i) + ')') for i in range(N)]
for i in range(N):
    model.Add(t[i] == 1).OnlyEnforceIf(second[i])
    model.Add(t[i] != 1).OnlyEnforceIf(second[i].Not())
    model.Add(u[i] - x[i] == 0).OnlyEnforceIf(second[i])

# rang buoc ve tong dien tich
model.Add(sum(a[i] * u[i] for i in range(N)) <= A)

# rang uoc ve tong chi phi
model.Add(sum(c[i] * u[i] for i in range(N)) <= C)

# ham toi uu
model.Maximize(sum(u[i] * f[i] for i in range(N)))

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10.0
status = solver.Solve(model)
end = time.time() - start
print(status)
if status == cp_model.OPTIMAL:
    
    for i in range(N):
        print(solver.Value(u[i]))
        
    # for i in range(N):
    #     print(solver.Value(t[i]))
    print('Objective value =', solver.ObjectiveValue())
print(f"time thuc thi {end}")
