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
    def __init__(self,NP=200,CR=0.7,F=1.1,G=150):
        """ #Entradas do problema
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
        """        
        self._tolerancia=0.9
        self._NP=NP
        self._D=3
        self._CR=CR
        self._F=F
        self._G=G
        self._execucoes=10
        self._vet_raizes=[]
        self.set_limites()

    def funcao(self,x):
        #ff = -(sum(fabs(x))*exp(-sum(x**2))) #sinal  negativo no início, pois queremos achar o mínimo da função
 #       ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))      
        #a=0.5
        #b=0.8
        #c=0.3
        #kp=604500
        #P=0.00243        
        """Constantes do problema """
        
        k1= 3e5*exp(-5000/x[1])
        k2 =6e7*exp(-7500/x[1]) 
        F0=1
        T0=300
        try:
            #ff=(a-((c+2*x[0])**2*(a+b+c-2*x[0])**2)/(x[1])-x[0])**2 + (x[1]-kp*P**2*(b-3*x[0])**3)**2
            """Assume-se do problema original que:
                X = x[0]
                T = x[1]
                h = x[2]
            """            
            f1=-0.16*x[0]*F0/x[2]+k1*(1-x[0])-k2*x[0]
            f2 =0.16*F0*T0/x[2]-0.16*x[1]*F0/x[2]+5*(k1*(1-x[0])-k2*x[0])
            f3 = 0.16*F0-0.4*sqrt(x[2])             
            ff=(f1**2)+(f2**2)+(f3**2)            
        except ZeroDivisionError:
            x[0]=0.5 #Condição do problema
            x[1]=500 #Condição do problema
            x[2]=0.5
        return ff        
    
    def evolucao_diferencial(self):
        #criando vetores mutantes e de combinação com valores quaisquer    
       u,v,x=[],[],[]
       for i in range(self._NP):
            v.append(self.set_pontos()) #escolhe um ponto dentre os limites estabelecidos
            u.append(self.set_pontos()) #escolhe um ponto dentre os limites estabelecidos
            x.append(self.set_pontos()) #escolhe um ponto dentre os limites estabelecidos
        #loop das gerações
       for k in range(self._G):
           for i in range(self._NP):
                #escolha e validação dos índices            
                r1=randint(self._NP)
                while (r1==i):
                    r1=randint(self._NP)
                r2=randint(self._NP)
                while ((r2==i) or (r2==r1)):
                    r2=randint(self._NP)
                r3=randint(self._NP)#    
                while ((r3==i) or (r3==r2) or (r3==r1)):
                    r3=randint(self._NP)
                li=randint(self._D) #índice aleatoriamente escolhido
                rj=rdm.random()
                ### MUTAÇÃO ###
                v[i]=x[r1]+self._F*(x[r3]-x[r2]) 
                ### COMBINAÇÃO ###                
                for j in range(self._D): 
                    if ((rj<=self._CR) or (j==li)):
                        u[i]=v[i]
                    if ((rj>self._CR) and (j!=li)):
                        u[i]=x[i]
           ### SELEÇÃO ###
           for i in range(self._NP):
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
    
    def set_pontos(self):
        """Retorna um ponto qualquer dentro dos limites [min,max] para cada variável estipulados em set_limites()"""
        n1=uniform(self._limites[0][0],self._limites[0][1])
        n2=uniform(self._limites[1][0],self._limites[1][1])        
        n3=uniform(self._limites[2][0],self._limites[2][1])
        _pt=array([n1,n2,n3])
        return _pt
        
    def set_limites(self):
        self._limites=[]        
        for i in range(self._D):
            self._limites.append(rand(2)) #array com duas posições, sendo a 1a o valor mínimo e a 2a o valor máximo
        #definição da área de busca para cada variável
        self._limites[0]=array([0,5]) #[min,max]
        self._limites[1]=array([200,700]) #[min,max]
        self._limites[2]=array([0,5]) #[min,max]
        return self._limites
    
    def get_solucoes(self):
        """ Obter k raízes em função da quantidade de execuções estabelecidas """
        #ini=time.time()
        self._vet_raizes=[]        
        for k in range(self._execucoes):
            self._vet_raizes.append(rand(self._D))
            self._vet_raizes[k]=self.evolucao_diferencial()
            print self._vet_raizes[k],self.funcao(self._vet_raizes[k])
    
    def filtro(self):
        """ Elimina as piores raízes repetidas."""         
        #FILTRO NOS PONTOS: eliminar as raízes que dão aproximadamente o mesmo valor de f(x)
        for i in range((self._execucoes)-1):
            for j in range(i+1,self._execucoes):
                if ((fabs(self._vet_raizes[i][0]-self._vet_raizes[j][0])<self._tolerancia) and (fabs(self._vet_raizes[i][1]- self._vet_raizes[j][1])<self._tolerancia) and (fabs(self._vet_raizes[i][2]- self._vet_raizes[j][2])<self._tolerancia)):
                    if (self.funcao(self._vet_raizes[j])<(self.funcao(self._vet_raizes[i]))): #Se a raiz j é a melhor, copiá-la para i
                        self._vet_raizes[i][0]=self._vet_raizes[j][0]  
                        self._vet_raizes[i][1]=self._vet_raizes[j][1]  
                        self._vet_raizes[i][2]=self._vet_raizes[j][2]  
                    self._vet_raizes[j][0]=0  #marcar como solução próxima
                    self._vet_raizes[j][1]=0  #marcar como solução próxima    
    
    def exibir_resultados(self):        
        self._qtdraiz=0        
        for i in range(self._execucoes):
            if (self._vet_raizes[i][0]!=0):
                self._qtdraiz=self._qtdraiz+1
                print self._vet_raizes[i],self.funcao(self._vet_raizes[i])
                arq=open('DE_Twoeq5.txt','a')
                #Formato (número de gerações, número de pontos, vetor de raízes, valor da função)            
                arq.write('%s %3s %.6f\n' %(self._vet_raizes[i], ' ', self.funcao(self._vet_raizes[i])))
                arq.close    
                
    def calculate(self):
        ini=time.time()        
        self.get_solucoes()
        #self.filtro()
        #self.exibir_resultados()
        fim=time.time()
        print fim-ini
        #arq=open('DE_Polymath_twoeq5.txt','a')
        #Formato (NP, CR, F, G, Tempo)            
        #arq.write('%d %.2f %.2f %d %f %d\n' %(self._NP, self._CR, self._F, self._G, fim-ini, self._qtdraiz))
        #arq.close
        
for i in range(1):
    d=ED()
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