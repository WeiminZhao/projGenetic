#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
from numpy.random import choice
import matplotlib.pyplot as plt

# the gene pool [1,2,3,4,5,6,7,8]
genePool=[1,2,3,4,5,6,7,8]

# the initialization function to generate initial random populations
def initialization(N=10):
    for i in range(N):
        population.append([])
        for j in range(8):
            randPick = random.randint(1,8)
            while randPick in population[i]:
                randPick = random.randint(1,8)
            population[i].append(randPick)

    #print("initial population ",population)
    return population

#calculate fitness value function
def calcFitness(population):
    fitnessOfPop=[]
    for i in range (len(population)):
        score = 8
        for j in range(8):
            for k in range(j+1,8,1):
                if abs((population[i][j]-population[i][k])/(j+1-k-1))==1 or population[i][j]==population[i][k]:
                    score-=1
                    break
        fitnessOfPop.append(score/8)
    #print("gym evalutaion ",fitnessOfPop)
    return fitnessOfPop

#select population function
def select(population, fitnessOfPop):
    selectedPop=[]

    totalFitness=0
    for val in fitnessOfPop:
        totalFitness+=val
    percFitness=[] #record the % fitness for each member
    for val in fitnessOfPop:
        percFitness.append(val/totalFitness)
    #print(percFitness) #now we can use percFitness as probability to select populations
    
    #this for loop just create the idex of according population member
    index=[]
    for i in range(len(population)):
        index.append(i)
    #then we select the according index based on the distribution of percFitness
    draw = choice(index, int(len(population)/2), False, percFitness)
    #print(draw)
    
    for val in draw:
        selectedPop.append(population[val])
        
    #print("strong individual ",selectedPop)
    return selectedPop

def crossover(selectedPop):
    children=[]
    for i in range(1,len(selectedPop),2):
        c1=[]
        c2=[]
        while True:
            c1=[]
            c2=[]
            for j in range(len(selectedPop[i])):#crossover gene
                s=choice([0,1],1,[0.5,0.5])
                if s[0]==0:
                    c1.append(selectedPop[i][j])
                    c2.append(selectedPop[i-1][j])
                else:
                    c1.append(selectedPop[i-1][j])
                    c2.append(selectedPop[i][j])
            if len(c1) == len(set(c1)) and len(c2) == len(set(c2)): #check if the crossover follow the rules
                break
        children.append(c1)
        children.append(c2)
    #print("new babies ",children)
    
    return children

def crossover_2(selectPop): #another type of crossover
    children=[]
    for i in range(1,len(selectedPop),2):
        c1=[]
        c2=[]
        for j in range(len(selectedPop[i])):#crossover gene
            if(selectedPop[i][j]==selectedPop[i-1][j]): #in this type of crossover, we want to keep the same part of parent and the randomize the different parts
                c1.append(selectedPop[i][j])
                c2.append(selectedPop[i][j])
            else:
                randPick = random.randint(1,8)
                while randPick in c1:
                    randPick = random.randint(1,8)
                c1.append(randPick)
                
                randPick = random.randint(1,8)
                while randPick in c2:
                    randPick = random.randint(1,8)
                c2.append(randPick)
        children.append(c1)
        children.append(c2)
    #print("new babies ",children)
    return children
            
def mutation(group):
    possibilityForMut=0.10
    for individual in group:
        s=choice([0,1],1,[1-possibilityForMut,possibilityForMut])
        if s[0]==1:
            index=[0,1,2,3,4,5,6,7]
            s2=choice(index,2,False)
            
            temp=individual[s2[0]]
            individual[s2[0]]=individual[s2[1]]
            individual[s2[1]]=temp
    return group

def evaluation(fitness):
    finded=0
    findedItem=[]
    for i in range(len(fitness)):
        if fitness[i] == 1:
            finded+=1
            findedItem.append(i)
            
    if finded>=92:
        return True,findedItem
    else:
        return False, findedItem


# In[2]:


#######main process Here#############
#generate populations
N = 4*1000 #the population number, must use a multiplication of 4
population=[]

population = initialization(N)

fitness=[]
for i in range(N):
    fitness.append(0)
plt.hist(fitness)
plt.show()

round=0
while True:
    round+=1
   
    #calculate fitness value?
    fitness=calcFitness(population)
    
    plt.clf()
    plt.hist(fitness)
    plt.pause(0.05)
    
    if round % 100 ==0:
        print(round," ps",fitness," ")
        #print(population)
    
    #evaluation
    evalu,pos=evaluation(fitness)
    print("fit pop find======> ", len(pos))
    if evalu:# if success
        for val in pos:
            print(population[val])
        break

    #select part of population for crossover
    selectedPop=select(population, fitness)

    #crossover
    children=crossover_2(selectedPop)
    
    #mutation
    children=mutation(children)
    
    #append all children to the population
    selectedPop.extend(children)
    population=[]
    population=selectedPop
print(population)

