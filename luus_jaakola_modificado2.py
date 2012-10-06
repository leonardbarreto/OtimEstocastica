# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 10:12:51 2012

@author: leonard
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:47:24 2012

@author: Leonard Barreto
@codigo: implementação de algoritmos Luus - Jaakola 
"""
"""
Obtenção dos mínimos globais utilização o algoritmo Luus-Jaakola:
   Modificação:
       Perturbação da função. (Adaptative optimization problem (HIRSCH))
"""
import numpy as np
import time
import random
class LJ:
    def __init__(self):
        self._x1=[] 
        self._x2=[] 
        self.raios=[]
        self._vnint=70
        self._vnout=15
        self._contract=0.01
        self._execucoes=20
        self._tolerancia=0.1
        self._dimensao=2
        self._limites=[]
        self._vet_raizes=[]
        self.set_raios()
        self.set_limites()
        self._beta=100
        self._ro=1.8
        self._dist=2    #distância
        
    def funcao(self,x):
        """ Funcao adaptada para a técnica de penalização de funções. Variáveis:
            β (beta) =  constante suficientemente grande
            ρ (ro) = constante pequena
            δ (delta) = distância entre coordenadas 
            fo - função original
            fp - função perturbação
        """
        if (self._dist<=self._ro):
            xp=1
        else:
            xp=0
        fo=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))
        fp=(exp(1)**(-(self._dist))*xp*(self._dist))
        ff=fo+fp
        return ff
        
    def set_limites(self):
        #[min,max]    
        self._limites=array([-6.,6.])
        
    def set_raios(self):    
        self.raios=array([-0.5,0.5])#Cria array com duas posicões
        return self.raios
        
    def atualizar_limites(self):
        """Contrair os limites das variáveis em relação à contração da área de busca """
        self._limites[0]=self._limites[0]-(self._limites[0]*self._contract)
        self._limites[1]=self._limites[1]-(self._limites[1]*self._contract)
        #print self._limites
        
    def get_solucoes(self):
        #ini=time.time()
        for k in range(self._execucoes):
            self._vet_raizes.append(rand(self._dimensao))
            self.set_limites()            
            vx0=self.set_pontos(self._limites[0],self._limites[1]) #escolhe um ponto dentre os limites estabelecidos
            if (k>0):
                self._dist=self.dist_euclideana(self._vet_raizes[k-1],self._vet_raizes[k])
                #print self._dist
            self._vet_raizes[k]=self.luus_jaakola(vx0,self._vnout,self._vnint,self.raios,self._contract,2)
            print self._vet_raizes[k],self.funcao(self._vet_raizes[k])
            
    def exibir_resultados(self):        
        for i in range(self._execucoes):
            if (self._vet_raizes[i][0]!=0):
                print self._vet_raizes[i],self.funcao(self._vet_raizes[i])
        
    def set_pontos(self,_l_sup,_l_inf):
        """Configura as coordenadas de acordo com os valores limitantes estipulados"""
        n1=uniform(_l_inf,_l_sup)
        n2=uniform(_l_inf,_l_sup)        
        _pt=array([n1,n2])
        return _pt
    
    def luus_jaakola(self,x0,nout,nint,raios,contract,dimen):
        #x0 = rand(dimen) #x0 é um vetor de tamanho dimen
        for i in range(nout):
            for j in range(nint):
                novox = x0 + raios*(rand(dimen)-0.5)
                if self.funcao(novox)<self.funcao(x0):
                    x0=novox
            raios = (1-contract)*raios
            self.atualizar_limites()
        return x0
    
    def dist_euclideana(self,p,q):
        """ Norma L2 """
        for i in range(self._dimensao):
            res=sqrt(sum((p-q)**2))
        #soma= sqrt(((p[0]-q[0])**2)+((p[1]-q[1])**2))
        return res
        
        
    def calculate(self):
        ini=time.time()        
        self.get_solucoes()
        #self.exibir_resultados()
        fim=time.time()
        print fim-ini
    
    #fim=time.time()
    #print fim-ini
    #raios - espaço de busca
    def grava_resultados():
        arq=open('teste.txt','a')
        x=19.9
        y=1.5
        arq.write('Valores: %f %f' %(x, y))
        arq.write('%s' %vet_solucoesfinal)
        arq.close
    #grava_resultados()
    
l=LJ()
l.calculate()
"""    
    def filtro(self,tol):
        print len(self._vet_raizes)
        print self._vet_raizes
        i=0
        tam=len(self._vet_raizes)
        while (i<tam):
            print "Raiz %d " %i            
            j=i+1
            while (j<tam):
                if (fabs(self._vet_raizes[i][0]-self._vet_raizes[j][0])<tol and fabs(self._vet_raizes[i][0]-self._vet_raizes[j][1])<tol):
                    print self._vet_raizes[j]                    
                    del self._vet_raizes[j]
                    j=j-1                    
                    tam=len(self._vet_raizes)
                    print "!"
                j=j+1
            i=i+1
            tam=len(self._vet_raizes)
        print len(self._vet_raizes)
        print self._vet_raizes
"""
    
