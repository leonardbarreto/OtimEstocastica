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
        self._fFlies=[]                 #população de fireflies        
        self._dimen=2                   #dimensão do problema
        self._qtd_fireflies=6
        self._gama=0                    #coeficiente (real) de absorçao de luz pelo meio
        self._alfa=(float)(rand(1))     #parâmetro de randomização para a movimentação de um firefly
        self._n_geracoes=100            #número de gerações
        self._beta0=1                   #Atratividade para distância r=0
        self.set_populacao_inicial(self._dimen,self._qtd_fireflies)
    
    def funcao(self,x):
        """ Definição da função objetivo do problema proposto """
        #return -(sum(fabs(x))*exp(-sum(x**2))) # Minimizar (sinal negativo)
        return (x[0]**2)+x[1]
    def set_intensidade_emitida_de_luz(self,_pFflies):
        """ Criar e calcular a intensidade de emissão de luz de cada firefly. A intensidade de luz (Ii) de cada firefly (FFi) é determinado pelo valor f(xi). 
            Parâmetros:
                - _pFflies -> populacao de fireflies"""
        _int_luz=[]
        for i in range(self._qtd_fireflies):
            _int_luz.append(self.funcao(_pFflies[i]))
        self._intensidade_de_luz=_int_luz
    
    def get_intensidade_emitida_de_luz(self):
        return self._intensidade_de_luz
    
    def calcular_fator_de_atratividade(self):
        #calcular a distância euclidiana entre os vagalumes mais e menos brilhante.
        _ffMaisBri=self.get_mais_brilhante(self._intensidade_de_luz)        
        _ffMenosBri=self.get_menos_brilhante(self._intensidade_de_luz)
        self._r=self.set_distancia_euclidiana(_ffMaisBri,_ffMenosBri)
        beta=self._beta0*exp(-self._gama*(self._r**2))
        return beta
        
    def calcular_intensidade_percebida_de_luz(self,_pR,_pGama):
        """ Calcular a intensidade percebida de luz de cada firefly em relação aos demais. 
            Parâmetros:
                - _pR    -> distância(euclidiana) entre os fireflies
                - _pGama -> absorção da luz pelo meio 
        """
        
    def calculate(self):
        for i in range(self._qtd_fireflies):
            for j in range(i,self._qtd_fireflies):
                if (self._intensidade_de_luz[j]>self._intensidade_de_luz[i]): #Se algum firef
                    self.set_movimentar_firefly(i,j)
                #atualizar a luminosidade
                    
    def set_movimentar_firefly(self,_de,_para):
        """ Reliza a movimentação(atualiza coordenadas) de um firefly para o mais luminoso de acordo com a fórmula. """        
        _beta=self.calcular_fator_de_atratividade()
        return self._fFlies[_de]=self._fFlies[_de]+_beta*(self._fFlies[_para]-self._fFlies[_de])+self._alfa((int)rand(1)-0.5)
                
    def set_populacao_inicial(self,_p_dimen,_p_qtdff):
        """ Cria e inicializa a população de fireflies e a respectiva intensidade de luz, composta por n fireflies(vetores).
            Parãmetros:
                - _p_dimen -> dimensão do problema
                - _p_qtdff -> Quantidade de fireflies do problema
        """        
        
        for i in range(_p_qtdff):               #criar quantidade de fireflies definida...
            self._fFlies.append(rand(_p_dimen)) #...atribuindo valores reais para cada um entre 0..1
        self.set_intensidade_emitida_de_luz(self._fFlies)
        
    def get_populacao_fireflies(self):
        return self._fFlies
    
    def get_intensidade_de_luz(self):
        return self._intensidade_luz
    
    def get_mais_brilhante(self,_p_iel):
        """ Retorna o firefly mais brilhante, ou seja, com maior valor na função objetivo.
            Parâmetros:
                - _p_iel -> Intensidade Emitida de Luz de cada firefly (vetor)
            Retorno:
                - _pMab -> Identifica o firefly mais brilhante (posição)
        """
        _pMab=0                         # posição do mais brilhante
        _vMab=self.funcao(_p_iel[0])    # valor do mais brilhante
        for i in range(1,self._qtd_fireflies):
            _v=self.funcao(_p_iel[i])            
            if (_v>_pMab):
                _pMab=i
                _vMab=_v
        return _vMab
                        
    def get_menos_brilhante(self,_p_iel):
        """ Retorna o firefly menos brilhante, ou seja, com maior valor na função objetivo.
            Parâmetros:
                - _p_iel -> Intensidade Emitida de Luz de cada firefly (vetor)
            Retorno:
                - _vmeb -> Intensidade de brilho (valor da função objetivo) do respectivo firefly
        """
        _pmeb=0                         # posição do menos brilhante
        _vmeb=self.funcao(_p_iel[0])    # valor do mais brilhante
        for i in range(1,self._qtd_fireflies):
            _v=self.funcao(_p_iel[i])            
            if (_v<_pmeb):
                _pmeb=i
                _vmeb=_v
        return _vmeb
        
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
        
        