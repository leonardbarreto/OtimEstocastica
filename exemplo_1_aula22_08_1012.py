# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:47:24 2012

@author: leonard
@codigo: implementação de algoritmos Luus - Jaakola 
"""
import numpy as np

def funcao(x):
    ff = x[0]**2 +x[1]**2
    return ff
    
def luus_jaakola(nint,nout,raios,contract,dimen):
    x0 = rand(dimen) #x0 é um vetor de tamanho dimen
    for i in range(nout):
        for j in range(nint):
            novox = x0 + raios*(rand(dimen)-0.5)
            if funcao(novox)<funcao(x0):
                x0=novox
        raios = (1-contract)*raios
    return x0