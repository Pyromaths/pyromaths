# -*- coding: utf-8 -*-
from Polylycee import *
from random import randrange
from math import *
import sys, os, codecs
pyropath=os.path.normpath(os.path.join(os.getcwd(),'..'))
sys.path.append(pyropath)
from outils.Arithmetique import carrerise,pgcd

def Exo_factorisation(rac_min=-10,rac_max=10,denom1=5,var='x'):
    '''exercice de factorisation'''

    X=Polynome({1:1},var=var)
    exo="\\exercice\n"
    cor="\\exercice*\n"
    exo+="\\begin{enumerate}\n"
    cor+="\\begin{enumerate}\n"

    exo,cor=identites_remarquables(exo,cor,rac_min,rac_max,X)
    
    exo,cor=degre2racine_entiere(exo,cor,rac_min,rac_max,X)
    
    for i in range(3):
        degre2racinefractionnaire(exo,cor,rac_min,rac_max,denom1,X)

    for i in range(7):
        a3=2*randrange(2)-1
        b3=randrange(10)
        c3=randrange(-10,10)
        pol3=a3*X**2+b3*X+c3
        delta=int(pol3[1]**2-4*pol3[2]*pol3[0])
        exo+=u"\item (unitaire) Factoriser le polynôme $$P="+pol3.TeX()+"$$\n"

        cor+="\\item Je calcule $\Delta=("+str(pol3[1])+u")^2-4\\times("+str(pol3[2])+"\\times"+str(pol3[0])+")="\
        +str(delta)+"$\n"
        if delta<0:
            cor+=" donc P n'a pas de racines."
        elif delta==0:
            cor+=" donc $P$ a une seule racine."
        else:
            coeff,radicande=simplifie_racine(delta)
            if radicande==1:
                rac_delta=TeX(coeff)
                egalx1="="+TeX(Fraction(-b3+coeff,2*a3))
                egalx2="="+TeX(Fraction(-b3-coeff,2*a3))
            elif coeff==1:
                    rac_delta=radicalTeX(delta)
                    egalx1="=\\dfrac{"+TeX(-b3)+"+"+rac_delta+"}{"+TeX(2*a3)+"}"
                    egalx2="=\\dfrac{"+TeX(-b3)+"-"+rac_delta+"}{"+TeX(2*a3)+"}"
            else:
                rac_delta=TeX(coeff)+radicalTeX(radicande)                
                simplifie=pgcd(pgcd(b3,coeff),2*a3)                    
                if simplifie==coeff:
                    rac_delta1="+"+TeX(coeff/simplifie)+radicalTeX(radicande)
                    rac_delta2="-"+TeX(coeff/simplifie)+radicalTeX(radicande)
                else:
                    rac_delta1="+"+radicalTeX(radicande)
                    rac_delta2="-"+radicalTeX(radicande)                    
                if simplifie==2*a3:
                    egalx1="="+TeX(-b3/simplifie)+rac_delta1
                    egalx2="="+TeX(-b3/simplifie)+rac_delta2
                else:
                    egalx1="=\\dfrac{"+TeX(-b3/simplifie)+rac_delta+"}{"+TeX(2*a3/simplifie)+"}"
                    egalx2="=\\dfrac{"+TeX(-b3/simplifie)+rac_delta+"}{"+TeX(2*a3/simplifie)+"}"
            strx1,strx2=TeXracines(pol3[2],pol3[1],delta,simple=False)
            cor+="et $\sqrt{"+str(delta)+"}="+rac_delta+"$.\par\n"
            cor+=" Les racines de $P$ sont $x_1="+ strx1 +egalx1 +"$ et $x_2="+ strx2 + egalx2 +"$.\n"
            cor+=u"\\\\ Donc $P$ peut s'écrire $P=$\n"
        
    exo+="\\end{enumerate}\n\\baselineskip=2mm\n\\parskip=5mm"
    cor+="\\end{enumerate}\n"
    return exo,cor

def degre2racinefractionnaire(exo,cor,rac_min,rac_max,denom1,X):
    a2=2*randrange(2)-1 #a2=-1 ou 1
    p2facteur=[randrange(2,denom1)*X-randrange(rac_min,rac_max)\
               for i in range(2)]
    pol2=a2*p2facteur[0]*p2facteur[1]
    x1=-(p2facteur[0][0])/p2facteur[0][1]
    x2=-(p2facteur[1](0))/p2facteur[1][1]

    if x1>x2:
        x1,x2=x2,x1
    delta=pol2[1]**2-4*pol2[2]*pol2[0]
    exo+=u"\item (fraction) Factoriser le polynôme $$P="+pol2.TeX()+"$$\n"
    strx1,strx2=TeXracines(pol2[2],pol2[1],delta)
    cor+="\\item Je calcule $\Delta=("+str(pol2[1])+u")^2-4\\times("+str(pol2[2])+"\\times"+str(pol2[0])+")$="\
    +str(delta)+"\n"
    cor+="et $\sqrt{"+str(delta)+"}="+str(int(sqrt(delta)))+"$.\par\n"
    cor+=u" Les racines de $P$ sont $x_1="+strx1+"="+ TeX(x1) +"$ et $x_2="+strx2+"="+TeX(x2)  +"$.\n"
    cor+=u"\\\\ Donc $P$ peut s'écrire $P="
    cor+=TeX(pol2[2])+"\\times\\left("+(X-x1).TeX()+"\\right)\\times\\left("+(X-x2).TeX()+"\\right)$.\n"

def identites_remarquables(exo,cor,rac_min,rac_max,X):
    a1=randrange(1,11)
    racine=randrange(rac_min,rac_max)
    sgns=[-1,1]
    p1facteur=[X+sgns[i]*racine for i in range(2)]
    pol1=a1*p1facteur[0]*p1facteur[1]

    exo+=u"\\item(identite) Factoriser le polynôme $$P="+pol1.TeX()+"$$\n"
    cor+=u"\\item On remarque que $P="+str(a1)+"\\times("+(pol1/a1).TeX()+")$\n"
    cor+=u"\\\\ Donc $P$ peut s'écrire $P="
    cor+=str(a1)+"\\times\\left("+p1facteur[0].TeX()+"\\right)\\times\\left("+p1facteur[1].TeX()+"\\right)$."
    return exo,cor

def degre2racine_entiere(exo,cor,rac_min,rac_max,X):
    a1=a2=1
    p2facteur=[X-randrange(rac_min,rac_max) for i in range(2)]
    pol2=a2*p2facteur[0]*p2facteur[1]
    x1=-(p2facteur[0][0])
    x2=-(p2facteur[1](0))
    if x1>x2:
        x1,x2=x2,x1
    delta=pol2[1]**2-4*pol2[2]*pol2[0]
    strx1,strx2=TeXracines(pol2[2],pol2[1],delta)
    exo+=u"\\item(facile) Factoriser le polynôme $$P="+pol2.TeX()+"$$\n"
    cor+="\\item Je calcule $\Delta=("+str(pol2[1])+u")^2-4\\times("+str(pol2[2])+"\\times"+str(pol2[0])+")$="\
        +str(delta)+"\n"
    cor+="et $\sqrt{"+str(delta)+"}="+str(int(sqrt(delta)))+"$.\par\n"           
    cor+=u" Les racines de $P$ sont $x_1="+ strx1 +"="+TeX(x1)+"$ et $x_2="+strx2  +"="+TeX(x2)+"$.\n"
    cor+=u"\\\\ Donc $P$ peut s'écrire $P="
    cor+=str(a1)+"\\times\\left("+p2facteur[0].TeX()+"\\right)\\times\\left("+p2facteur[1].TeX()+"\\right)$."
    return exo,cor

def tTeX(nombre):
    '''raccourci pour TeX(nombre,terme=True)'''
    return TeX(nombre,terme=True)
def pTeX(nombre):
    '''raccourci pour TeX(nombre,parenthese=True)'''
    return TeX(nombre,parenthese=True)
def TeX(nombre,parenthese=False,terme=False):
    '''renvoie une chaine de caractere pour TeX'''
    if parenthese and nombre<0:
        strTeX="\\left("
        finTeX="\\right)"
    elif terme:
        strTeX="+"
        finTeX=""
    else:
        strTeX=finTeX=""
    if isinstance(nombre,Fraction):
        fractex="\\dfrac"
        if nombre.denominator == 1:
            strTeX += str(nombre.numerator) + ' '
        elif nombre.numerator < 0:
            strTeX += "-"+fractex+"{"+str(-nombre.numerator)+"}{"+str(nombre.denominator)+"} "
        else:
            strTeX += fractex+"{"+str(nombre.numerator)+"}{"+str(nombre.denominator)+"} "
        return strTeX+finTeX
    else:
        return strTeX+str(nombre)+finTeX

def radicalTeX(n):
    return "\\sqrt{"+TeX(n)+"}"
def simplifie_racine(n):
    ##La classe classes.Racine.py doit faire cela aussi bien
    if n==0:
        return "0",0
    else:
        ncar=carrerise(n)
        if ncar==1:
            return int(sqrt(n)),1
        elif ncar==n:
            return 1,ncar
        else:
            return int(sqrt(n/ncar)),ncar

def TeXracines(a,b,delta,simple=True):
    '''renvoie la formule des racines sous forme TeX'''
    strx1="\\dfrac{-"+pTeX(b)+"-\\sqrt{"+TeX(delta)+"}}{2\\times"+pTeX(a)+"}"
    strx2="\\dfrac{-"+pTeX(b)+"+\\sqrt{"+TeX(delta)+"}}{2\\times"+pTeX(a)+"}"
    if simple:
        if a>0:
            return strx1,strx2
        else:
            return strx2,strx1
    x1=(-b-sqrt(delta))/(2*a)
    x2=(-b+sqrt(delta))/(2*a)
    if a>0:
        return strx1,strx2
    else:
        return strx1,strx2

if __name__=="__main__":
    from imprimetest import *
    exo,cor=Exo_factorisation()
    imprime_TeX(exo+'\\pagebreak'+cor)
