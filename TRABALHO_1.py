# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:47:24 2012

@author: leonard
@codigo: implementação de algoritmos Luus - Jaakola 
"""
import numpy as np
import random as rdm
import math

def funcao(x):
    ff = -(sum(fabs(x))*exp(-sum(x**2))) #sinal  negativo no início, pois queremos achar o mínimo da função
    #ff = -(sum(fabs(x))*exp(-sum(np.power(x,x))))   
    return ff
    
def luus_jaakola(nint,nout,raios,contract,dimen):
    #nint - número de iterações interna
    #nout - númoer de iterações externa
    #raios - vetor de dimensão 'dimen' com números entre -0.5 e 0.5
    #contract - número pequeno
    #dimen -dimensao do problema
    x0 = rand(dimen) #x0 é um vetor de tamanho dimen
    for i in range(nout):
        for j in range(nint):
            novox = x0 + raios*(rand(dimen)-0.5)
            if funcao(novox)<funcao(x0):
                x0=novox
        raios = (1-contract)*raios
    print "Luus_jaakola: ",x0, "f(x1,x2)= ",funcao(x0)
    return x0
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
def evolucao_diferencial(NP,D,F,G,CR):
    #criando vetores mutantes e de combinação com valores quaisquer    
    v=rand(NP*D)
    v.shape=(NP,D)    
    u=rand(NP*D)
    u.shape=(NP,D)    
    #criar vetor target xi - população inicial    
    for i in range(NP):
        x=rand(NP*D)
        x.shape=(NP,D)
    print "1)x",x,"\nv",v,"\nu",u
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
            r3=rdm.randint(0,NP-1)
            while ((r3==i) or (r3==r2) or (r3==r1)):
                r3=rdm.randint(0,NP-1)
            li=rdm.randint(0,D-1) #índice aleatoriamente escolhido
            rj=rdm.random()
            v[i]=x[r1]+F*(x[r3]-x[r2])
            for j in range(D): #combinação
                if ((rj<=CR) or (j==li)):
                    u[i]=v[i]
                if ((rj>CR) and (j!=li)):
                    u[i]=x[i]
        for i in range(NP):  #seleção      
            if (funcao(u[i])<funcao(x[i])):
                x[i]=u[i]
    #pegar o vetor com menor valor da funcao
    Min=funcao(x[0])
    pos=0
    for i in range(NP):
        f=funcao(x[i])        
        if (f<Min):
            Min=f            
            pos=i
    print "ED: ",x[pos],"f(x1,x2)= ",Min
    return 0

def evolucao_diferencial2(NP,D,F,G,CR):
    #criando vetores mutantes e de combinação com valores quaisquer    
   u,v,x=[],[],[]
   for i in range(NP):
        v.append(rand(D))
        u.append(rand(D))
        x.append(rand(D))    
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
   print "ED: ",x[pos],"f(x1,x2)= ",Min
   return x[pos]

NP=7
D=2
CR=0.6
F=1.5
G=1000
evolucao_diferencial2(NP,D,F,G,CR)
nint=3
nout=4
contract=0.2
dimen=2
raios=rand(dimen)-2
luus_jaakola(nint,nout,raios,contract,dimen)
