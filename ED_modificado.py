# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 09:56:37 2012

@author: leonard
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:33:38 2012

@author: leonard
"""
import numpy as np
import time
import random as rdm
class ED:
    def __init__(self):
        self._tolerancia=0.2
        self._NP=20
        self._D=2
        self._CR=0.6
        self._F=1.5
        self._G=30
        self._execucoes=50
        self._vet_raizes=[]
        self._vet_solucoes=[]
        self.set_limites()

    def funcao(self,x):
        #ff = -(sum(fabs(x))*exp(-sum(x**2))) #sinal  negativo no início, pois queremos achar o mínimo da função
        ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))      
        return ff
    
    def evolucao_diferencial(self,NP,D,F,G,CR):
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
       for i in range(self._NP):
            v.append(self.set_pontos(self._limites[0],self._limites[1])) #escolhe um ponto dentre os limites estabelecidos
            u.append(self.set_pontos(self._limites[0],self._limites[1])) #escolhe um ponto dentre os limites estabelecidos
            x.append(self.set_pontos(self._limites[0],self._limites[1])) #escolhe um ponto dentre os limites estabelecidos
        #loop das gerações
       for k in range(self._G):
           for i in range(self._NP): #mutação
                #escolha e validação dos índices            
                r1=rdm.randint(0,self._NP-1)
                while (r1==i):
                    r1=rdm.randint(0,NP-1)
                r2=rdm.randint(0,self._NP-1)
                while ((r2==i) or (r2==r1)):
                    r2=rdm.randint(0,self._NP-1)
                r3=rdm.randint(0,self._NP-1)#    
                while ((r3==i) or (r3==r2) or (r3==r1)):
                    r3=rdm.randint(0,self._NP-1)
                li=rdm.randint(0,self._D-1) #índice aleatoriamente escolhido
                rj=rdm.random()
                v[i]=x[r1]+self._F*(x[r3]-x[r2]) #mutação
                for j in range(self._D): #combinação
                    if ((rj<=self._CR) or (j==li)):
                        u[i]=v[i]
                    if ((rj>self._CR) and (j!=li)):
                        u[i]=x[i]
           for i in range(self._NP): #seleção
               if (self.funcao(u[i])<self.funcao(x[i])):
                   x[i]=u[i]
        #pegar o vetor com menor valor da funcao
       Min=self.funcao(x[0])
       pos=0
       for i in range(1,self._NP):
           f=self.funcao(x[i])        
           if (f<Min):
               Min=f            
               pos=i
       #print "ED: ",x[pos],"f(x1,x2)= ",Min
       return x[pos]
    
    def set_pontos(self,_l_sup,_l_inf):
        """Configura as coordenadas de acordo com os valores limitantes estipulados"""
        n1=uniform(_l_inf,_l_sup)
        n2=uniform(_l_inf,_l_sup)        
        _pt=array([n1,n2])
        return _pt
        
    def set_limites(self):
        self._limites=array([-2.,2.]) #[min,max]    
    
    def get_solucoes(self):
        """ Obter k raízes em função da quantidade de execuções estabelecidas """
        #ini=time.time()
        for k in range(self._execucoes):
            self._vet_raizes.append(rand(self._D))
            self._vet_raizes[k]=self.evolucao_diferencial(self._NP,self._D,self._F,self._G,self._CR)
    
    def filtro(self):
        """ Elimina as piores raízes repetidas."""         
        #FILTRO NOS PONTOS: eliminar as raízes que dão aproximadamente o mesmo valor de f(x)
        for i in range((self._execucoes)-1):
            for j in range(i+1,self._execucoes):
                if ((fabs(self._vet_raizes[i][0]-self._vet_raizes[j][0])<self._tolerancia) and (fabs(self._vet_raizes[i][1]- self._vet_raizes[j][1])<self._tolerancia)):
                    if (self.funcao(self._vet_raizes[j])<(self.funcao(self._vet_raizes[i]))): #Se a raiz j é a melhor, copiá-la para i
                        self._vet_raizes[i][0]=self._vet_raizes[j][0]  
                        self._vet_raizes[i][1]=self._vet_raizes[j][1]  
                    self._vet_raizes[j][0]=0  #marcar como solução próxima
                    self._vet_raizes[j][1]=0  #marcar como solução próxima    
    
    def exibir_resultados(self):        
        for i in range(self._execucoes):
            if (self._vet_raizes[i][0]!=0):
                print self._vet_raizes[i],self.funcao(self._vet_raizes[i])
#                arq=open('LJ.txt','a')
                #Formato (nint, nout, contract, raiz, solução)            
 ##              arq.close    
    
    def calculate(self):
        ini=time.time()        
        self.get_solucoes()
        self.filtro()
        self.exibir_resultados()
        fim=time.time()
        print fim-ini
        #arq=open('LJ.txt','a')
        #Formato (nint, nout, contract, raiz, solução)            
        #arq.write('%f\n' %(fim-ini))
        #arq.close
        
d=ED()
d.calculate()