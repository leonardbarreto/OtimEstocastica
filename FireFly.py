# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 07:31:46 2012

@author: leonard
"""

class FireFly:
    # Parâmetros importantes do algoritmo
    #   - r -> distãncia euclidiana entre os vagalumes i e j, sendo i o mais brilhante e j o menos brilhante
    #   - _gama     -> coeficiente (real) de absorçao de luz pelo meio
    #   - _beta     -> fator de atratividade    
    def __init__(self):
        self._dimen=2                  #dimensão do problema
        self._qtd_fireflies=6
        self._gama=0                  #coeficiente (real) de absorçao de luz pelo meio
        self._n_geracoes=100             #número de gerações
        self.set_populacao_inicial(self._dimen,self._qtd_fireflies)
    
    def funcao(self,x):
        """ Definição da função objetivo do problema proposto """
        return -(sum(fabs(x))*exp(-sum(x**2))) # Minimizar (sinal negativo)
        
    def set_intensidade_emitida_de_luz(self,_pFflies):
        """ Criar e calcular a intensidade de emissão de luz de cada firefly. A intensidade de luz (Ii) de cada firefly (FFi) é determinado pelo valor f(xi). 
            Parâmetros:
                - _pFflies -> populacao de fireflies"""
        self._intensidade_luz=[]
        for i in range(self._qtd_fireflies):
            self._intensidade_luz.append(self.funcao(_pFflies[i]))
    
    def calcular_intensidade_percebida_de_luz(self,_pR,_pGama):
        """ Calcular a intensidade percebida de luz de cada firefly em relação aos demais. 
            Parâmetros:
                - _pR    -> distância(euclidiana) entre os fireflies
                - _pGama -> absorção da luz pelo meio 
        """
        
            
    def set_populacao_inicial(self,_p_dimen,_p_qtdff):
        """ Cria e inicializa a população de fireflies e a respectiva intensidade de luz, composta por n fireflies(vetores).
            Parãmetros:
                - _p_dimen -> dimensão do problema
                - _p_qtdff -> Quantidade de fireflies do problema
        """        
        self._fFlies=[]  #população de fireflies
        for i in range(_p_qtdff): #criar quantidade de fireflies definida...
            self._fFlies.append(rand(_p_dimen)) #...atribuindo valores reais para cada um entre 0..1
        self.set_intensidade_de_luz(self._fFlies)
        
    def get_populacao_fireflies(self):
        return self._fFlies
    
    def get_intensidade_de_luz(self):
        return self._intensidade_luz
    
    def set_distancia_euclidiana(self,_fforig,_ffdest):
        """ Retorna a distância euclidiana entre o firefly origem e destino.
            Parâmetros:
                - _fforig -> coordenada do firefly de origem
                - _ffdest -> coordenada do firefly de destino
            Retorno:
                - _r -> distância euclidiana entre os dois pontos
        """
       _r=0
       for j in range(self._dimen): #calcula em função da dimensão do problema
           _r=_r+((_fforig[j]-_ffdest[j])**2)
       _r=sqrt(_r)
       return _r
       # rij - Distãncia r entre o firefly(i) e o firefly(j)
        
        