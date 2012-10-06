# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:47:24 2012

@author: leonard
@codigo: implementação de algoritmos Luus - Jaakola 
"""
import numpy as np

def funcao(x):
    #ff = x[0]**2 +x[1]**2
    ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))    
    return ff
    
def luus_jaakola(nint,nout,raios,contract,dimen):
    #x0 = rand(dimen) #x0 é um vetor de tamanho dimen
    x0 = array([-2,2])    
    for i in range(nout):
        for j in range(nint):
            novox = x0 + raios*(rand(dimen)-0.5)
            if funcao(novox)<funcao(x0):
                x0=novox
        raios = (1-contract)*raios
    return x0
    
nint=50
nout=10
raios=[]
raios=rand(2)
raios=array([-0.5,0.5])
print raios
#raios[0][1]=-2
contract=0.05
dimen=2
print luus_jaakola(nint,nout,raios,contract,dimen)