# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 23:31:30 2012

@author: leonard
"""

class AG:
    """ Algoritmos genéticos """
    tamCrom=0
    def __init__(self,pMin=0.1,tamPop=6,txCr=2,txMut=0.1,numGer=4):
        self.pMin=pMin              #precisao mínima  
        self.tamPop=tamPop          #tamanho da população
        self.txCr=txCr              #taxa de cruzamento
        self.txMut=txMut            #taxa de mutação (em percentual)
        self.numGer=numGer          #número de gerações
        #self.funcao=funcao          #funcao proposta para ser resolvida
        #self.intervalo=intervalo    #intervalo de busca para a funcao
        #definir o intervalo das variáveis de cada função    
        
    #def f1(x):                   #funcão 1 proposta
    #    return ((x[0]-1)**2+(x[1]-1)**2-x[0]*x[1])
    #def f2(x):                  # funcao 2 proposta
    #    return (x[0]**2+3*x[1]**2-2*x[0]-2*x[1])
    def funcao(self,f,i):    
        
    def getDimensao(self,funcao):
        """Retorna a dimensão do problema de acordo com a função fornecida """    
        self.dimensao=len(funcao)        
        return self.dimensao
                
        #recebe funcao (f) e e os intervalos (i) das variaveis
    def getAmplitude(self,i):
        # i - vetor com intervalo de busca
        return sum(fabs(i))
        
       
    #def populacaoInicial():
        