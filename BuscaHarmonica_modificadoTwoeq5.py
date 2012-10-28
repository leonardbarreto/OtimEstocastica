# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 10:47:15 2012

@author: leonard
"""
import numpy as np
import pylab

class BuscaHarmonica:
    """ Algoritmo de otimização e busca baseado em perfomance musical. Busca de múltiplos ótimos baseado no conceito de filtro de raízes.
        Parâmetros:
            -Funcao objetivo (fo)
            -Número de variáveis de decisao (N)
    """
    def __init__(self):#,p_txpar=0.3,p_mi=100,p_txhmcr=0.5,p_fw=0.1):
        _tx_improv=1        #Taxa de improvisação - possibilita a inserção de novas notas musicais na harmonia        
        self._tx_par=0.3    #Taxa referente à probabilidade de uma variável sofrer ajustes. RELAÇÃO COM OS VALORES DO INTERVALO
        self._mi=500      #número máximo de improvisos (número máximo de iterações ou gerações)
        self._tx_hmcr=0.8   #taxa de escolha de um valor da memória. RELAÇÃO COM OS VALORES DO INTERVALO [entre 0..1]
        self._fw=0.4        #Fret Width(tamanho da pertubação) - ajustes que podem ser realizados em uma variável de uma harmonia (elemento do vetor)
        self._hms=100         #Número de vetores presentes na memória harmôniaca
        self._n_inst=3      #Número de instrumentos na memória harmônica - similar a dimensão do problema (quantidade de variáveis do problema)
        self._tolerancia=0.01
        self._vet_raizes=[]
        self._ensaios=15 #número de execuções
        self.set_limites()
        self.set_memoria_harmonica(self._hms)
        self.set_nova_harmonia()        
        
    def funcao(self,x):
        """ Definição da função objetivo do problema proposto """
        #ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))
        #parâmetros da função        
        k1= 3e5*exp(-5000/x[1])
        k2 =6e7*exp(-7500/x[1]) 
        F0=1
        T0=300
        try:
            f1=-0.16*x[0]*F0/x[2]+k1*(1-x[0])-k2*x[0]
            f2 =0.16*F0*T0/x[2]-0.16*x[1]*F0/x[2]+5*(k1*(1-x[0])-k2*x[0])
            f3 = 0.16*F0-0.4*sqrt(x[2])             
            ff=(f1**2)+(f2**2)+(f3**2)   
        except ZeroDivisionError:
            x[0]=0.5 #Condição do problema
            x[1]=500 #Condição do problema
            x[2]=0.5
        return ff
  
    def set_nova_harmonia(self):        
        #_nvh=[]     #Novo vetor harmônico
        #ALTERAR PARA ATRIBUIR OS VALORES ENTRE A FAIXA DE LIMITES DAS VARIÁVEIS (AQUI INSTRUMENTOS)...        
        #_vnh.append(rand(_p_nInst)); #Nova harmonia com valores entre 0..1 de dimensão em relação _n_inst
        #_vnh.append(array([uniform(-2,2),uniform(-2,2)]))        
        #_nvh.append(self.set_pontos())
        self._v_nova_harmonia=[]
        self._v_nova_harmonia.append(self.set_pontos())
        #self._v_nova_harmonia=_nvh
    
    def set_pontos(self):
        """Retorna um ponto qualquer dentro dos limites [min,max] para cada variável estipulados em set_limites()"""
        n1=uniform(self._limites[0][0],self._limites[0][1])
        n2=uniform(self._limites[1][0],self._limites[1][1])        
        n3=uniform(self._limites[2][0],self._limites[2][1])
        _pt=array([n1,n2,n3])
        return _pt
    
    def set_limites(self):
        self._limites=[]        
        for i in range(self._n_inst):
            self._limites.append(rand(2)) #array com duas posições, sendo a 1a o valor mínimo e a 2a o valor máximo
        #definição da área de busca para cada variável
        self._limites[0]=array([0,5]) #[min,max]
        self._limites[1]=array([200,700]) #[min,max]
        self._limites[2]=array([0,5]) #[min,max]
        return self._limites
    
    #def get_nova_harmonia(self):
    #    return self._v_nova_harmonia
                
    def set_memoria_harmonica(self,_pHms):
        """ Cria e inicializa a memória harmônica, composta por n harmonias(vetor).
            Parãmetros:
                - Número de vetores presentes na memória harmônica
                - Número de instrumentos na memória harmônica
        """        
        self._memHarm=[]        #Inicializa a memória harmônica
        for i in range(_pHms):  # A quantidade de vetores é de acordo com o valor da variável self._hms
            self._memHarm.append(self.set_pontos())
        return self._memHarm
    
    def improvisar_nova_harmonia(self,_pHmcr,_pFw,_pHms):
        """ Uma nova harmonia será gerada a partir da combinação de várias harmonias existentes na memória harmônica.
            Nesta caso, CADA instrumento (variável) 
            Parãmetros:
                - _pHmcr-> taxa de escolha de um valor da memória
                - _pFw  -> taxa da pertubacao de uma harmonia
                - _pHms -> Número de vetores presentes na memória harmônica
        """
        
        _r=uniform(-1,1)                    #escolha aleatória de reais entre -1 e 1
        for j in range(self._n_inst):
            _indAle=randint(0,_pHms)          #escolha aleatória de uma harmonia da memória harmônica (linha de uma matriz)            
            if (float(rand(1))<=self._tx_hmcr):
                self._v_nova_harmonia[0][j]=self._memHarm[_indAle][j]
                if (float(rand(1))<=self._tx_par): 
                    self._v_nova_harmonia[0][j]=self._v_nova_harmonia[0][j]+_r*self._fw
            else:
                self.set_nova_harmonia()
        return self._v_nova_harmonia
            
    def atualizar_memoria_harmonica(self,_pNovaHarmonia):
        """ Verifica se a nova harmonia é melhor do que a pior harmonia na memória harmônica. Caso seja, a pior harmonia deverá ser substituida pela nova.  
            Parâmetros:
                - _pNovaHarmonia -> A nova harmonia abtida no método improvisar_nova_memoria"""
        #Se existir uma harmonia pior do a nova harmonia, substituir pior.        
        #se o valor da função da nova harmonia é melhor do que a pior harmonia na memória. Considerar a função de minimizar        
        self.pior_harmonia(self._memHarm)
        if (self.funcao(_pNovaHarmonia[0])<self._piorHar): 
            self._memHarm[self._piorPos]=_pNovaHarmonia[0] #substituir melhor harmonia pela pior da memória harmônica
        
    
    def pior_harmonia(self,_pHarm):
        """ Retorna a pior harmonia da memória harmônica.
            Parâmetros:
                - _pHarm -> memória harmônica
            Retorno:
                - _piorPos  -> localização (posição) da pior harmonia
                - _piorHar -> pior valor da função na posição _piorPos
        """
        _valorFuncao=0        
        self._piorPos=0                             #Posicao da pior harmonia
        self._piorHar=self.funcao(self._memHarm[0])   #Pior valor (f(x)) da harmonia da memória harmônica
        #verificando o pior valor da harmonia armazenada na memória harmônica. Como queremos minimizar o pior valor é o mais alto
        for i in range(1,self._hms):
            _valorFuncao=self.funcao(self._memHarm[i])  #_valorFuncao armazena o valor da função da harmonia[i]
            if (_valorFuncao>self._piorHar):
                self._piorHar=_valorFuncao
                self._piorPos=i
        return self._piorPos,self._piorHar
        
    def melhor_harmonia(self):
        """ Calcula a melhor harmonia da memória harmônica 
            Parâmetros:
                - _pHarm -> Memória harmônica
            Retorno:
                - _pHarm[_melhorPos]  -> melhor valor da função na posição _melhorPos
                - _piorHar          -> localização (posição) da melhor harmonia
        """
        _valorFuncao=0  
        self._melhorPos=0                          #Posicao da melhor harmonia
        self._melhorHar=self.funcao(self._memHarm[0]) #Melhor harmonia (valor (f(x)) da memória harmônica
        for i in range(1,self._hms):
            _valorFuncao=self.funcao(self._memHarm[i])  #_valorFuncao armazena o valor da função da harmonia[i]
            if (_valorFuncao>self._melhorHar):
                self._melhorHar=_valorFuncao
                self._melhorPos=i
        return self._memHarm[self._melhorPos],self._melhorHar
    
    def get_solucoes(self):
        """ Obter k raízes em função da quantidade de execuções estabelecidas """
        self._vet_raizes=[]
        self._vet_raizes.append(rand(self._n_inst))        
        #ini=time.time()
        for k in range(self._ensaios):
            for i in range(self._mi): #até o número máximo de iterações        
                self.set_nova_harmonia()                            
                self.improvisar_nova_harmonia(self._tx_hmcr,self._fw,self._hms)
                self.atualizar_memoria_harmonica(self._v_nova_harmonia)
        self._vet_raizes[0]=self.melhor_harmonia()[0]
        
    
    def filtro(self):
        """ Elimina as piores raízes repetidas."""         
        #FILTRO NOS PONTOS: eliminar as raízes que dão aproximadamente o mesmo valor de f(x)
        for i in range((self._ensaios)-1):
            for j in range(i+1,self._ensaios):
                if ((fabs(self._vet_raizes[i][0]-self._vet_raizes[j][0])<self._tolerancia) and (fabs(self._vet_raizes[i][1]- self._vet_raizes[j][1])<self._tolerancia)):
                    if (self.funcao(self._vet_raizes[j])<self.funcao(self._vet_raizes[i])): #Se a raiz j é a melhor, copiá-la para i
                        self._vet_raizes[i][0]=self._vet_raizes[j][0]  
                        self._vet_raizes[i][1]=self._vet_raizes[j][1]  
                    self._vet_raizes[j][0]=0  #marcar como solução próxima
                    self._vet_raizes[j][1]=0  #marcar como solução próxima
    
    def exibir_resultados(self):        
        print self._vet_raizes[0]#,self.funcao(self._vet_raizes[0])            
        #self._qtdraiz=0        
        #for i in range(self._ensaios):
        #    print self._vet_raizes[i],self.funcao(self._vet_raizes[i])
            #if (self._vet_raizes[i][0]!=0):
            #    self._qtdraiz=self._qtdraiz+1
            #    print self._vet_raizes[i],self.funcao(self._vet_raizes[i])
                #arq=open('HS_Twoeq5.txt','a')
                #Formato (número de gerações, número de pontos, vetor de raízes, valor da função)            
                #arq.write('%s %3s %.6f\n' %(self._vet_raizes[i], ' ', self.funcao(self._vet_raizes[i])))
                #arq.close        
#    def calculate(self):
#        """ Método responsavel por realizar o cálculo """
#        for k in range(self._mi): #até o número máximo de iterações        
#            self.set_nova_harmonia(self._n_inst)            
#            self.improvisar_nova_memoria(self._tx_hmcr,self._valorFuncaow,self._hms)
#            self.atualizar_memoria_harmonica(self._v_nova_harmonia)
#        return self.melhor_harmonia(self._memHarm)
    def calculate(self):
        self.get_solucoes()
        #self.filtro()
        self.exibir_resultados()
   
a=BuscaHarmonica()
a.calculate()
