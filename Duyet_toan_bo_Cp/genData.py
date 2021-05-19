import random
N = int(input("enter a value: "))
A = N * 30
C = N * 7000



def genData(filename):
    global N, A, C
    parameter = [N, A, C]
    parameter = [str(i) for i in parameter]
    c = [str(random.randint(1, C // 10)) for i in range(N)]
    a = [str(random.randint(1, A // 10)) for i in range(N)]
    f = [str(random.randint(1, int(c[i])) // 3) if random.randint(1, int(c[i])) // 3 >= 1 else str(1) for i in range(N)]
    m = [str(random.randint(1, (A // 5) // int(a[i]))) for i in range(N)]
    
    str_parameter = " ".join(parameter)
    str_c = " ".join(c)
    str_a = " ".join(a)
    str_f = " ".join(f)
    str_m = " ".join(m)
    with open(filename, 'w') as f:
        f.write(str_parameter + '\n')
        f.write(str_c + '\n')
        f.write(str_a + '\n')
        f.write(str_f + '\n')
        f.write(str_m + '\n')
  

genData('data/miniproject-6/data.txt')
