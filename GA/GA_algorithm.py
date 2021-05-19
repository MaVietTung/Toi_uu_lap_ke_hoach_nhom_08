import Config
import pickle
import numpy as np
import copy
import sys
import time
import random
from Preprocess_Data import Data


'''
Với mỗi một khởi tạo kích thước ma trận(1,length of tasks).
giá trị của mỗi một node của ma trận là giá trị từ [-1,0,...,Mvs.size()].
hàm check() để kiểm tra mỗi cá thể có thỏa mãn yêu cầu của bài toán hay không. 
'''
def check(individual,data):
    isAccept = True
    sum_A = 0
    sum_C = 0
    for i in range(data["N"]):
        sum_A = sum_A + individual[i] *data["a"][i]
        sum_C = sum_C + individual[i] *data["c"][i]
    if sum_A> data["A"] or sum_C>data["C"]:
        return False
    else:
        return isAccept

def init_individual(data):
    action = np.zeros(data["N"])
    A = data["A"]
    C = data["C"]
    for i in range(data["N"]):
        h = []
        if (data["m"][i]<min(int(A/data["a"][i]),int(C/data["c"][i]))):
            h = [i for i in range(data["m"][i],min(int(A/data["a"][i]),int(C/data["c"][i])))]
        h.append(0)
        m = random.choice(h)

        action[i]=m
        A = A - data["a"][i]*m
        C = C - data["c"][i]*m
    return action

def init_individual(data):
    individual = np.zeros(data["N"])
    A = data["A"]
    C = data["C"]
    for i in range(data["N"]):
        h = []
        if (data["m"][i]<min(int(A/data["a"][i]),int(C/data["c"][i]))):
            h = [i for i in range(data["m"][i],min(int(A/data["a"][i]),int(C/data["c"][i])))]
        h.append(0)
        m = random.choice(h)

        individual[i]=m
        A = A - data["a"][i]*m
        C = C - data["c"][i]*m
    return individual

def mutation(location,individual,data):
    A = data["A"]
    C = data["C"]
    location =location[0]
    h = []
    for i in range(data["N"]):
        if i!= location:
            A = A - data["a"][i]*individual[0][i]
            C = C - data["c"][i]*individual[0][i]
    if (data["m"][i]<min(int(A/data["a"][location]),int(C/data["c"][location]))):
        h = [i for i in range(data["m"][location],min(int(A/data["a"][location]),int(C/data["c"][location])))]
    h.append(0)
    return h

'''
tính giá trị hàm fitness của bài toán
@parameter:individual là một một cá thể trong quần thể
'''

def fitness_function(individual,data):
    fitness = 0
    for i in range(data["N"]):
        fitness = fitness +data["f"][i]*individual[i]
    
    return -fitness

        

initialization=[]
"""
Sử dụng thuật toán GA cho bài toán.
@para init_size_population:số lượng cá thể khởi tạo cho quần thể ban đầu
@para number_loop: số vòng lặp để tìm giá trị tối ưu
@para cut_poins: số điểm cắt khi lai ghép
"""

def GA(init_size_population:int,number_loop,cut_points:int):
    data = Data().read_data()

    #khởi tạo quần thể
    initialization=[]
    first = time.time()
    for i in range(init_size_population):
        individual = init_individual(data)
        initialization.append(individual)
    optimize_value=fitness_function(initialization[0],data)
    optimize_individual=initialization[0]
    opt=[]
    for individual in initialization:
        if(optimize_value>fitness_function(individual,data)):
            optimize_value=fitness_function(individual,data)
            optimize_individual=copy.deepcopy(individual)
    population=initialization

    for i in range(number_loop):
        new_population=[]
        for j in range(int(init_size_population/2)):

            #lai ghép điểm cắt
            if cut_points==1:
                index=np.random.randint(1,len(initialization),size=2)
                first_individual=population[index[0]]
                second_individual =population[index[0]]
                point=np.random.randint(2,data["N"] -1)
                new_individual=np.concatenate((first_individual[0:point+1],second_individual[point+1:data["N"]]))
                new_individual1=np.concatenate((second_individual[0:point+1],first_individual[point+1:data["N"]]))

            #lai ghép điểm cắt
            else:
                index=np.random.randint(1,len(population),size=2)
                m=population[index[0]]
                n =population[index[0]]
                point=np.random.randint(3,data["N"]-1)
                point1=np.random.randint(2,point)
                new_individual=np.concatenate((m[0:point1+1],n[point1+1:point+1],m[point+1:data["N"]]))
                new_individual1=np.concatenate((n[0:point1+1],m[point1+1:point+1],n[point+1:data["N"]]))
            if(check(new_individual,data)):
                new_population.append(new_individual)
            if(check(new_individual1,data)):
                new_population.append(new_individual1)

        new_population=np.array(new_population)
        initialization=[]
        for i in range(init_size_population):
            individual = init_individual(data)
            initialization.append(individual)
        
        population=np.concatenate((initialization,new_population),axis=0)


        #đột biến
        for ii in range(int(init_size_population/10)):
            location=np.random.randint(0,data["N"],size=1)
            a = np.random.randint(0,len(population),size=1)
            individual=population[a]
            array_candidate = mutation(location,individual,data)
            population[a,location[0]]=random.choice(array_candidate)
        object_population=[]
        for ii in population:
            if check(ii,data):
                k=fitness_function(ii,data)
                if(optimize_value>k):
                    optimize_value=k
                    optimize_individual=copy.deepcopy(ii)
                object_population.append({'individual':ii,'fitness':k})
        object_population.sort(key=lambda x: x['fitness'])
        a=[]
        for ii in range(init_size_population):
            a.append(object_population[ii]["individual"])
            population=a
        print(-optimize_value)
    last = time.time()
    print(last-first)
    return optimize_individual

print(GA(100,1000,1))

