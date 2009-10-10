# -*- coding: utf-8 -*-

import re
from Terme import *

class Polynome:
    def __init__(self, string, var = "x"):
        self.var = var # Lettre pour la var
        self.string = string
        self.termes = self.splitpoly()
        self.deg = (self.termes[0]).puiss

    def __add__(self, other):
        if self.var == other.var:
            result = []
            liste1 = self.termes[:]
            liste2 = other.termes[:]
            while ((len(liste1) != 0) or (len(liste2) != 0)):
                if (len(liste1) != 0) and (len(liste2) != 0):
                    if (liste1[0]).puiss > (liste2[0]).puiss:
                        result.append(str(liste1[0]))
                        liste1.remove(liste1[0])
                    elif (liste1[0]).puiss < (liste2[0]).puiss:
                        result.append(str(liste2[0]))
                        liste2.remove(liste2[0])
                    else:
                        result.append(str(liste1[0] + liste2[0]))
                        liste1.remove(liste1[0])
                        liste2.remove(liste2[0])
                elif (len(liste1) == 0) and (len(liste2) != 0):
                    result.append(str(liste2[0]))
                    liste2.remove(liste2[0])
                else:
                    result.append(str(liste1[0]))
                    liste1.remove(liste1[0])
            for element in result:
                if element[0] != '-':
                    index = result.index(element)
                    result[index] = '+' + element
        return Polynome(''.join(result), self.var)


    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            newtermes = []
            for element in self.termes:
                if element == -1:
                    newtermes.append('')
                elif element == 1:
                    newtermes.append('+')
                else:
                    mult = str(element * other )
                    if mult[0] == "-":
                        newtermes.append(mult)
                    else:
                        newtermes.append("+" + mult)
        return Polynome(''.join(newtermes), self.var)

    def __rmul__(self, other):
        return self * other
        
    def __neg__(self):
        return self * (-1)
        
    def __str__(self):
        return self.string

    def splitpoly(self):
        resultat = []
        termes = []
        separeplus = (self.string).split("+")

        for element in separeplus:
            temp = []
            temp = element.split("-")
            for bis in temp:
                resultat.append(bis)
                if temp.index(bis) != len(temp)-1:
                    resultat.append(-1)
            if separeplus.index(element) != len(separeplus)-1:
                resultat.append(1)
        if '' in resultat:
            resultat.remove('')
        for element in resultat:
            index = resultat.index(element)
            if index > 0:
                coeff = resultat[index-1]
            else:
                coeff = 1
            if (element not in [-1, 1]):
                a = re.findall('\d+(?:\.\d*)?', element)
                if (len(a) == 1) and (not re.findall('\^', element)) and (re.findall(self.var, element)):
                    termes.append(Terme(coeff * float(a[0]), 1, self.var))
                elif (len(a) == 1) and (re.findall(self.var, element)):
                    termes.append(Terme(coeff * 1, int(a[0]), self.var))
                elif (len(a) == 1):
                    termes.append(Terme(coeff * float(a[0]), 0, self.var))
                else:
                    termes.append(Terme(coeff * float(a[0]), int(a[1]), self.var))
        return termes


a=Polynome('-x^3-3x^2+2x-5')

b=Polynome('x^2')

print "a=", a
print "b=", b

print "a+b=", a+b

print "a-b=", a-b
print "a*5=", a*5

















        
                