# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:47:24 2012

@author: Leonard Barreto
@codigo: implementação de algoritmos Luus - Jaakola 
"""
"""
Obtenção dos mínimos globais utilização o algoritmo Luus-Jaakola:
   Modificação:
       Definição de um array de raízes;
       Definição de um array de soluções;
       
       Executar o algoritmo com a finalidade de gerar um conjunto de soluções iniciais próximas do ideal. O critério para escolha dos parâmetros:
           - Número considerável de execuções com a finalidade de gerar uma boa quantidade de soluções candidatas.
       Aplicar um filtro para eliminar as raízes repetidas do array. O critério de igualdade é de acordo com uma proximidade (self._toleranciaerância) definida a priori.
       A partir das Soluções Iniciais, executar novamente o Luus-Jaakola para obtenção do vetor de soluções finais, onde:
           o vetor de solução inicial do LJ são os vetores resultantes do filtro.
           a quantidade de loops é em função da quantidade de soluções iniciais.
       Ao final, um novo filtro é realizado no array de soluções finais de modo a eliminar resultados iguais.
"""
import numpy as np
import time
import random
class LJ:
    def __init__(self):
        self._x1=[] 
        self._x2=[] 
        self.raios=[]
        self._vnint=100
        self._vnout=100
        self._contract=0.01
        self._execucoes=30
        self._tolerancia=0.1
        self._dimensao=2
        self._limites=[]
        self._vet_raizes=[]
        self.set_raios()
        self.set_limites()
        
    def funcao(self,x):
        #ff = -(fabs(sum(x))*exp(-sum(x**2)))
        ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))    
        #ff=((x[0] - x[1])**2 + (x[0]**2 + x[1]**2 - 1)**2)
        
        #ff = (x[0]**3 - 3*x[0]**2 - x[1] + 2)**2 + ((x[0] - 1)**2 + x[1]**2 - 4)**2 #FUNCÃO
        #minimo = (2.4142137; -1.4142134)
        #minimo = (1.7653669; -1.8477590)
        #minimo = (0.2346331; 1.8477590)
        #minimo = (2.8477590; 0.7653669)
        #minimo = (-0.4142136; 1.4142135)
        #minimo = (-0.8477591; -0.7653669)
        return ff
    
    def funcao2(self,x):
        """ Funcao adaptada para a técnica de penalização de funções. Variáveis:
            β (beta) =  constante suficientemente grande
            ρ (ro) = constante pequena
            δ (delta) = distância entre coordenadas """
        
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
            #print self.luus_jaakola(vx0,5,50,self.raios,self._contract,2)
            self._vet_raizes[k]=self.luus_jaakola(vx0,self._vnout,self._vnint,self.raios,self._contract,2)
    
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
    
    def calculate(self):
        ini=time.time()        
        self.get_solucoes()
        self.filtro()
        self.exibir_resultados()
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
    
