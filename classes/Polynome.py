# -*- coding: utf-8 -*-

import os,sys,codecs
if __name__=="__main__":
    sys.path.append('/home/nicolas/pyrogit/pyromaths')

from fractions import Fraction
import re
from outils.Arithmetique import carrerise,pgcd,ppcm
from classes.Racine import simplifie_racine
from math import sqrt
from outils.TeXMiseEnForme import TeXMiseEnForme
sepmilliers=TeXMiseEnForme("").sepmilliers
from random import randrange,randint

class Polynome:
    '''Classe de polynôme pour le lycee'''
    def __init__(self, liste_coeff, var = "x"):
        self.var = var # Lettre pour la var
        liste_reduite={}
        if liste_coeff=={} or liste_coeff==[]:
            liste_reduite={0:0}        
        elif isinstance(liste_coeff,str):
            liste_coeff=str_Polynome(liste_coeff,var)
        elif isinstance(liste_coeff,list):
            liste_coeff=dict((i,liste_coeff[i])for i in range(len(liste_coeff)))
        elif isinstance(liste_coeff,int) or isinstance(liste_coeff,Fraction) or isinstance(liste_coeff,float):
            liste_coeff={0:liste_coeff}
        for i in liste_coeff.iterkeys():
            if liste_coeff[i] != 0:
                liste_reduite[i]=liste_coeff[i]+Fraction(0, 1)
        if liste_reduite=={} or liste_coeff==[]:
            liste_reduite={0:0}
        self.dictio = liste_reduite
        self.puiss = liste_reduite.keys()
        self.puiss.sort(reverse=True)
        self.deg=self.degre()
        self.degre=max(0,self.deg)

    def degre(self):
        degre=-8
        for i in self.dictio.iterkeys():
            if i > degre and self.dictio[i] !=0:
                degre=i
        return degre
    def __getitem__(self,i):
        '''P[i] renvoie le coefficient de rang i'''
        return self.dictio.get(i,0)
    
    def __str__(self):
        '''renvoie une str pour un affichage python'''
        exposants = []+self.puiss
        premier = 1
        string=''
        for exposant in exposants :
            if not(premier) and self.dictio[exposant]>=0:
                string=string+ " + "
            if self.dictio[exposant] == 1:
                coeff = ''
            elif self.dictio[exposant] == -1:
                coeff = '-'
            else:
                coeff = str(self.dictio[exposant])
            if exposant == 1:
                terme = self.var
            elif (exposant == 0) and ((self.dictio[exposant] == 1) or (self.dictio[exposant] == -1)):
                terme = '1'
            elif exposant == 0:
                terme = ''
            else:
                terme = self.var+u'^'+str(exposant)
            string=string+coeff+terme
            premier=0
        return string
    
           
    def TeX(self,display=True,parenthese=False):
        '''renvoie une chaine de caractere imprimant les fractions dans TeX'''
        
        exposants = []+self.puiss
        premier = 1
        string=''
        if display:
            fractex="\\dfrac"
        else:
            fractex="\\frac"
        for exposant in exposants :
            if not(premier) and self.dictio[exposant]>=0:
                string=string+ " + "
            if self.dictio[exposant] == 1:
                coeff = ''
            elif self.dictio[exposant] == -1:
                coeff = '-'
            elif isinstance(self.dictio[exposant],Fraction):
                if self.dictio[exposant].denominator == 1:
                    coeff = str(self.dictio[exposant].numerator) + ' '
                elif self.dictio[exposant].numerator < 0:
                    coeff = "-"+fractex+"{"+str(-self.dictio[exposant].numerator)+"}{"+str(self.dictio[exposant].denominator)+"} "
                else:
                    coeff = fractex+"{"+str(self.dictio[exposant].numerator)+"}{"+str(self.dictio[exposant].denominator)+"} "
            else:
                coeff = str(self.dictio[exposant])
            if exposant == 1:
                terme = self.var
            elif (exposant == 0) and ((self.dictio[exposant] == 1) or (self.dictio[exposant] == -1)):
                terme = '1'
            elif exposant == 0:
                terme = ''
            else:
                terme = self.var + u'^' + str(exposant)
            string=string+coeff+terme
            premier=0
        if parenthese and (len(self.puiss)>1 or self[self.degre]<0):
            return "\\left("+string+"\\right)"
        else:
            return string

    def __add__(self, other):
        if isinstance(other,int) or isinstance(other,float) or isinstance(other,Fraction):
            return self+Polynome({0:other},var=self.var)
        result={0:0}
        liste1=self.puiss
        liste2=other.puiss
        for i in liste1 :
            s=self.dictio.get(i)+other.dictio.get(i,0)
            if s!=0:
                result[i]=s
        for i in liste2:
            if i not in liste1:
                result[i]=other.dictio[i]
        return Polynome(result,var=self.var)
    
    def __mul__(self, other):
        result=Polynome({0:0},var=self.var)
        for i in self.dictio.iterkeys():
            for j in other.dictio.iterkeys():
                exposant=i+j
                coefficient=self.dictio[i]*other.dictio[j]
                result = result + Polynome({exposant:coefficient},var=self.var)
        return result
    def __ne__(self,other):
        return not(self == other)
    def __eq__(self,other):
        if (isinstance(other,int) or isinstance(other,Fraction) or isinstance(other,float)):
            if self.degre==0 and self[0]==other:
                return True
            else:
                return False
        elif self.var==other.var and self.dictio==other.dictio:
            return True
        else:
            return False
    
    def __pow__(self, other):
        if isinstance(other,int) and other>=0:
            result=Polynome({0:1},self.var)
            for i in xrange(other):
                result*=self
            return result

    def __radd__(self, other):
        if isinstance(other,int) or isinstance(other,float) or isinstance(other,Fraction):
            return self+Polynome({0:other},var=self.var)
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -(self - other)

    def __neg__(self):
        return self * Polynome({0:-1},var=self.var)

    def __rmul__(self,nombre):
        return self*Polynome({0:nombre})
    
    def __div__(self,other):
        if isinstance(other,int):
            return Fraction(1,other)*self
        elif isinstance(other,Fraction) or isinstance(other,float):
            return (1/other)*self
        else:
            quotient=Polynome({},var=self.var)
            reste=self
            diviseur_degre=other.deg
            while diviseur_degre <= reste.deg:
                ajout_quotient_deg=reste.deg-diviseur_degre
                facteur= reste.dictio[reste.deg]/other.dictio[other.deg]
                ajout_quotient=Polynome({ajout_quotient_deg:facteur},var=self.var)
                quotient=quotient+ajout_quotient
                soustrait_reste=ajout_quotient*other
                reste=reste-soustrait_reste
            return quotient,reste
    def __rdiv__(self,other):
        if isinstance(other,Polynome):
            return other/self
        elif isinstance(other,int):
            return Fraction(1,other)*self
        elif isinstance(other,Fraction) or isinstance(other,float):
            return (1/other)*self
    
    def __call__(self,x):
        '''renvoie la Fraction ou l'int P(x)'''
        result=0
        for i in self.dictio.iterkeys():
            result= result+self[i]*x**i
        if isinstance(result,Fraction) and result.denominator==1:
            return result.numerator
        else:
            return result

    def racine_evidente(self,liste=[-2,-1,0,1,2]):
        listerac=[]
        for i in liste:
            if self(i)==0:
                listerac=listerac+[i]
        return listerac

    def factorise(self,TeX=False,racines=[0,-1,1,2,-2]):
        facteurs=[Polynome({0:self.dictio[self.deg]},var=self.var)]
        developpe,reste=self/facteurs[0]
        for r in racines: 
            while developpe(r)==0:
                rac=-r
                developpe,reste = developpe/Polynome({1:1,0:rac},var=self.var)
                facteurs=facteurs+[Polynome({1:1,0:rac})]
        if TeX:
            stringTeX=""
            if not(facteurs[0]==Polynome({0:1},var=self.var)):
                stringTeX+=facteurs[0].TeX()
            for i in facteurs[1:]:
                if i[0]!=0:
                    stringTeX+="\\left("+i.TeX()+"\\right) \\times "
                else:
                    stringTeX+=i.TeX()+" \\times "
            if developpe==Polynome({0:1},var=self.var):
                return stringTeX[:-7]
            else:
                return stringTeX+"\\left("+developpe.TeX()+"\\right)"
        else:
            return facteurs + [developpe]

    def derive(self):
        result={}
        for i in self.dictio.iterkeys():
            if i == 0:
                result[0]=0
            else:
                result[i-1]=int(i)*self.dictio[i]
        return Polynome(result,self.var)
    def primitive(self):
        result={}
        for i in self.dictio.iterkeys():
            result[i+1]=Fraction(1,int(i+1))*self.dictio[i]
        return Polynome(result,self.var)
    
def str_Polynome(string,var='x'):
    '''str -> dict'''
    #TODO reconnaitre les coefficients fractionnaires
    resultat = []
    termes = {}
    separeplus = (string).split("+")
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
            if element==var:
                termes[1]=(coeff)
            else:
                a = re.findall('\d+(?:\.\d*)?', element)
                if (len(a) == 1) and (not re.findall('\^', element)) and (re.findall(var, element)):
                    termes[1]=coeff * Fraction(a[0])
                elif (len(a) == 1) and (re.findall(var, element)):
                    termes[int(a[0])]=coeff * 1
                elif (len(a) == 1):
                    termes[0]=coeff * Fraction(a[0])
                else:
                    termes[int(a[1])]=coeff * Fraction(a[0])
    return termes 
    
class RacineDegre2:
    def __init__(self,entier=0,denominateur=1,coeff=1,radicande=0):
        self.entier=entier
        self.denominateur=denominateur
        self.coeff=coeff
        self.radicande=radicande
        self=Fraction(entier,denominateur)
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
    
    def simplifie(self):
        coeff,radicande=simplifie_racine(self.radicande)
        coeff=(self.coeff)*int(coeff)
        simplifie=pgcd(pgcd(coeff,self.entier),self.denominateur)
        entier=self.entier/simplifie
        coeff=coeff/simplifie
        denominateur=self.denominateur/simplifie
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

    
    def __pow__(self,n):
        result=1
        for i in range(n):
            result=result*self
        return result

    def __div__(self,other):
        return "pas fait"
    def __int__(self):
        return int((self.entier+self.coeff*sqrt(self.radicande))/self.denominateur)


if __name__=="__main__":
    from TEST.imprimetest import *
    X=Polynome("x")
##    P=Polynome({2:4,1:8,0:1,3:0})
##    Q=Polynome({2:-4,0:-1,1:8})
##    R=Polynome({3:1,2:1,1:-2})
##    D=Polynome({1:1,0:2})
##    F=Polynome("x-4")
##    FF=Polynome("x^2-3")
##    Divi=FF*F+7
##    FR=Polynome({3:Fraction(2,3),2:Fraction(2,3),1:Fraction(-4,3)})
##    print "P=", P
##    print "Q=", Q
##    print "R=", R
##    print "FR=",FR
##    R_facteur=R.factorise()
##    print "R=",R.factorise(TeX=True)
##    #TeX_division(R,D)
##    print Divi*Polynome("x^3")-28*X
##    #imprime_TeX(TeX_division(Divi*Polynome("x^3")-28*X,F*X))
