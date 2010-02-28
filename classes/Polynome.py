# -*- coding: utf-8 -*-


if __name__=="__main__":
    import sys
    sys.path.append('/home/nicolas/pyrogit/pyromaths')

from classes.Fractions import Fractions
import re
from outils.Affichage import decimaux

from outils.Arithmetique import carrerise,pgcd,ppcm
from classes.Racine import simplifie_racine
from math import sqrt

class Polynome:
    '''Classe de polynôme pour le lycee'''
    def __init__(self, liste_coeff, var = "x"):
        self.var = var # Lettre pour la var
        liste_reduite={}
        if isinstance(liste_coeff,str):
            liste_coeff=str_Polynome(liste_coeff,var)
        elif isinstance(liste_coeff,list):
            liste_coeff=dict((i,liste_coeff[i])for i in range(len(liste_coeff)))
        elif isinstance(liste_coeff,int) or isinstance(liste_coeff,Fractions) or isinstance(liste_coeff,float):
            liste_coeff={0:liste_coeff}
        for i in liste_coeff.iterkeys():
            if liste_coeff[i] != 0:
                liste_reduite[i]=liste_coeff[i]+Fractions(0, 1)
        if liste_reduite=={} or liste_coeff==[]:
            liste_reduite={0:0}
        self.dictio = liste_reduite
        self.puiss = liste_reduite.keys()
        self.puiss.sort(reverse=True)
        self.deg=self.degre()
        self.degre_max=max(0,self.deg)

    def __len__(self):
        return max(0,self.deg)+1
    
    def degre(self):
        degre=float("-inf")
        for i in self.dictio.iterkeys():
            if i > degre and self.dictio[i] !=0:
                degre=i
        return degre

    def __getitem__(self,i):
        '''P[i] renvoie le coefficient de rang i'''
        return self.dictio.get(i,0)
    
    def __str__(self):
        '''renvoie une str pour un affichage python'''
        return self.TeX(var=self.var)
    
           
    def TeX(self,var='',display=True,parenthese=False):
        '''renvoie une chaine de caractere imprimant les fractions dans TeX'''
        if var=='':
            var=self.var
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
            elif isinstance(self.dictio[exposant],Fractions):
                if self.dictio[exposant].denominateur == 1:
                    coeff = str(self.dictio[exposant].numerateur) + ' '
                elif self.dictio[exposant].numerateur < 0:
                    coeff = "-"+fractex+"{"+str(-self.dictio[exposant].numerateur)+"}{"+str(self.dictio[exposant].denominateur)+"} "
                else:
                    coeff = fractex+"{"+str(self.dictio[exposant].numerateur)+"}{"+str(self.dictio[exposant].denominateur)+"} "
            else:
                coeff = str(self.dictio[exposant])
            if exposant == 1:
                terme = var
            elif (exposant == 0) and ((self.dictio[exposant] == 1) or (self.dictio[exposant] == -1)):
                terme = '1'
            elif exposant == 0:
                terme = ''
            else:
                terme = var + u'^' + str(exposant)
            string=string+coeff+terme
            premier=0
        if parenthese and (len(self.puiss)>1 or self[self.degre_max]<0):
            return "\\left("+string+"\\right)"
        else:
            return string

    def __add__(self, other):
        if isinstance(other,int) or isinstance(other,float) or isinstance(other,Fractions):
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
        if isinstance(other,Polynome):
            result=Polynome({0:0},var=self.var)
            for i in self.dictio.iterkeys():
                for j in other.dictio.iterkeys():
                    exposant=i+j
                    coefficient=self.dictio[i]*other.dictio[j]
                    result = result + Polynome({exposant:coefficient},var=self.var)
            return result
        else:
            return self*Polynome(other)
    def __ne__(self,other):
        return not(self == other)
    def __eq__(self,other):
        if (isinstance(other,int) or isinstance(other,Fractions) or isinstance(other,float)):
            if self.degre_max==0 and self[0]==other:
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
        if isinstance(other,int) or isinstance(other,float) or isinstance(other,Fractions):
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
            return Fractions(1,other)*self
        elif isinstance(other,Fractions) or isinstance(other,float):
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
    def simplifie(self):
        result={}
        for i in self.puiss:
            if isinstance(self[i],Fractions):
                result[i]=self[i].simplifie()
            else:
                result[i]=self[i]
        return Polynome(result)
    
    def __call__(self,x,):
        '''renvoie la Fraction ou l'int P(x)'''
        if x==float("inf") or x==float("-inf"):
            if self.degre_max==0:
                return self[0]
            elif self.deg%2==0:
                return self[self.deg]*float("inf")
            else:
                return self[self.deg]*x
        elif isinstance(x,str):
            return self.TeX(var=x)
        else:
            result=0
            for i in self.dictio.iterkeys():
                result= result+self[i]*x**i
            if isinstance(result,Fractions):
                result=result.simplifie()
            if result.denominateur==1:
                return result.numerateur
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
                result[i-1]=int(i)*self[i]
        return Polynome(result,self.var)
    def primitive(self):
        result={}
        for i in self.dictio.iterkeys():
            result[i+1]=Fractions(1,int(i+1))*self.dictio[i]
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
                    termes[1]=coeff * Fractions(eval(a[0]))
                elif (len(a) == 1) and (re.findall(var, element)):
                    termes[int(a[0])]=coeff * 1
                elif (len(a) == 1):
                    termes[0]=coeff * Fractions(eval(a[0]))
                else:
                    termes[int(a[1])]=coeff * Fractions(eval(a[0]))
    return termes

if __name__=="__main__":
    from TEST.imprimetest import *
    X=Polynome("x")
    P=Polynome({2:4,1:8,0:1,3:0})
##    Q=Polynome({2:-4,0:-1,1:8})
##    R=Polynome({3:1,2:1,1:-2})
##    D=Polynome({1:1,0:2})
##    F=Polynome("x-4")
##    FF=Polynome("x^2-3")
##    Divi=FF*F+7
##    FR=Polynome({3:Fractions(2,3),2:Fractions(2,3),1:Fractions(-4,3)})
##    print "P=", P
##    print "Q=", Q
##    print "R=", R
##    print "FR=",FR
##    R_facteur=R.factorise()
##    print "R=",R.factorise(TeX=True)
##    #TeX_division(R,D)
##    print Divi*Polynome("x^3")-28*X
##    #imprime_TeX(TeX_division(Divi*Polynome("x^3")-28*X,F*X))
