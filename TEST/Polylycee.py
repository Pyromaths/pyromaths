# -*- coding: utf-8 -*-

import os,sys,codecs
from fractions import Fraction
import re

from random import randrange

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
    
           
    def TeX(self,display=True):
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

    def __eq__(self,other):
        if self.var==other.var and self.dictio==other.dictio:
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
            result= result+self.dictio[i]*x**i
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
    
def TeX_division(dividende,diviseur):
    '''renvoie une chaine de caractere TeX pour afficher la division en détail'''
    quotient=Polynome({0:0})
    texquotient,restera= dividende/diviseur
    reste=dividende
    diviseur_degre=diviseur.deg
    sauve=min(dividende.puiss+texquotient.puiss)
    longueur=dividende.degre-sauve
    string= "$$\n\\begin{array}{c"
    for i in range(longueur):
        string+= "c"
    string+= "|c}\n"
    string+=tab_print(dividende,longueur+1)
    string+= str(diviseur)+ "\\\\\n"
    string+= "\\cline{"+str(dividende.deg+2-sauve)+"-"+str(dividende.deg+2-sauve)+"}\n"
    i=0
    while reste.deg>=diviseur.deg:
        for k in range(i):
            string+= " &"
        ajout_quotient_deg=reste.deg-diviseur_degre
        facteur= reste.dictio[max(0,reste.deg)]/diviseur.dictio[diviseur.deg]
        ajout_quotient=Polynome({ajout_quotient_deg:facteur},var=dividende.var)
        soustrait_reste=ajout_quotient*diviseur
        string +=tab_print(soustrait_reste,diviseur_degre+1,parenthese=True)
        for k in range(longueur-i-diviseur.deg):
            string+= " & "
        if i ==0:
            string+= str(texquotient)
        string+= "\\\\\n"
        string+= "\\cline{"+str(i+1) +"-"+str(i+diviseur.deg+1) +"}\n"
        avant=reste.deg
        reste=reste-soustrait_reste
        delta=avant-reste.degre
        i=i+delta
        for k in range(i):
            string+= " &"
        string +=tab_print(reste,diviseur.deg)
        for k in range(longueur-i-diviseur.deg):
            string+= " & "
        string+= "\\\\ \n"
    string+= "\\end{array}\n$$"

    string+="\n On a $$"+dividende.TeX()+" = \\left(" + texquotient.TeX()+"\\right) \\times \\left("+diviseur.TeX()+"\\right)+"+restera.TeX()+"$$"
    return string
def tab_print(polynome,longueur=0,parenthese=False):
    '''utilise par TeX_division pour décaler le reste dans la partie gauche'''
    degre=polynome.degre
    string=''
    if parenthese:
        string = "-("
        fin=")"
    else:
        fin=""
    if polynome.deg<0:
        string =string+ str(0)+ " &"
    else:
        for i in range(longueur):
            k=degre-i
            coeff=polynome.dictio.get(k,0)
            if coeff>=0:
                string=string+ "+"
            string =string+ str(coeff)
            if k!=0:
                string=string+ "x"
            if k != 1 and k!=0:
                string+= u"^" + str(k)
            if longueur-i==1:
                    string+= fin
            string+= " & "
    return string

if __name__=="__main__":
    from imprimetest import *
    P=Polynome({2:4,1:8,0:1,3:0})
    Q=Polynome({2:-4,0:-1,1:8})
    R=Polynome({3:1,2:1,1:-2})
    D=Polynome({1:1,0:2})
    FR=Polynome({3:Fraction(2,3),2:Fraction(2,3),1:Fraction(-4,3)})
    print "P=", P
    print "Q=", Q
    print "R=", R
    print "FR=",FR
    R_facteur=R.factorise()
    print "R=",R.factorise(TeX=True)
    TeX_division(R,D)
    #imprime_TeX(TeX_division(P,D))
