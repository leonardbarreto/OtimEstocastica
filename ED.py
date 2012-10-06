# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:33:38 2012

@author: leonard
"""
import numpy as np
import time
import random as rdm

def funcao(x):
    #ff = -(sum(fabs(x))*exp(-sum(x**2))) #sinal  negativo no início, pois queremos achar o mínimo da função
    ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))      
    return ff

def evolucao_diferencial(NP,D,F,G,CR):
    #Entradas do problema
    #   - NP=número de pontos (vetores)
    #   - D=Dimensão 
    #   - F=constante real entre [0,2]
    #   - G= número de gerações
    #   - CR= constante real definida pelo usuário no intervalo [0,1]
    #Outras variáveis
    #   - x = vetor alvo
    #   - v = vetor mutação
    #   - u = vetor combinação
    #   - li = número inteiro entre [0,D-1], representa um índice aleatoriamente escolhido
    #   - rj = número real aleatório entre [0,1]

    #criando vetores mutantes e de combinação com valores quaisquer    
   u,v,x=[],[],[]
   for i in range(NP):
        #v.append(rand(D))
        #u.append(rand(D))
        #x.append(rand(D))    
        v.append(array([uniform(-2,2),uniform(-2,2)]))
        u.append(array([uniform(-2,2),uniform(-2,2)]))
        x.append(array([uniform(-2,2),uniform(-2,2)]))
    #loop das gerações
   for k in range(G):
       for i in range(NP): #mutação
            #escolha e validação dos índices            
            r1=rdm.randint(0,NP-1)
            while (r1==i):
                r1=rdm.randint(0,NP-1)
            r2=rdm.randint(0,NP-1)
            while ((r2==i) or (r2==r1)):
                r2=rdm.randint(0,NP-1)
            r3=rdm.randint(0,NP-1)#    
            while ((r3==i) or (r3==r2) or (r3==r1)):
                r3=rdm.randint(0,NP-1)
            li=rdm.randint(0,D-1) #índice aleatoriamente escolhido
            rj=rdm.random()
            v[i]=x[r1]+F*(x[r3]-x[r2]) #mutação
            for j in range(D): #combinação
                if ((rj<=CR) or (j==li)):
                    u[i]=v[i]
                if ((rj>CR) and (j!=li)):
                    u[i]=x[i]
       for i in range(NP): #seleção
           if (funcao(u[i])<funcao(x[i])):
               x[i]=u[i]
    #pegar o vetor com menor valor da funcao
   Min=funcao(x[0])
   pos=0
   for i in range(1,NP):
       f=funcao(x[i])        
       if (f<Min):
           Min=f            
           pos=i
   #print "ED: ",x[pos],"f(x1,x2)= ",Min
   return x[pos]

ini=time.time()
tol=0.1
NP=40
D=2
CR=0.6
F=1.5
G=30
execucoes=30
vet_raizes=[]
vet_solucoes=[]
for i in range(execucoes):
    vet_raizes.append(rand(2))
    vet_raizes[i]=evolucao_diferencial(NP,D,F,G,CR)

for i in range(execucoes-1):
    for j in range(i+1,execucoes):
        if ((fabs(vet_raizes[i][0]-vet_raizes[j][0])<tol) and (fabs(vet_raizes[i][1]- vet_raizes[j][1]<tol))):
            vet_raizes[j][0]=0  #marcar como solução próxima
            vet_raizes[j][1]=0  #marcar como solução próxima    
        
k=0
for i in range(execucoes):
    if (vet_raizes[i][0]!=0):
        vet_solucoes.append(rand(2))        
        vet_solucoes[k]=vet_raizes[i]
        k=k+1

for k in range(len(vet_solucoes)):
    print vet_solucoes[k],funcao(vet_solucoes[k])

fim=time.time()
print "Tempo gasto: ",fim-ini
    
    
