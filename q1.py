import pygame
import math
import random
import copy

pygame.init()
size = width, height = 1200, 700
screen=pygame.display.set_mode(size)

def pointgenerator(L,r,deg,inc,j,k):
    for i in range(6):
        L.append((j+r*math.cos((math.pi*deg)/180),k+r*math.sin((math.pi*deg)/180)))
        deg=deg+inc #This function generates points for a regular hexagon centred at (j,k), with radius of circumcircle(or side length) r

r=5 #Side or circumradius of each hexagonal cell

m=10
n=20
'''for k in range(90): #Function for creating a grid
    for j in range(130):
        L1=[]
        l=n+j*2*r*math.cos((math.pi*30)/180)
        pointgenerator(L1,r,30,60,l,m)
        pygame.draw.polygon(screen,(25,255,255),L1,1)
        pygame.display.update() #Creating a row of hexagons
    m+=r+r*math.sin((math.pi*30)/180) #Shifting the y coordinate for the centres of the hexagon in the next row
    n+=(-1)**k*r*math.cos((math.pi*30)/180)'''

Llivecell=set() #Set containing the indices of all the live cells
Lunderp=set() #Set containing the indices of the cells which last died by underpopulation
Loverp=set() #Set containing the indices of the cells which last died by overpopulation
Resurrect={} #Dictionary containing the indices as keys and the iteration in which they died as value 

def livecell(j,k,temp):
    L2=[]
    m2=10+k*(r+r*math.sin((math.pi*30)/180))
    n2=20
    if k%2!=0:
        n2=20+r*math.cos((math.pi*30)/180)
    l=n2+j*2*r*math.cos((math.pi*30)/180)
    pointgenerator(L2,r,30,60,l,m2)
    pygame.draw.polygon(screen,(255,255,255),L2)
    #pygame.display.update()
    temp.add((j,k))  #Function for making a cell alive and adding it to the set of live cells

def resurrectcell(j,k,temp):
    L2=[]
    m2=10+k*(r+r*math.sin((math.pi*30)/180))
    n2=20
    if k%2!=0:
        n2=20+r*math.cos((math.pi*30)/180)
    l=n2+j*2*r*math.cos((math.pi*30)/180)
    pointgenerator(L2,r,30,60,l,m2)
    pygame.draw.polygon(screen,(0,255,0),L2)
    #pygame.display.update()
    temp.add((j,k))  #Function for making a cell alive and adding it to the set of live cells

def celldeath(j,k,temp):
    L2=[]
    m2=10+k*(r+r*math.sin((math.pi*30)/180))
    n2=20
    if k%2!=0:
        n2=20+r*math.cos((math.pi*30)/180)
    l=n2+j*2*r*math.cos((math.pi*30)/180)
    pointgenerator(L2,r,30,60,l,m2)
    pygame.draw.polygon(screen,(255,0,0),L2)
    #pygame.display.update()
    if (j,k) in temp:
        temp.remove((j,k))  #Function for the death of a cell and removing it from the set of live cells

while(len(Llivecell)-50):
    j=random.randint(50,69)
    k=random.randint(40,59)
    livecell(j,k,Llivecell) #Starting the game
#print(Llivecell)
pygame.display.update()

def countneighbours(j, k):
    count = 0
    offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if k% 2 == 0:
       offsets.extend([(-1, -1), (-1, 1)])
    else:
        offsets.extend([(1, -1), (1, 1)])
    for i in offsets:
        n = (j + i[0], k + i[1])
        if n in Llivecell:
            count += 1
    return count

'''def countneighbours(j,k):
    count=0
    if (j-1,k) in Llivecell:
        count+=1
    if (j+1,k) in Llivecell:
        count+=1
    if (j,k-1) in Llivecell:
        count+=1
    if (j,k+1) in Llivecell:
        count+=1
    #For odd k
    if k%2!=0:
        if (j+1,k-1) in Llivecell:
            count+=1
        if (j+1,k+1) in Llivecell:
            count+=1
    #For even k
    else:
        if (j-1,k-1) in Llivecell:
            count+=1
        if (j-1,k+1) in Llivecell:
            count+=1
    return count'''

clock=pygame.time.Clock()

for i in range(10000):
    temp=copy.copy(Llivecell)
    for k in range(90): 
        for j in range(130):
            if countneighbours(j, k)<2:
                if (j,k) in temp and (j,k) not in Lunderp:
                    celldeath(j,k,temp)
                    Lunderp.add((j,k))
                    Resurrect[(j,k)]=i
                if (j,k) in Loverp:
                    Loverp.remove((j,k))
            if countneighbours(j, k)==3 and (j,k) not in Llivecell:
                livecell(j,k,temp)
            if countneighbours(j,k)>3:
                if (j,k) in temp and (j,k) not in Loverp:
                    celldeath(j,k,temp)
                    Loverp.add((j,k))
                    Resurrect[(j,k)]=i
                if (j,k) in Lunderp:
                    Lunderp.remove((j,k))
    for t in Resurrect:
        if Resurrect[t]==i-6:
            resurrectcell(t[0],t[1],temp)
    if i%4==0:
        while True:
            a,b=random.randint(0,129),random.randint(0,89)
            if (a,b) not in Llivecell:
                livecell(a,b,temp)
                break
            else:
                continue            
    Llivecell.clear()
    Llivecell=temp
    
    clock.tick(100)
    pygame.display.update()
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
