# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 10:34:18 2012

@author: leonard
"""

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
    def __init__(self,NP=50,CR=0.6,F=1.5,G=15):
        self._tolerancia=0.2
        self._NP=NP
        self._D=2
        self._CR=CR
        self._F=F
        self._G=G
        self._rho=0.9
        self._xp=0
        self._beta=10000
        self._dist=2
        self._execucoes=10
        self._vet_raizes=[]
        self._vet_solucoes=[]
        self.set_limites()

    def funcao(self,x):
        if (len(self._vet_raizes)==1):    #não computa para a primeira raiz    
            self._xp=0
        else:
            if (self.ponto_proximo(x)==True):
                self._xp=1
            else:
                self._xp=0      
                
        fo = -(sum(fabs(x))*exp(-(sum(x**2)))) #sinal  negativo no início, pois queremos achar o mínimo da função
        #ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))    
        fp=self._beta*(exp(1)**(-(self._dist))*self._xp*(self._dist))
        ff=fo+fp        
        return ff
    
    def funcao2(self,x):
        return -(sum(fabs(x))*exp(-(sum(x**2))))
        
    
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
    
    def ponto_proximo(self,vetx):
        """ Retona True(1) se existe uma raiz próxima a este vetor passado como parâmetro"""
        self._dist=0        
        resp = False
        for j in range(0,len(self._vet_raizes)-1):
            self._dist=self._dist+self.dist_euclideana(vetx,self._vet_raizes[j])
            if (self._dist<self._rho):   #Se ponto próximo, ativar a variável para perturbar a função
                resp = True
        return resp
        
    def dist_euclideana(self,p,q):
        """ Norma L2 """
        res=0
        for i in range(self._D):
            res=(sum((p-q)**2))
        #soma= sqrt(((p[0]-q[0])**2)+((p[1]-q[1])**2))
        return sqrt(res)

    def exibir_resultados(self):        
        self._qtdraiz=0        
        for i in range(self._execucoes):
            if (self._vet_raizes[i][0]!=0):
                self._qtdraiz=self._qtdraiz+1                
                print self._vet_raizes[i],self.funcao2(self._vet_raizes[i])
                #Gravando resultados em arquivo            
                arq=open('DE_hirsch.txt','a')
                #Formato (número de gerações, número de pontos, vetor de raízes, valor da função)            
                #arq.write('%15d %d %s %f\n' %(self._G, self._NP, self._vet_raizes[i], self.funcao2(self._vet_raizes[i])))
                arq.write('%30s %s %3s %.6f\n' %(' ', self._vet_raizes[i], ' ', self.funcao2(self._vet_raizes[i])))                
                arq.close    
    
    def calculate(self):
        ini=time.time()        
        self.get_solucoes()
        self.filtro()
        self.exibir_resultados()
        fim=time.time()
        print fim-ini
        arq=open('DE_hirsch.txt','a')
        #Formato (nint, nout, contract, raiz, solução)            
        #arq.write('%f\n' %(fim-ini))
        arq.write('%d %.2f %.2f %d %f %d\n' %(self._NP, self._CR, self._F, self._G, fim-ini, self._qtdraiz))
        arq.close
        
for i in range(30):
    d=ED(40,0.2,1.1,20)
    d.calculate()
    del(d)

#Executar para diversos valores de atributos
#for n in [20,30,40,50]:
#    for c in [0.2, 0.4, 0.6]:
#        for f in [1.1, 1.3, 1.5, 1.7]:
#            for g in [15, 20, 25]:
#                d=ED(n,c,f,g)
#                d.calculate()
#                del(d)

