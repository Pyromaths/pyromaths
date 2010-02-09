# -*- coding: utf-8 -*-

import re

class Expression:
    '''Classe expression'''
    def __init__(self, donnee,parenthese=False):
        self.arbre=donnee
        self.parenthese=parenthese
        self.signe=self.arbre[0]

    def __add__(self,other):
        return Expression(('+',self,other))

    def __mul__(self,other):
        return Expression(('*',self,other))

    def __sub__(self,other):
        return Expression(('-',self,other))

    def __str__(self):
        if self.signe=="n":
            string=str(self.arbre[1])
        elif self.signe=="opp":
            string="-"+str(self.arbre[1])
        else:
            string=str(self.arbre[1])+self.arbre[0]+str(self.arbre[2])
        if self.parenthese:
            return '('+string+')'
        else:
            return string

def split_parenthese(donnee):
    gauche=donnee.find('(')
    if gauche!=-1:
        droite=donnee.rfind(')')    
        return donnee[:gauche],donnee[gauche+1:droite],donnee[droite+1:]
    else:
        return donnee

def str_expression(donnee,parenthese=False):
    recherche=split_parenthese(donnee)
    if isinstance(recherche,tuple):
        if recherche[0]=='':
            return Expression((recherche[2][0],str_expression(recherche[1],parenthese=True),
                               str_expression(recherche[2][1:])), parenthese=parenthese)
        elif recherche[2]=='':
            return Expression((recherche[0][-1],str_expression(recherche[0][:-1]),str_expression(recherche[1],parenthese=True)),
                              parenthese=parenthese)
        else:
            return Expression((recherche[0][-1],str_expression(recherche[0][:-1]),
                Expression((recherche[2][0],str_expression(recherche[1],parenthese=True),str_expression(recherche[2][1:])))),parenthese=parenthese)
    else:
        for signe in ['+','-','*']:
            position=donnee.find(signe)
            if position!=-1:
                return Expression((signe,str_expression(donnee[:position]),str_expression(donnee[position+1:])),parenthese=parenthese)
        return Expression(('n',int(donnee)))
            
