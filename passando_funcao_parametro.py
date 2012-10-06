# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 10:25:23 2012

@author: leonard
"""

def soma(x,y):
    return x+y

def dobra(funcao,args):
    return funcao(*args)*2

dobra(soma, (1,2))
