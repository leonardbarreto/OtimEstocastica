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
    def __init__(self,p_txpar=0.3,p_mi=10000,p_txhmcr=0.5,p_fw=0.1):
        _tx_improv=1        #Taxa de improvisação - possibilita a inserção de novas notas musicais na harmonia        
        self._tx_par=0.3    #Taxa referente à probabilidade de uma variável sofrer ajustes. RELAÇÃO COM OS VALORES DO INTERVALO
        self._mi=1000      #número máximo de improvisos (número máximo de iterações ou gerações)
        self._tx_hmcr=0.3   #taxa de escolha de um valor da memória. RELAÇÃO COM OS VALORES DO INTERVALO [entre 0..1]
        self._fw=0.2        #Fret Width(tamanho da pertubação) - ajustes que podem ser realizados em uma variável de uma harmonia (elemento do vetor)
        self._hms=10         #Número de vetores presentes na memória harmôniaca
        self._n_inst=2      #Número de instrumentos na memória harmônica - similar a dimensão do problema (quantidade de variáveis do problema)
        self._tolerancia=0.9
        self._vet_raizes=[]
        self._execucoes=50
        self.set_limites()        
        self.set_memoria_harmonica(self._hms,self._n_inst)
        self.set_nova_harmonia(self._n_inst)        
        
    def funcao(self,x):
        """ Definição da função objetivo do problema proposto """
        #ff=-((fabs(x[0])+fabs(x[1]))*exp(-(x[0]**2+x[1]**2)))
        #parâmetros da função        
        a=0.5
        b=0.8
        c=0.3
        kp=604500
        P=0.00243        
        try:
            ff=(a-((c+2*x[0])**2*(a+b+c-2*x[0])**2)/(x[1])-x[0])**2 + (x[1]-kp*P**2*(b-3*x[0])**3)**2
        except ZeroDivisionError:
            x[0]=0 #Condição do problema
            x[1]=-1 #Condição do problema
        return ff
        #return -(sum(fabs(x))*exp(-sum(x**2))) # Minimizar (sinal negativo)
            
    def grafico(self):
        entrada = pylab.arange(0, 20, 1)
        saida=self.funcao(entrada)
        pylab.plot(entrada, saida)
        pylab.xlabel('x1')
        pylab.ylabel('x2')
        pylab.title('f(x1,x2)')
        pylab.grid(True)
        pylab.show()
        #return 0
    
    def set_nova_harmonia(self,_p_nInst):
        _vnh=[]     #Novo vetor harmônico
        #ALTERAR PARA ATRIBUIR OS VALORES ENTRE A FAIXA DE LIMITES DAS VARIÁVEIS (AQUI INSTRUMENTOS)...        
        #_vnh.append(rand(_p_nInst)); #Nova harmonia com valores entre 0..1 de dimensão em relação _n_inst
        #_vnh.append(array([uniform(-2,2),uniform(-2,2)]))        
        _vnh.append(self.set_pontos(self._limites[0],self._limites[1]))
        self._v_nova_harmonia=_vnh
    
    def set_pontos(self,_l_sup,_l_inf):
        """Configura as coordenadas de acordo com os valores limitantes estipulados"""
        n1=uniform(_l_inf,_l_sup)
        n2=uniform(_l_inf,_l_sup)        
        _pt=array([n1,n2])
        return _pt
    
    def set_limites(self):
        self._limites=array([-5.,5.]) #[min,max]
    
    def get_limites(self):
        return self._limites
    
    def get_nova_harmonia(self):
        return self._v_nova_harmonia
                
    def set_memoria_harmonica(self,_pHms,_pNinst):
        """ Cria e inicializa a memória harmônica, composta por n harmonias(vetor).
            Parãmetros:
                - Número de vetores presentes na memória harmônica
                - Número de instrumentos na memória harmônica
        """        
        _vh=[]                          #vetor harmônico
        for i in range(_pHms):
            #_vh.append(rand(_pNinst)) #Cria valores reais entre 0..1
            _vh.append(self.set_pontos(self._limites[0],self._limites[1]))
        self._mHarm=_vh
        #return self._mHarm
    
    def get_memoria_harmonica(self):
        return self._mHarm
    
    def improvisar_nova_memoria(self,_pHmcr,_pFw,_pHms):
        """ Uma nova harmonia será gerada a partir da combinação de várias harmonias existentes na memória harmônica.
            Parãmetros:
                - _pHmcr-> taxa de escolha de um valor da memória
                - _pFw  -> taxa da pertubacao de uma harmonia
                - _pHms -> Número de vetores presentes na memória harmônica
        """
        _r=uniform(-1,1)                    #escolha aleatória de reais entre -1 e 1
        for j in range(self._n_inst):
            _iAle=randint(0,_pHms)          #escolha aleatória de uma harmonia da memória harmônica (linha de uma matriz)            
            #if (self._mHarm[_iAle][j]<=self._tx_hmcr):
            if (float(rand(1))<=self._tx_hmcr):
                self._v_nova_harmonia[0][j]=self._mHarm[_iAle][j]
                #if (self._mHarm[_iAle][j]<=self._tx_par): #
                if (float(rand(1))<=self._tx_par): 
                    self._v_nova_harmonia[0][j]=self._v_nova_harmonia[0][j]+_r*self._fw
            else:
                self._v_nova_harmonia[0][j]=uniform(self._limites[0],self._limites[1]) #valores reais aleatórios entre 0..1
        return self._v_nova_harmonia
            
    def atualizar_memoria_harmonica(self,_pNovaHarmonia):
        """ Verifica se a nova harmonia é melhor do que a pior harmonia na memória harmônica. Caso seja, a pior harmonia deverá ser substituida pela nova.  
            Parâmetros:
                - _pNovaHarmonia -> A nova harmonia abtida no método improvisar_nova_memoria"""
        #Se existir uma harmonia pior do a nova harmonia, substituir pior.        
        #se o valor da função da nova harmonia é melhor do que a pior harmonia na memória. Considerar a função de minimizar        
        self.pior_harmonia(self._mHarm)        
        if (self.funcao(_pNovaHarmonia[0])<self._pVh): 
            self._mHarm[self._pPh]=_pNovaHarmonia[0] #substituir melhor harmonia pela pior da memória harmônica
        self._melhorHarmonia=_pNovaHarmonia
        return self._melhorHarmonia
    
    def pior_harmonia(self,_pHarm):
        """ Retorna a pior harmonia da memória harmônica.
            Parâmetros:
                - _pHarm -> memória harmônica
            Retorno:
                - _pH  -> localização (posição) da pior harmonia
                - _pVh -> pior valor da função na posição _pH
        """
        _f=0        
        self._pPh=0                             #Posicao da pior harmonia
        self._pVh=self.funcao(self._mHarm[0])   #Pior valor (f(x)) da harmonia da memória harmônica
        #verificando o pior valor da harmonia armazenada na memória harmônica. Como queremos minimizar o pior valor é o mais alto
        for i in range(1,self._hms):
            _f=self.funcao(self._mHarm[i])  #_f armazena o valor da função da harmonia[i]
            if (_f>self._pVh):
                self._pVh=_f
                self._pPh=i
        return self._pVh,self._pPh
        
    def melhor_harmonia(self,_pHarm):
        """ Calcula a melhor harmonia da memória harmônica 
            Parâmetros:
                - _pHarm -> Memória harmônica
            Retorno:
                - _pHarm[_mPh]  -> melhor valor da função na posição _mPh
                - _pVh          -> localização (posição) da melhor harmonia
        """
        _mPh=0                          #Posicao da melhor harmonia
        _mH=self.funcao(self._mHarm[0]) #Melhor valor (f(x)) da harmonia da memória harmônica
        for i in range(1,self._hms):
            _f=self.funcao(self._mHarm[i])  #_f armazena o valor da função da harmonia[i]
            if (_f>_mH):
                _mH=_f
                _mPh=i
        return _pHarm[_mPh],_mH
    
    def get_solucoes(self):
        """ Obter k raízes em função da quantidade de execuções estabelecidas """
        #ini=time.time()
        for k in range(self._execucoes):
            self._vet_raizes.append(rand(self._n_inst))
            for i in range(self._mi): #até o número máximo de iterações        
                self.set_nova_harmonia(self._n_inst)            
                self.improvisar_nova_memoria(self._tx_hmcr,self._fw,self._hms)
                self.atualizar_memoria_harmonica(self._v_nova_harmonia)
            self._vet_raizes[k]=self.melhor_harmonia(self._mHarm)[0]
    
    def filtro(self):
        """ Elimina as piores raízes repetidas."""         
        #FILTRO NOS PONTOS: eliminar as raízes que dão aproximadamente o mesmo valor de f(x)
        for i in range((self._execucoes)-1):
            for j in range(i+1,self._execucoes):
                if ((fabs(self._vet_raizes[i][0]-self._vet_raizes[j][0])<self._tolerancia) and (fabs(self._vet_raizes[i][1]- self._vet_raizes[j][1])<self._tolerancia)):
                    if (self.funcao(self._vet_raizes[j])<self.funcao(self._vet_raizes[i])): #Se a raiz j é a melhor, copiá-la para i
                        self._vet_raizes[i][0]=self._vet_raizes[j][0]  
                        self._vet_raizes[i][1]=self._vet_raizes[j][1]  
                    self._vet_raizes[j][0]=0  #marcar como solução próxima
                    self._vet_raizes[j][1]=0  #marcar como solução próxima
    
    def exibir_resultados(self):        
        self._qtdraiz=0        
        for i in range(self._execucoes):
            if (self._vet_raizes[i][0]!=0):
                self._qtdraiz=self._qtdraiz+1
                print self._vet_raizes[i],self.funcao(self._vet_raizes[i])
                #arq=open('DE.txt','a')
                #Formato (número de gerações, número de pontos, vetor de raízes, valor da função)            
                #arq.write('%30s %s %3s %.6f\n' %(' ', self._vet_raizes[i], ' ', self.funcao(self._vet_raizes[i])))
                #arq.close        
#    def calculate(self):
#        """ Método responsavel por realizar o cálculo """
#        for k in range(self._mi): #até o número máximo de iterações        
#            self.set_nova_harmonia(self._n_inst)            
#            self.improvisar_nova_memoria(self._tx_hmcr,self._fw,self._hms)
#            self.atualizar_memoria_harmonica(self._v_nova_harmonia)
#        return self.melhor_harmonia(self._mHarm)
    def calculate(self):
        self.get_solucoes()
        self.filtro()
        self.exibir_resultados()
   
a=BuscaHarmonica()
a.calculate()
