# -*- coding: utf-8 -*-

import re 
import outils.Arithmetique
import string
import math
import os
from outils.Conversions import radians, degres


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


class Litteral:

    """Classe permettant d'opérer sur des expressions littérales
    Une expression littérale est stockée ainsi :
    [(coeff1, variable1, exposant1), (coeff2, variable2, exposant2), ...]"""

    def __init__(self, expression):
        self.e = expression

    def reduit(self):

        # retourne l'expression réduite, en supprimant les coefficients nuls,
        # excepté s'il est de degré 0.

        expression = sorted(self.e, key=lambda x: (x[1], -x[2]))
        (expr, i) = ([expression[0]], 1)
        for i in range(1, len(expression)):
            if expr:
                if expr[-1][1] == expression[i][1] and expr[-1][2] == \
                    expression[i][2]:
                    if expr[-1][0] + expression[i][0] or expr[-1][2] == \
                        0:
                        expr.append((expr.pop(-1)[0] + expression[i][0],
                                    expression[i][1], expression[i][2]))
                    else:
                        expr.pop(-1)
                else:
                    expr.append(expression[i])
            else:
                expr.append(expression[i])

        return Litteral(expr)

    def oppose(self):

        # retourne l'opposé d'une expression littérale

        expr = self.e
        expression = []
        for i in range(len(expr)):
            expression.append((-expr[i][0], expr[i][1], expr[i][2]))
        return Litteral(expression)

    def __add__(self, expression):
        expr1 = self.e
        expr2 = expression.e
        expr1.extend(expr2)
        return Litteral.reduit(Litteral(expr1))

    def __sub__(self, expression):
        expr1 = self.e
        expr2 = Litteral.oppose(expression).e
        expr1.extend(expr2)
        return Litteral.reduit(Litteral(expr1))

    def __mul__(self, expression):
        expr1 = self.e
        expr2 = expression.e
        expression = []
        for i in range(len(expr1)):
            for j in range(len(expr2)):
                if expr1[i][1] == expr2[j][1]:
                    expression.append((expr1[i][0] * expr2[j][0], expr1[i][1],
                            expr1[i][2] + expr2[j][2]))
                else:
                    pass

                    # TODO: Cas du produit de deux expressions à plusieurs variables

        return Litteral.reduit(Litteral(expression))

 
#print a>b
#print (c.n,c.d)
#a=Litteral([(3,'x',0),(2,'x',1)])
#b=Litteral([(3,'x',0),(-2,'x',1)])
#print (a*b).e
           
