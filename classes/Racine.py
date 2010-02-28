# -*- coding: utf-8 -*-

import sys
sys.path[:0] = ['../outils','outils']
from Arithmetique import *
from Affichage import decimaux
from math import *

def produitfacteurs(facteurs):
    """Affiche sous forme de produit les éléments d'une liste."""
    prodfacteurs = ''
    for element in facteurs:
        prodfacteurs += str(element) + ' \\times '
    return prodfacteurs[:-7]

class Racine:
    def __init__(self, radicande, coeff = 1, indice = 2):
        if (radicande < 0) or not (isinstance(indice, int)):
            print "Erreur de définition ! Le radicande doit être positif et l'indice un nombre entier !"
        self.radicande = radicande
        self.indice = indice # Nombre entier
        self.coeff = coeff # Coeff devant la racine

    def __add__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return [str(self.simplifie()[0]) + "+" + str(other.simplifie()[0]), Racine(self.radicande, self.coeff + other.coeff, self.indice)]
        else:
            return str(self) + " + " + str(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return Racine(self.radicande, self.coeff - other.coeff, self.indice)
        else:
            return (str(self) + " - " + str(other), "tset")

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.coeff * other, self.indice)
        elif self.indice == other.indice:
            return Racine(self.radicande * other.radicande, self.coeff * other.coeff, self.indice)
        else:
            return str(self) + ' x ' + str(other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.coeff / other, self.indice)
        elif self.indice == other.indice:
            return Racine(self.radicande / float(other.radicande), self.coeff / float(other.coeff), self.indice)
        else:
            return str(self) + ' / ' + str(other)

    def __rdiv__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, other / float(self.coeff * self.radicande), self.indice)
        elif self.indice == other.indice:
            return Racine(other.radicande / float(self.radicande), other.coeff / float(self.coeff), self.indice)
        else:
            return str(other) + ' / ' + str(self)

    def __str__(self):
        if self.coeff == 0:
            return "0"
        else:
            if self.coeff == 1:
                coeff = ""
            else:
                coeff = decimaux(self.coeff, 1) + " \\, "
            if self.radicande == 0:
                coeff = ""
                racine = ""
                radicande = "0"
            elif self.indice == 2:
                racine = "\\sqrt{"
                radicande = decimaux(self.radicande, 1) + "}"
            else:
                racine = "\\sqrt[{0}]{{".format(self.indice)
                radicande = decimaux(self.radicande, 1) + "}"
            return coeff + racine + radicande

    def simplifie(self):
        facteurs = factor(self.radicande)
        prodfacteurs = produitfacteurs(facteurs)
        if self.indice == 2:
            racine = "\\sqrt{"
        else:
            racine = "\\sqrt[{0}]{{".format(self.indice)
        coeff = self.coeff
        radicande = self.radicande
        detail = [str(self), ' = ', str(coeff) + racine + prodfacteurs + '}']
        for element in facteurs:
            if facteurs.count(element) % self.indice == 0:
                coeff *= element
                for n in range(self.indice):
                    facteurs.remove(element)
                radicande = radicande // (element**(self.indice))
                prodfacteurs = produitfacteurs(facteurs)
                detail.append(' = ')
                detail.append(str(coeff) + ' \\times ' + racine + prodfacteurs + '}')
        if radicande == 1:
            return (coeff, detail)
        else:
            return (Racine(radicande, coeff, self.indice), detail)

def simplifie_racine(n):
    '''renvoie coeff,radicande où sqrt(n)=coeff*sqrt(radicande)'''
    if n==0:
        return 0,0
    else:
        ncar=carrerise(n)
        return int(sqrt(n//ncar)),ncar
        
class RacineDegre2:
    def __init__(self,entier=0,denominateur=1,coeff=1,radicande=0):
        self.entier=entier
        self.denominateur=denominateur
        self.coeff=coeff
        self.radicande=radicande
        self=Fractions(entier,denominateur)
        
    def __str__(self):
        numerateur=""
        if self.entier==0 and self.radicande!=0:
            numerateur=""
        else:
            numerateur=str(self.entier)
        if self.radicande!=0:
            numerateur+=tTeX(self.coeff)+"\\sqrt{"+TeX(self.radicande)+"}"
        if self.denominateur==1:
            result=numerateur
        else:
            result="\\dfrac{%s}{%s}"%(numerateur,self.denominateur)
        return result
    
    def simplifie(self,detail=False):
        coeff,radicande=simplifie_racine(self.radicande)
        coeff=(self.coeff)*int(coeff)
        simplifie=pgcd(pgcd(coeff,self.entier),self.denominateur)
        entier=self.entier//simplifie
        coeff=coeff//simplifie
        denominateur=self.denominateur//simplifie
        return RacineDegre2(entier,denominateur,coeff,radicande)
    
    def __add__(self,other):
        if isinstance(other,RacineDegre2):
            radicande=max(self.radicande,other.radicande)
            premier=self.simplifie()
            second=other.simplifie()
            denominateur=ppcm(premier.denominateur,second.denominateur)
            facteur1=denominateur/premier.denominateur
            facteur2=denominateur/second.denominateur
            if self.radicande==other.radicande:
                coeff=premier.coeff*facteur1+second.coeff*facteur2
                if coeff==0:
                    radicande=0
                return RacineDegre2(premier.entier*facteur1+second.entier*facteur2,
                                    denominateur,
                                    coeff,
                                    radicande)
        elif isinstance(other,int):
            return RacineDegre2(self.entier+self.denominateur*other,self.coeff,self.radicande)
        elif isinstance(other,Fraction):
            return RacineDegre2(self.entier*other.denominator+self.denominateur*other.numerator,
                                self.denominateur*other.denominator,
                                self.coeff*other.denominator,
                                self.radicande)
    def __radd__(self,other):
        return self+other
    def __neg__(self):
        return RacineDegre2(-self.entier,self.denominateur,-self.coeff,self.radicande)

    def __sub__(self,other):
        return self+(-other)

    def __mul__(self,other):
        if isinstance(other,Fraction):
            return self*RacineDegre2(other.numerator,other.denominator,0,self.radicande)
        elif isinstance(other,int):
            return self*RacineDegre2(other,1,0,self.radicande)
        else:
            radicande=max(self.radicande,other.radicande)#cela autorise d'avoir un radicande=0 mais n'efface pas l'autre
            coeff=self.entier*other.coeff+self.coeff*other.entier
            if coeff==0:
                radicande=0
            return RacineDegre2(self.entier*other.entier+(self.coeff*other.coeff)*self.radicande,
                            self.denominateur*other.denominateur,
                            self.entier*other.coeff+self.coeff*other.entier,
                            radicande)
    def __rmul__(self,other):
        return self*other


