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
        self._qtd_raizes=4
        self._vnint=50
        self._vnout=20
        self._contract=0.05
        self._dimensao=2
        self._limites=[]
        self._vet_raizes=[]
        self.set_raios()
        self.set_limites()
        self._beta=100000
        self._rho=0.6
        self._dist=2    #distância
        self._xp=0
        
    def funcao(self,x):
        """ Funcao adaptada para a técnica de penalização de funções. Variáveis:
            β (beta) =  constante suficientemente grande
            ρ (ro) = constante pequena
            δ (delta) = distância entre coordenadas 
            fo - função original
            fp - função perturbação
        """
        if (len(self._vet_raizes)==1):    #não computa para a primeira raiz    
            self._xp=0
        else:
            if (self.ponto_proximo(x)==True):
                self._xp=1
            else:
                self._xp=0
        
        fo=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))
        fp=self._beta*(exp(1)**(-(self._dist))*self._xp*(self._dist))
        ff=fo+fp
        return ff
        
    def funcao2(self,x):
        ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))
        return ff
        
    def set_limites(self):
        #[min,max]    
        self._limites=array([-2.,2.])
        
    def set_raios(self):    
        self.raios=array([-0.5,0.5])#Cria array com duas posicões
        return self.raios
        
    def atualizar_limites(self):
        """Contrair os limites das variáveis em relação à contração da área de busca """
        self._limites[0]=self._limites[0]-(self._limites[0]*self._contract)
        self._limites[1]=self._limites[1]-(self._limites[1]*self._contract)
        #print self._limites
        
    def get_raizes(self):
        for k in range(self._qtd_raizes):
            vx0=self.set_pontos(self._limites[0],self._limites[1]) #escolhe um ponto dentre os limites estabelecidos
            if (len(self._vet_raizes)>0):
                while (self.ponto_proximo(vx0)==True):   #Escolher um ponto inicial q nao seja uma raiz          
                    vx0=self.set_pontos(self._limites[0],self._limites[1]) #escolhe um ponto dentre os limites estabelecidos
                    #self.ponto_proximo(vx0)
            self._vet_raizes.append(vx0)
            self._vet_raizes[k]=self.luus_jaakola(vx0,self._vnout,self._vnint,self.raios,self._contract,2)            
            print "Raiz " ,k,self._vet_raizes[k]
            
    def exibir_resultados(self):        
        self._xp=0  #desligar a chave        
        for i in range(self._qtd_raizes):
            print self._vet_raizes[i],self.funcao2(self._vet_raizes[i])
            #Gravando resultados em arquivo            
            arq=open('LJ_hirsch.txt','a')
            #Formato (nint, nout, contract, raiz, solução)            
            arq.write('%15d %d %f %s %f\n' %(self._vnout, self._vnint, self._contract, self._vet_raizes[i], self.funcao2(self._vet_raizes[i])))
            arq.close
            
        
    def set_pontos(self,_l_sup,_l_inf):
        """Configura as coordenadas de acordo com os valores limitantes estipulados"""
        n1=uniform(_l_inf,_l_sup)
        n2=uniform(_l_inf,_l_sup)        
        _pt=array([n1,n2])
        return _pt
    
    def ponto_proximo(self,vetx):
        """ Retona True(1) se existe uma raiz próxima a este vetor passado como parâmetro"""
        self._dist=0        
        resp = False
        for j in range(0,len(self._vet_raizes)-1):
            self._dist=self._dist+self.dist_euclideana(vetx,self._vet_raizes[j])
            if (self._dist<self._rho):   #Se ponto próximo, ativar a variável para perturbar a função
                resp = True
        return resp

    def luus_jaakola(self,x0,nout,nint,raios,contract,dimen):
        #x0 = rand(dimen) #x0 é um vetor de tamanho dimen
        for i in range(nout):
            for j in range(nint):
                novox = x0 + raios*(rand(dimen)-0.5)
                if (self.funcao(novox)<self.funcao(x0)):
                    x0=novox
            raios = (1-contract)*raios
            self.atualizar_limites()
        return x0
    
    def dist_euclideana(self,p,q):
        """ Norma L2 """
        res=0
        for i in range(self._dimensao):
            res=(sum((p-q)**2))
        #soma= sqrt(((p[0]-q[0])**2)+((p[1]-q[1])**2))
        return sqrt(res)
        
        
    def calculate(self):
        ini=time.time()        
        self.get_raizes()
        self.exibir_resultados()
        fim=time.time()
        print fim-ini
        arq=open('LJ_hirsch.txt','a')
        #Formato (nint, nout, contract, raiz, solução)            
        arq.write('%f\n' %(fim-ini))
        arq.close
    
    #fim=time.time()
    #print fim-ini
    #raios - espaço de busca
    def grava_resultados():
        arq=open('teste.txt','a')
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
    
