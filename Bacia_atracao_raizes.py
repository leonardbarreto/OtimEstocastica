# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:57:11 2012

@author: leonard
"""

import random as nd 
import math as mt
import time
import pylab
from numpy import matrix
from numpy import linalg


def funcao(x,indiceFuncao):
    """ Parâmetros:
        - x: vetor
        - indiceFuncao: 
        Função Twoeq7
    """
    r = [0.0]*5
   # r[0] = 4*x[0]**2 - 20*x[0] + 0.25*x[1]**2 + 8
    #r[1] = 0.5*x[0]*x[1]**2 + 2*x[0] - 5*x[1] + 8
    a=0.5
    b=0.8
    c=0.3
    kp=604500
    P=0.00243
    try:
        r[0]=a-((c+2*x[0])**2*(a+b+c-2*x[0])**2)/(x[1])-x[0]
    except ZeroDivisionError:
        x[0]=0 #Condição do problema
        x[1]=-1 #Condição do problema
    r[1]=x[1]-kp*P**2*(b-3*x[0])**3
    """r[0] = x[0] - x[1] 
    r[1] = x[0]**2 + x[1]**2 - 1"""

    """r[0] = x[0]**3 - 3*x[0]**2 - x[1] + 2
    r[1] = (x[0] - 1)**2 + x[1]**2 - 4"""
    
    return r[indiceFuncao]

def derivadaNumerica(indiceFuncao,ponto,indicePonto):
    """ Parâmetros:
        - indiceFuncao: indica a funçao a ser derivada
        - ponto:
        - indicePonto:

    """    
    h = 0.001
    pontoCopia = ponto
    pontoCopia[indicePonto] = pontoCopia[indicePonto] - 2*h
    parcela1 = funcao(pontoCopia,indiceFuncao)
    pontoCopia[indicePonto] = pontoCopia[indicePonto] + 2*h
   
    pontoCopia[indicePonto] = pontoCopia[indicePonto] - h
    parcela2 = 8*funcao(pontoCopia,indiceFuncao)
    pontoCopia[indicePonto] = pontoCopia[indicePonto] + h
    
    pontoCopia[indicePonto] = pontoCopia[indicePonto] + h
    parcela3 = 8*funcao(pontoCopia,indiceFuncao)
    pontoCopia[indicePonto] = pontoCopia[indicePonto] - h
    
    pontoCopia[indicePonto] = pontoCopia[indicePonto] + 2*h
    parcela4 = funcao(pontoCopia,indiceFuncao)
    pontoCopia[indicePonto] = pontoCopia[indicePonto] - 2*h
    
    return ((parcela1 - parcela2 + parcela3 - parcela4) / (12*h))   

def calculaMatrizJacobiana(ordemMatriz,ponto):
    """Parâmetros:
        - ordemMatriz: indica a ordem da matriz (que deve ser quadrada)        
        - ponto: variável que deseja-se derivar ("em função de")
    """
    matriz = []
    for linha in range(ordemMatriz):
        tmp = []
        for coluna in range(ordemMatriz):
            tmp.append(derivadaNumerica(linha,ponto,coluna))
        matriz.append(tmp[:])
    return matriz

def calculaTermoFonte(ordemMatriz,ponto):
    matriz = []
    for linha in range(ordemMatriz):
        tmp = []
        for coluna in range(1):
            tmp.append(-funcao(ponto,linha))
        matriz.append(tmp[:])
    return matriz
        
def criterioParada(matriz,erro,dimensao):
    parar = 1
    for linha in range(dimensao):
        if (abs(matriz[linha] - 0) > erro):
            parar = 0
    return parar
    
def resolveSistema(chuteInicial,dimensao):
    erro = 0.00001
    matrizJacobiana = matrix(calculaMatrizJacobiana(dimensao,chuteInicial))
    matrizTermoFonte = matrix(calculaTermoFonte(dimensao,chuteInicial))
    try:    
        matrizSolucao = linalg.solve(matrizJacobiana,matrizTermoFonte) #resolver sistema linear
    except LinAlgError:
        #return [0,0]
        return 'ERRO'
    deltas = []
    for linha in range(dimensao):
        deltas.append(matrizSolucao[linha,0])
    for linha in range(dimensao):
        chuteInicial[linha] = chuteInicial[linha] + deltas[linha]
    
    while (criterioParada(matrizTermoFonte,erro,dimensao) == 0):
        matrizJacobiana = matrix(calculaMatrizJacobiana(dimensao,chuteInicial))
        matrizTermoFonte = matrix(calculaTermoFonte(dimensao,chuteInicial))
        try:
            matrizSolucao = linalg.solve(matrizJacobiana,matrizTermoFonte)
        except LinAlgError:
            #return [0,0]
            return 'ERRO'
        for linha in range(dimensao):
            deltas[linha] = matrizSolucao[linha,0]
        for linha in range(dimensao):
            chuteInicial[linha] = chuteInicial[linha] + deltas[linha]
    
    return chuteInicial
    
def montaMatrizSolucao():
    x1 = [-100,100]
    x2 = [-100,100]
    amplitude = 1
    iniciador = x2[0]
    x = []
    while (x1[0] <= x1[1]):
        while (x2[0] <= x2[1]):
            z = [x1[0],x2[0]]   #Chute inicial
            x.append(resolveSistema(z,2))
            x2[0] = x2[0] + amplitude
        x2[0] = iniciador
        x1[0] = x1[0] + amplitude
    #print x
    return x
    
def distanciaEntrePontos(pontoUm,pontoDois,coordenada):
    distancia = abs(pontoUm[coordenada] - pontoDois[coordenada])
    return distancia
    
def codificaRespostas():
    """ Codifica as respostas em função dos valores encontrados. 
        Assume-se o valor 0(zero) quando há erro. Os demais valores são em função do número de soluções do problema.
        Para o sistema proposto, assume-se:
            O valor 1(um) para ~ [0.05, 0.86] = cor branca
            O valor 2(dois) para ~ [0.60, -3,57] = cor azul
    """    
    lista = montaMatrizSolucao()
    codificacao = []
    solucoesDistintas = []
    tolerancia = 0.1
        
    # exclui os pontos muito perto uns dos outros
    for linha in range(len(lista)):
        if (lista[linha] != 'ERRO'):
            for linha2 in range(linha + 1,len(lista)):
                if (lista[linha2] != 'ERRO'):
                    if ((distanciaEntrePontos(lista[linha],lista[linha2],0) < tolerancia) and (distanciaEntrePontos(lista[linha],lista[linha2],1) < tolerancia)):
                # procurar uma forma de excluir esta posicao                    
                        lista[linha2] = [0,0]
    # termina de excluir os pontos pertos um dos outros
    
    for cont in range(len(lista)):
        if ((lista[cont] != [0,0]) and (lista[cont] <> 'ERRO')):
            solucoesDistintas.append(lista[cont])
    
    lista = montaMatrizSolucao()
    
    for cont in range(len(lista)):
        codificacao.append(0)
    
    for cont in range(len(lista)):
        if (lista[cont] == 'ERRO'):
            codificacao[cont] = 0
            
    indiceResposta = 0
    for cont in range(len(solucoesDistintas)):
        indiceResposta = indiceResposta + 1
        for cont2 in range(len(lista)):
            if (lista[cont2] != 'ERRO'):
                if (distanciaEntrePontos(solucoesDistintas[cont],lista[cont2],0) < tolerancia) and (distanciaEntrePontos(solucoesDistintas[cont],lista[cont2],1) < tolerancia):
                    codificacao[cont2] = indiceResposta
    
    posicao = 0
    matriz = []
    for linha in range(int(math.sqrt(len(lista)))):
        tmp = []
        for coluna in range(int(math.sqrt(len(lista)))):
            tmp.append(codificacao[posicao])
            posicao = posicao + 1
        matriz.append(tmp[:])
    #print matriz
    return matriz

def baciaAtracaoRaizes():
    a = codificaRespostas()
    pylab.imshow(a,cmap=get_cmap('Blues'),origin='lower',extent=[-100,100,-100,100])
    #pylab.imshow(a,origin='lower',extent=[-5,5,-5,5])
    pylab.xlabel('Valores da Primeira Coordenada')
    pylab.ylabel('Valores da Segunda Coordenada')
    pylab.title('Bacia de Atracao de Raizes')
    pylab.show()
    #pylab.savefig('Bacia Atracao de Raizes')
    return 0

baciaAtracaoRaizes()