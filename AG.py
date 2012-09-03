# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 23:31:30 2012

@author: leonard
Regras e convençoes de código: http://www.python.org.br/wiki/GuiaDeEstilo
"""
#import AGfuncoes
import numpy
import random
class AG:
    """ Algoritmos genéticos """
    
    def __init__(self,pMin=1,tamPop=6,txCr=2,txMut=0.1,numGer=4):
        self.pMin=pMin              #precisao mínima (número inteiro indicando a quantidade de casas decimais requeridaa)  
        self.tamPop=tamPop          #tamanho da população
        self.txCr=txCr              #taxa de cruzamento
        self.txMut=txMut            #taxa de mutação (em percentual)
        self.numGer=numGer          #número de gerações
        self.SetDimensao()
        self.SetIntervalo(self.dimensao)        
        self.SetAmplitude(self.dimensao,self.intervalo)
        self.SetNumeroDePontos(self.amplitude,self.pMin,self.dimensao)
        self.SetTamCromossomo(self.NP,self.dimensao)
        self.SetCadeia(self.tamCrom,self.dimensao)
        self.SetPopulacaoInicial(self.tamPop,self.cadeia)
        
    #def f1(x):                   #funcão 1 proposta
    #    return ((x[0]-1)**2+(x[1]-1)**2-x[0]*x[1])
    #def f2(x):                  # funcao 2 proposta
    #    return (x[0]**2+3*x[1]**2-2*x[0]-2*x[1])
    
    def SetDimensao(self):
        """ Configura dimensão de acordo com a função proposta """        
        self.dimensao=2;
    
    def GetDimensao(self):
        """ Retorna a dimensao do problema """        
        return self.dimensao
    
    def SetIntervalo(self,dimen):
        """ Configura o intervalo de busca para as variáveis do problema (funcao). Depende da dimensao do problema (quantidade de variáveis) """  
        _vInt=[]                        #cria lista vazia
        for i in range(dimen):      #cria lista de arrays com valores nulos de tamanho dimen
            _vInt.append(numpy.zeros(dimen)) 
        #Ainda fixo para duas dimensoes
        _vInt[0][0]=-2
        _vInt[0][1]=1.5
        _vInt[1][0]=-0.5
        _vInt[1][1]=3
        self.intervalo=_vInt
    
    def GetIntervalo(self):
        return self.intervalo
    
    def Funcao(self,x):
        #x é um array de tamanho dimen ( ou cromossomo)
        self.f=((x[0]-1)**2+(x[1]-1)**2-x[0]*x[1])    

    def SetAmplitude(self,dimen,vIntB):
        """ obtem amplitude do intervalo em relação aos intervalos de busca de acordo com a dimensao da função fornecida """        
        # dimen  - dimensao do problema
        # vIntB - vetor com Intervalo de Busca
        _vAmp=[]        
        for i in range(dimen):      #cria lista de arrays com valores nulos de tamanho dimen
            _vAmp.append(sum(numpy.fabs(vIntB[i]))) 
        self.amplitude=_vAmp
        
    def GetAmplitude(self):
        """ Retorna a amplitude do intervalo em relação aos intervalos de busca de acordo com a dimensao da função fornecida """                
        return self.amplitude
    
    def SetNumeroDePontos(self,a,p,dimen,base=10):
        """ calcula o número de pontos na base (base) em funcao da amplitude (a), precisão (p) """        
        _vNP=[]
        for i in range(dimen):
            _vNP.append((a[i]*(base**p)))
        self.NP=_vNP
    
    def GetNumeroDePontos(self):        
        """ Retorna o número de pontos na base calculado em SetNumeroDePontos """                
        return self.NP
        
    def CalcBits(self,quociente):
        """ retorna a quantidade necessária de bits para representar um número decimal """        
        _qtdBit=1
        while quociente!=1:
            quociente=int(quociente)/2
            _qtdBit=_qtdBit+1
        return _qtdBit
        
    def SetTamCromossomo(self,valor,dimen):
        """ Escolhe o tamanho do cromossomo, em função do número de pontos(valor) calculado no método setNumeroDePontos """
        _vTC=[] #vetor tamanho do cromossomo em função da dimensão
        for i in range(dimen):        
            bits=self.CalcBits(valor[i])    
            _vTC.append(bits)
        self.tamCrom=max(_vTC) #retorna a maior quantidade necessária para representar o maior número
    
    def GetTamCromossomo(self):       
        """ Escolhe o tamanho do cromossomo, calculado em setTamCromossomo """        
        return self.tamCrom
       
    def SetCadeia(self,tC,dimen):
        """  Configura a cadeia do cromossomo. Requisitos:
            - Tamanho do cromossomo (tC)
            - dimensao (dimen)
        """
        self.cadeia=tC*dimen
    
    def GetCadeia(self):
        return self.cadeia
        
    def SetPopulacaoInicial(self,tP,tC):
        """ Inicia uma populacao inicial. Necessita das seguintes informações:
        -tamanho da população (tP)        
        -tamanho da cadeia (tC)
        """
        _vPopIni=randint(0,2,tP*tC)
        _vPopIni.shape=(tP,tC)
        self.PopIni=_vPopIni
        
    def GetPopulacaoInicial(self):
        return self.PopIni
    
    def ConverterCromossomo(self,tCrom):
        """ converter cromossomo de uma base binária para uma base decimal 
            - Tamanho do cromossomo (tCrom)
        """
        fim=-1
        for i in range(self.dimensao):        
            ini=fim+1
            fim=ini+(tC-1)
            print ini,fim
        #nMax=2**self.tamCrom #maior número decimal obtido de acordo com o tamanho em bits do cromossomo
        
a=AG()
