# -*- coding: utf-8 -*-
from Polylycee import *
from random import randrange,randint
from math import *
import sys, os, codecs
pyropath=os.path.normpath(os.path.join(os.getcwd(),'..'))
sys.path.append(pyropath)
from outils.Arithmetique import carrerise,pgcd

def Exo_factorisation():
    '''exercice de factorisation'''

    #intervalle pour les racines entières ou fractionnaire
    rac_min=-10
    rac_max=10
    #denominateur maximmum pour les racines fractionnaires
    denom_max=denom1=12
    #Valeurs absolues maximales des coefficients d'un polynôme quelconque
    abs_a=1
    abs_b=10
    abs_c=10
    #X est le polynome P=x pour faciliter la construction des polynômes, TODO : changer  l'inconnue
    inconnues=['x','y','z','t']
    nom_poly=['P','Q','R','S']
    exo="\\exercice\n"
    cor="\\exercice*\n"
    exo+="\\begin{enumerate}\n"
    cor+="\\begin{enumerate}\n"
    global info
    info="(identite)"
    for i in range(13):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        exo,cor=identites_remarquables(exo,cor,rac_min,rac_max,X)
    cor+="\\pagebreak\n"
    info="(rac entieres)"
    for i in range(13):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_entieres(rac_min,rac_max,X)
        exo,cor=degre2racine(exo,cor,P)
    cor+="\\pagebreak\n"
        #exo,cor=degre2racine_entiere(exo,cor,rac_min,rac_max,X)
    info="(fractions)"
    for i in range(13):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_fractionnaires(rac_min,rac_max,denom1,X)
        exo,cor=degre2racine(exo,cor,P)
    cor+="\\pagebreak\n"
        #exo,cor=degre2racinefractionnaire(exo,cor,rac_min,rac_max,denom1,X)
    info="(quelconque)"
    for i in range(13):
        #exo,cor=degre2racinequelconque(exo,cor,abs_a=1,abs_b=10,abs_c=10,X=X)
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)
        exo,cor=degre2racine(exo,cor,P)
    cor+="\\pagebreak\n"
    exo+="\\end{enumerate}\n\\baselineskip=2mm\n\\parskip=5mm"
    cor+="\\end{enumerate}\n"
    return exo,cor

def degre2racine(exo,cor,P):
    var=P.var
    #X=Polynome({1:1},var=P.var)
    delta=int(P[1]**2-4*P[2]*P[0])
    exo+=u"\\item "+info+u" Factoriser le polynôme $$P="+P.TeX()+"$$\n"

    cor+="\\item Je calcule $\Delta="+pTeX(P[1])+u"^2-4\\times"+pTeX(P[2])+"\\times"+pTeX(P[0])+"="\
    +TeX(delta)+"$"
    if delta<0:
        cor+=" donc P n'a pas de racines."
    elif delta==0:
        x0=Fraction(-1,2)*P[1]/P[2]
        cor+=" donc $P$ a une seule racine $"+var+"_0="+TeX(x0)+"$.\\par\n"
        cor+=u"Ainsi $P$ peut s'écrire $P="
        if P[2]!=1:
            cor+=TeX(P[2])
        cor+="{\\left("+(Polynome({1:1,0:-x0},var=P.var)).TeX()+u"\\right)}^2$.\n"
    else:
        rac_delta,simplrac,strx1,x1,strx2,x2,parenthesex1,parenthesex2=listeracines(P[2],P[1],delta)
        if simplrac:
            cor+=" et $"+radicalTeX(delta)+"="+rac_delta+"$"
        cor+=".\par\n"
        cor+=" Les racines de $P$ sont $"+var+"_1="+ strx1 +"="+x1 +"$ et $"+var+"_2="+ strx2 + "="+x2 +"$.\n"
        cor+=u"\\\\ Donc $P$ peut s'écrire $P=\n"
        if parenthesex1:
            x1="\\left("+x1+"\\right)"
        if parenthesex2:
            x2="\\left("+x2+"\\right)"
        cor+=TeX(P[2])+"\\times\\left("+var+"-"+x1+"\\right)\\times\\left("+var+"-"+x2+"\\right)$.\n"
    return exo,cor

def poly_racines_quelconques(abs_a,abs_b,abs_c,X):
    a3=(2*randrange(2)-1)*randrange(1,abs_a+1)
    b3=randrange(abs_b)
    c3=randrange(-abs_c,abs_c)
    return a3*X**2+b3*X+c3
def poly_racines_fractionnaires(rac_min,rac_max,denom1,X,deltanul=False):
    delta=0
    pol2=[0,0]
    while (delta==0 and pol2[1]==0) and (not(deltanul) or delta!=0):
        #pour éviter P=77x^2
        a2=2*randrange(2)-1 #a2=-1 ou 1
        p2facteur=[randint(1,denom1)*X-randint(rac_min,rac_max)for i in range(2)]
        pol2=a2*p2facteur[0]*p2facteur[1]
    return pol2
def poly_racines_entieres(rac_min,rac_max,X):
    a1=1
    p1facteur=[X-randrange(rac_min,rac_max) for i in range(2)]
    pol1=a1*p1facteur[0]*p1facteur[1]
    return pol1


def identites_remarquables(exo,cor,rac_min,rac_max,X):
    a=randint(1,10)
    while 1:
        coeff=randrange(rac_min,rac_max)
        racine=randrange(rac_min,rac_max)
        if coeff!=0 and racine!=0:
            break
    sgns=[[-1,1][randrange(2)]for i in range(2)]
    p1facteur=[coeff*X+sgns[i]*racine for i in range(2)]
    pol1=a*p1facteur[0]*p1facteur[1]

    #pol1=a1*(coeff X ± racine)(coeff X ± racine)
    a1=pgcd(int(pol1[0]),pgcd(int(pol1[1]),int(pol1[2])))#du signe de a=pol1[2]
    if a1!=1 or a1!=-1:
        pol2=pol1/a1
    else:
        pol2=pol1
    #coeff=coeff/int(math.sqrt(a1))
    #pol2=(cx)^2 ±2× cx × b + b^2
    #pol2[2]=c^2
    #pol2[1]=2× cx × b
    #pol2[0] = b^2
    c=int(sqrt(pol2[2]))
    exo+="\\item "+info+u" Factoriser le polynôme $$P="+pol1.TeX()+"$$\n"
    if a1!=1:
        cor+="\\item On remarque que $P="+pol1.TeX()+"="+TeX(a1)+"\\times\\big["+(pol1/a1).TeX()+"\\big]$"
        cor+="="+TeX(a1)+"\\times \\big["
    else:
        cor+="\\item $P="+pol1.TeX()+"="
    if c!=1:
        cor+="("+TeX(c)+X.var+u")^2"
    else:
        cor+=X.var+u"^2"
    if sum(sgns):
        if sgns[0]==-1:
            cor+= "-2 \\times "
        else:
            cor+= "+2 \\times"
        if c<0:
            cor+="\\left("+TeX(c)+X.var+"\\right)"
        elif c==1:
            cor+=X.var
        else:
            cor+=TeX(c)+X.var
        b=int(sqrt(pol2[0]))
        cor+=" \\times "+TeX(b)
        cor+="+"
        
    else:
        cor+="-"
        b=int(sqrt(-(pol2[0])))
    cor+=TeX(b)+u"^2"
    if a1!=1:
        cor+="\\big]"
    cor+="$\\\\\n"
    cor+="Ainsi $P="
    if a1!=1:
        cor+=TeX(a1)
    if sum(sgns):#(cx-b)² ou (cx+b)²
        cor+="{("+ (c*X+sgns[0]*b).TeX() +")}^2$"
    else:#(cx-b)(cx+b)
        cor+="("+ (c*X+b).TeX() +")("+(c*X-b).TeX()+")$"
    return exo,cor


def TeXz(nombre):
    '''n'affiche pas b si b=0'''
    if nombre==0:
        return ""
    else:
        return TeX(nombre)

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
    elif terme and nombre>0:
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
    return strx1,strx2
def listeracines(a,b,delta):
    '''renvoie racsimple,simplifie,formule_x1,x_1,formule_x2,x2'''
    '''avec x_1<x_2'''
    '''On suppose delta >0'''
    '''simplrac est True si racine de delta se simplifie'''

    parenthesex1=parenthesex2=True #par défaut
    simplrac=True
    strx1="\\dfrac{-"+pTeX(b)+"-\\sqrt{"+TeX(delta)+"}}{2\\times"+pTeX(a)+"}"
    strx2="\\dfrac{-"+pTeX(b)+"+\\sqrt{"+TeX(delta)+"}}{2\\times"+pTeX(a)+"}"
    ##on a strx1<strx2
    coeff,radicande=simplifie_racine(delta)
    if radicande==1:#delta est un carré
        rac_delta=TeX(coeff)
        x1=TeX(Fraction(1)*(-b-coeff)/(2*a))
        x2=TeX(Fraction(1)*(-b+coeff)/(2*a))
        #les racines sont fractionnaires ou entières
        parenthesex1=((b+coeff)*a>0)
        parenthesex2=((b-coeff)*a>0)
    else:
        #x1,x2 simplifiés ont une écriture fracionnaire donc
        parenthesex1=parenthesex2=False
        if coeff==1:#delta n'a pas de facteur carré, on ne peut rien simplifier
            rac_delta=radicalTeX(delta)
            simplrac=False
        else:
            rac_delta=TeX(coeff)+radicalTeX(radicande)                
        simplifie=pgcd(pgcd(b,coeff),2*a)#simplifie est négatif si a<0
        if simplifie==coeff:
            rac_delta1="-"+radicalTeX(radicande)
            rac_delta2="+"+radicalTeX(radicande)
        elif simplifie==-coeff:
            rac_delta1="+"+radicalTeX(radicande)
            rac_delta2="-"+radicalTeX(radicande)
        else:
            rac_delta1=tTeX(-coeff/simplifie)+radicalTeX(radicande)
            rac_delta2=tTeX(coeff/simplifie)+radicalTeX(radicande)
        if simplifie==2*a:
            x1=TeXz(-b/simplifie)+rac_delta1
            x2=TeXz(-b/simplifie)+rac_delta2
            #plus de barre de fraction donc
            parenthesex1=parenthesex2=True
        else:
            x1="\\dfrac{"+TeXz(-b/simplifie)+rac_delta1+"}{"+TeX(2*a/simplifie)+"}"
            x2="\\dfrac{"+TeXz(-b/simplifie)+rac_delta2+"}{"+TeX(2*a/simplifie)+"}"
        if b==0:
            parenthesex1=(coeff*a>0)
            parenthesex2=(coeff*a<0)
    if a<0:
        strx1,strx2,x1,x2,parenthesex1,parenthesex2=strx2,strx1,x2,x1,parenthesex2,parenthesex1
    return rac_delta,simplrac,strx1,x1,strx2,x2,parenthesex1,parenthesex2

if __name__=="__main__":
    from imprimetest import *
    exo,cor=Exo_factorisation()#denom1=12)
    imprime_TeX(exo+'\\pagebreak'+cor)
