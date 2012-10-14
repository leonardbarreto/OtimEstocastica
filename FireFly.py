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
        self._gama=uniform(0.01,100)    #coeficiente (real) de absorçao de luz pelo meio
        self._alfa=(float)(rand(1))     #parâmetro de randomização para a movimentação de um firefly
        self._n_geracoes=100          #número de gerações
        self._beta0=1                   #Atratividade para distância r=0
        self.set_limites()        
        self.set_populacao_inicial(self._dimen,self._qtd_fireflies)
        
    
    def funcao(self,x):
        """ Definição da função objetivo do problema proposto """
        ff= -(sum(fabs(x))*exp(-sum(x**2))) # Minimizar (sinal negativo)
        #ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))    
        #return (x[0]**2)+x[1]
        return ff
        
    def set_intensidade_emitida_de_luz(self,_pFflies):
        """ Criar e calcular a intensidade de emissão de luz de cada firefly. A intensidade de luz (Ii) de cada firefly (FFi) é determinado pelo valor f(xi). 
            Parâmetros:
                - _pFflies -> populacao de fireflies"""
        for i in range(self._qtd_fireflies):
            self._luminosidade[i]=(self.funcao(_pFflies[i]))
    
    def get_intensidade_emitida_de_luz(self):
        return self._luminosidade
    
    def set_pontos(self,_l_sup,_l_inf):
        """Configura as coordenadas de acordo com os valores limitantes estipulados"""
        n1=uniform(_l_inf,_l_sup)
        n2=uniform(_l_inf,_l_sup)        
        _pt=array([n1,n2])
        return _pt    
    
    def set_limites(self):
        self._limites=array([-2.,2.]) #[min,max] 

    def get_limites(self):
        return self._limites        
        
    def calcular_fator_de_atratividade(self):
        """ Calcular o fator de atratividade entre os firefly mais brilhante e o menos brilhante.
            Requisitos:
                - Obter o firefly mais brilhante e o menos brilhante através da avaliação dos valores do vetor _luminosidade
                - Calcular a distância euclideana entre os dois fireflies
                - Aplicar a fórmula com os seguintes parãmetros:
                    * _beta0-> coeficiente de atratividade
                    * _gama -> coeficiente de absorção de luz
                    * _r    -> distância euclideana entre os dois pontos
        """
        _ffMaisBri=self.get_mais_brilhante(self._luminosidade)        
        _ffMenosBri=self.get_menos_brilhante(self._luminosidade)
        self._r=self.set_distancia_euclidiana(_ffMaisBri,_ffMenosBri)
        beta=self._beta0*exp(1)**(-self._gama*(self._r**2))
        return beta
        
    def set_movimentar_firefly(self,_de,_para):
        """ Reliza a movimentação(atualiza coordenadas) de um firefly para o mais luminoso de acordo com a fórmula. """        
        _beta=self.calcular_fator_de_atratividade()
        self._fFlies[_de]=self._fFlies[_de]+_beta*(self._fFlies[_para]-self._fFlies[_de])+self._alfa*((float)(rand(1)-0.5))
            
    def set_populacao_inicial(self,_p_dimen,_p_qtdff):
        """ Cria e inicializa a população de fireflies e a respectiva intensidade de luz, composta por n fireflies(vetores).
            Parãmetros:
                - _p_dimen -> dimensão do problema
                - _p_qtdff -> Quantidade de fireflies do problema
        """        
        self.get_limites()
        self._luminosidade=[]
        for i in range(_p_qtdff):               #criar quantidade de fireflies definida...
            self._fFlies.append(rand(_p_dimen)) #...atribuindo valores reais para cada um entre 0..1
            #self._fFlies.append(self.set_pontos(self._limites[0],self._limites[1]))            
            self._luminosidade.append(0)          #criando um vetor nulo para armazenar informações sobre a luminosidade de cada firefly
        self.set_intensidade_emitida_de_luz(self._fFlies)
        
    def get_populacao_fireflies(self):
        return self._fFlies
    
    def get_luminosidade(self):
        return self._intensidade_luz
    
    def get_mais_brilhante(self,_p_iel):
        """ Retorna a posição do firefly mais brilhante, ou seja, com maior valor na função objetivo.
            Parâmetros:
                - _p_iel -> Intensidade Emitida de Luz de cada firefly (vetor)
            Retorno:
                - _pMab -> Identifica o firefly mais brilhante (posição)
        """
        _pMab=0                         # posição do mais brilhante
        _vMab=self.funcao(_p_iel[0])    # valor do mais brilhante
        for i in range(1,self._qtd_fireflies):
            _v=self.funcao(_p_iel[i])            
            if (_v>_vMab):
                _pMab=i
                _vMab=_v
        return _pMab
                        
    def get_menos_brilhante(self,_p_iel):
        """ Retorna a posição do firefly menos brilhante, ou seja, com maior valor na função objetivo.
            Parâmetros:
                - _p_iel -> Intensidade Emitida de Luz de cada firefly (vetor)
            Retorno:
                - _vmeb -> Intensidade de brilho (valor da função objetivo) do respectivo firefly
        """
        _pmeb=0                         # posição do menos brilhante
        _vmeb=self.funcao(_p_iel[0])    # valor do mais brilhante
        for i in range(1,self._qtd_fireflies):
            _v=self.funcao(_p_iel[i])            
            if (_v<_vmeb):
                _pmeb=i
                _vmeb=_v
        return _pmeb
        
    def set_distancia_euclidiana(self,_fforig,_ffdest):
        """ Retorna a distância euclidiana entre o firefly origem e destino.
            Parâmetros:
                - _fforig -> coordenada do firefly de origem
                - _ffdest -> coordenada do firefly de destino
            Retorno:
                - _de -> distância euclidiana entre os dois pontos
        """
        _de=0
        for j in range(self._dimen): #calcula em função da dimensão do problema
            _de=_de+((self._fFlies[_fforig][j]-self._fFlies[_ffdest][j])**2)
        _de=sqrt(_de)
        return _de
       # rij - Distãncia r entre o firefly(i) e o firefly(j)
        
    def calculate(self):
        for k in range(self._n_geracoes):
            for i in range(self._qtd_fireflies):
                for j in range(i,self._qtd_fireflies):
                    if (self._luminosidade[j]>self._luminosidade[i]): #Se algum firef
                        self.set_movimentar_firefly(i,j)
                    self.set_intensidade_emitida_de_luz(self._fFlies)   #Atualizar luminosidade de todos os vagalumes
        _mb=self.get_menos_brilhante(self._luminosidade)                #pegar a posição do  menos brilhante
        print self._fFlies[_mb],self.funcao(self._fFlies[_mb])                            #exibir o valor da função do menos brilhante
    
x=FireFly()
x.calculate()