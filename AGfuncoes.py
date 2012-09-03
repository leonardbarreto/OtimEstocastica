# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 12:51:10 2012

@author: leonard
"""

class Funcoes:
    def __init__(self,dimensao=0):
        self.setDimensao()
        self.setIntervalo(self.dimensao)
    def setDimensao(self):
        self.dimensao=2;
    def getDimensao(self):
        return self.dimensao
    def setIntervalo(self,dimen):
        x=[]                        #cria lista vazia
        for i in range(dimen):      #cria lista de arrays com valores nulos de tamanho dimen
            x.append(zeros(dimen)) 
        x[0][0]=-5.12
        x[0][1]=5.12
        x[1][0]=-5.12
        x[1][1]=5.12
        self.intervalo=x
    def getIntervalo(self):
        return self.intervalo
    def Funcao(self,x):
        #x é um array de tamanho dimen
        self.f=((x[0]-1)**2+(x[1]-1)**2-x[0]*x[1])