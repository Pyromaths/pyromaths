# -*- coding: utf-8 -*-

if __name__=="__main__":
    import sys
    sys.path.append("/home/nicolas/pyrogit/pyromaths")

from classes.Polynome import *
from outils.TeXMiseEnForme import *
from random import randrange,randint
from math import *
from re import findall
from outils.Arithmetique import pgcd
from outils.Polynomes import *
from classes.Fractions import Fractions

def exo_fonctions_rationnelles():
    var=['t','x'][randrange(2)]
    X=Polynome({1:1},var)
    #intervalle pour les racines entières ou fractionnaire
    rac_min=-10
    rac_max=10
    b1=b2=a1=a2=0
    while b1==0 or b2==0 or a1==0 or a2==0:
        b1=randint(rac_min,rac_max)
        b2=randint(rac_min,rac_max)
        a1=randint(-5,5)
        a2=randint(-5,5)
    P=a1*X+b1
    Q=a2*X+b2
    Intervalle=[rac_min,rac_max]
    nomf=['f','g','h','k'][randrange(4)]
    #Je veux que f soit définie et dérivable sur I=Intervalle
    if (-Q[0]/Q[1])>=rac_min and (-Q[0]/Q[1])<=rac_max:
        if ((-Q[0]/Q[1])-rac_min)<(rac_max-(-Q[0]/Q[1])):
            Intervalle=[int(-Q[0]/Q[1])+1,rac_max]
        else:
            Intervalle=[rac_min,int(-Q[0]/Q[1])-1]
    #dérivée
    numerateur="%s\\times%s-%s\\times%s"%\
                (P.derive().TeX(parenthese=True),Q.TeX(parenthese=True),P.TeX(parenthese=True),Q.derive().TeX(parenthese=True))
    numerateur_simplifie=P.derive()*Q-P*Q.derive()
    denominateur=u"%s^2"%(Q.TeX(parenthese=True))
    f_derivee="\\dfrac{%s}{%s}"%(numerateur,denominateur)
    f_derivee_simplifiee="\\dfrac{%s}{%s}"%(numerateur_simplifie,denominateur)
    exo=u"On considère la fonction $%s$ définie sur $I=[%s~;~%s]$ par $%s(%s)=\dfrac{%s}{%s}$.\n"%\
          (nomf,Intervalle[0],Intervalle[1],nomf,var,P,Q)
    exo+="\\begin{enumerate}\n"
    cor="\\begin{enumerate}\n"
    exo+=u"\\item Justifier que $%s$ est définie et dérivable sur $I$.\n"%(nomf)
    cor+=u"\\item Pour déterminer la valeur interdite on doit résoudre $%s=0$.\n\n"%(Q)
    cor+="\\begin{align*}\n\
            %s&=0\\\\\n\
            %s&=%s\\\\\n\
            %s&=%s\n\
            \\end{align*}\n"%(Q,(Q-Q[0]),TeX(-Q[0]),var,TeX(-Q[0]*Fractions(1)/Q[1]))
    cor+=u"Or $%s$ n'est pas dans l'intervalle $[%s~;~%s]$ donc $%s$ est bien définie et dérivable sur $I$.\n"%\
          (TeX(-Q[0]*Fractions(1)/Q[1]),Intervalle[0],Intervalle[1],nomf)
    exo+=u"\\item Déterminer $%s'(%s)$ pour tout $%s\in[%s~;~%s]$.\n"%\
          (nomf,var,var,Intervalle[0],Intervalle[1])
    cor+=u"\\item $$%s'(%s)=%s=%s$$\n"%(nomf,var,f_derivee,f_derivee_simplifiee)
    exo+=u"\\item En déduire le sens de variations de $%s$ sur $I$.\n"%(nomf)
    if numerateur_simplifie.degre==0:
        cor+=u"\\item Comme $%s$ est un carré, il est toujours positif.\\\\\n"%(denominateur)
        f_xmin=TeX(Fractions(1)*P(Intervalle[0])/Q(Intervalle[0]))
        f_xmax=TeX(Fractions(1)*P(Intervalle[1])/Q(Intervalle[1]))
        if numerateur_simplifie[0]<0:
            cor+=u" De plus, $%s<0$ donc pour tout $%s$ de $I$, $%s'(%s)<0$. Ainsi, on obtient \n"%\
                  (numerateur_simplifie[0],var,nomf,var)
            cor+="$$\\tabvar{\n"
            cor+="\\tx{%s}&\\tx{%s}&&\\tx{%s}\\cr\n"%(var,TeX(Intervalle[0]),TeX(Intervalle[1]))
            cor+="\\tx{%s'(%s)}&&\\tx{-}&&\\cr\n"%(nomf,var)
            cor+="\\tx{%s}&\\txh{%s}&\\fd&\\txb{%s}\\cr\n"%(nomf,f_xmin,f_xmax)
            cor+="}\n"
                                                              
            
        else:
            cor+=u" De plus, $%s>0$ donc pour tout $%s$ de $I$, $%s'(%s)>0$."%\
                  (numerateur_simplifie[0],var,nomf,var)
            cor+="$$\\tabvar{\n"
            cor+="\\tx{%s}&\\tx{%s}&&\\tx{%s}\\cr\n"%(var,TeX(Intervalle[0]),TeX(Intervalle[1]))
            cor+="\\tx{%s'(%s)}&&\\tx{+}&&\\cr\n"%(nomf,var)
            cor+="\\tx{%s}&\\txb{%s}&\\fm&\\txh{%s}\\cr\n"%(nomf,f_xmin,f_xmax)
            cor+="}$$\n"
    else:
        cor+=u"\\item Je ne sais pas faire avec un tel numérateur"
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor


def exo_variation():
    '''Exercice qui propose l'étude du sens de variation d'un polynôme de degré 3'''

    #intervalle pour les racines entières ou fractionnaire
    a=3*randint(1,3)
    rac_min=-10
    rac_max=10
    #denominateur maximmum pour les racines fractionnaires
    denom_max=denom1=12
    #Valeurs absolues maximales des coefficients d'un polynôme quelconque
    abs_a=6
    abs_b=10
    abs_c=10
    #X est le polynome P=x pour faciliter la construction des polynômes, TODO : changer  l'inconnue
    inconnues=['x','y','z','t']
    nom_poly=['P','Q','R','S']
    var="x"
    X=Polynome({1:1},var=var)
    nomP=["f","g","h","k","p","q"][randrange(6)]
    exo="\\begin{enumerate}\n"
    cor="\\begin{enumerate}\n"
    Pprime=poly_racines_entieres(rac_min,rac_max,X,a1=a)
    P=Pprime.primitive()+randint(-abs_c,abs_c)
    exo+=u"\\item Étudier le sens de variations de $%s$ définie par $%s(x)=%s$\n" % (nomP,nomP,P)
    cor+="\\item $%s(x)=%s$ donc $%s'(x)=%s$\\\\\n" % (nomP,P,nomP,Pprime)
    corfac,delta,P1,P2,x1,x2=factorisation_degre2(Pprime,nomP=nomP+"'",detail=True,factorisation=True)
    cor+=corfac+"\\\\\n"
    tab_signe,str_signe=tableau_de_signe(Pprime,nomP+"'",delta,P1,P2,x1,x2,detail=True)
    cor+=tab_signe
    if str_signe==u"négatif" or (delta==0 and P[3]<0):
        cor+=u"Donc la fonction polynômiale $%s$ est décroissante sur $\mathbb R$.\n" %(nomP)
    elif str_signe=="positif" or (delta==0 and P[3]>0):
        cor+=u"Donc la fonction polynômiale $%s$ est croissante sur $\mathbb R$.\n"%(nomP)
    else:
        cor+="On obtient ainsi le tableau de variation de $%s$."%nomP
        if P[3]>0:
            var_de_P="\\tx{%s}& &\\fm&\\txh{%s}&\\fd&\\txb{%s}&\\fm&\\cr"\
                        %(nomP,TeX(P(int(re.findall("[\-0-9]+",x1)[0]))),TeX(P(int(re.findall("[\-0-9]+",x2)[0]))))
        else:
            var_de_P="\\tx{%s}& &\\fd&\\txb{%s}&\\fm&\\txh{%s}&\\fd&\\cr"\
                      %(nomP,x1,x2)
        
        cor+="$$\
        \\tabvar{\n\
        \\tx{%s}& \\tx{+\\infty}&& \\tx{%s}&&\\tx{%s}&& \\tx{-\\infty}\\cr\n\
        %s %s}$$"%(P.var,x1,x2,str_signe,var_de_P)
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor


def exo_tableau():
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
    var="x"
    X=Polynome({1:1},var=var)
    Poly=[poly_racines_entieres(rac_min,rac_max,X),poly_racines_fractionnaires(rac_min,rac_max,denom1,X,deltanul=False),poly_racines_quelconques(abs_a,abs_b,abs_c,X)]
    nomP="P"
    exo="\\begin{enumerate}\n"
    cor="\\begin{enumerate}\n"
    for i in range(len(Poly)):
        P=Poly[i]
        exo+=u"\\item Étudier le signe du polynôme $%s=%s$\n" % (nomP,P)
        cor+="\\item $%s=%s$\\\\\n" % (nomP,P)
        corfac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP=nomP,detail=True,factorisation=True)
        cor+=corfac+"\\\\\n"
        cor+=tableau_de_signe(P,nomP,delta,P1,P2,x1,x2)
    
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor

def exo_racines_degre2():
    '''exercice recherche de racines second degré'''
    #intervalle pour les racines entières ou fractionnaire
    rac_min=-10
    rac_max=10
    #denominateur maximmum pour les racines fractionnaires
    denom_max=denom1=12
    #Valeurs absolues maximales des coefficients d'un polynôme quelconque
    abs_a=1
    abs_b=10
    abs_c=10
    #X est le polynome P=x pour faciliter la construction des polynômes,
    inconnues=['x','y','z','t']
    nom_poly=['P','Q','R','S']

    exo=u"Résoudre les équations suivantes :\n"
    cor=u"Résoudre les équations suivantes :\n"
    exo+="\\begin{enumerate}\n\
          \\begin{multicols}{3}\n"
    cor+="\\begin{enumerate}\n"
    for i in range(2):
        var=inconnues[randrange(4)]
        X=Polynome({1:1},var)
        P,sgns=poly_id_remarquables(rac_min,rac_max,X)
        exo+="\\item $%s=0$\n"%(P(var))
        exot,cor,racines=identites_remarquables(exo,cor,P,sgns,racines=True)
        cor+=u"\\\\\n On en déduit que l'équation a "
        if len(racines)==1:
            cor+="une solution $%s=%s$\n"%(X.var,TeX(racines[0]))
        else:
            cor+="deux solutions $%s=%s$ ou $%s=%s$\n"%(X.var,TeX(racines[0]),X.var,TeX(racines[1]))
    for i in range(2):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_entieres(rac_min,rac_max,X)
        #exo,cor=degre2racine(exo,cor,P,nomP="P")
        exo+="\\item $%s=0$\n"%(P(var))
        cor_fac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP="P",detail=True,factorisation=False)
        cor+="\\item "+cor_fac+"\n" 

    for i in range(3):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_fractionnaires(rac_min,rac_max,denom1,X,deltanul=False)
        #exo,cor=degre2racine(exo,cor,P,nomP="P")
        exo+="\\item $%s=0$\n"%(P(var))
        cor_fac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP="P",detail=True,factorisation=False)
        cor+="\\item "+cor_fac+"\n" 
    
    for i in range(2):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)
        #exo,cor=degre2racine(exo,cor,P,nomP="P")
        exo+="\\item $%s=0$\n"%(P(var))
        cor_fac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP="P",detail=True,factorisation=False)
        cor+="\\item "+cor_fac+"\n" 
    
    exo+="\\end{multicols}\n\
          \\end{enumerate}\n"
    cor+="\\end{enumerate}\n"  
    return exo,cor  
    
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
    exo="\\begin{enumerate}\n"
    cor="\\begin{enumerate}\n"
    for i in range(2):
        nomP="P"
        X=Polynome({1:1},var=inconnues[randrange(4)])
        pol1,sgns=poly_id_remarquables(rac_min,rac_max,X)
        exo,cor,racines=identites_remarquables(exo,cor,pol1,sgns,nomP)

    for i in range(2):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_entieres(rac_min,rac_max,X)
        exo+=u"\\item Factoriser le polynôme $$%s=%s$$\n"%(nomP,P)
        cor+="\\item "+factorisation_degre2(P)
        
    for i in range(3):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_fractionnaires(rac_min,rac_max,denom1,X)
        exo+=u"\\item Factoriser le polynôme $$%s=%s$$\n"%(nomP,P)
        cor+="\\item "+factorisation_degre2(P)
    
    for i in range(2):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)
        exo+=u"\\item Factoriser le polynôme $$%s=%s$$\n"%(nomP,P)
        cor+="\\item "+factorisation_degre2(P)

    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor
    
def Exo_factorisation_degre3():
    '''exercice de factorisation degre3'''

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
    exo="\\begin{enumerate}\n"
    cor="\\begin{enumerate}\n"
    for i in range(2):
        X=Polynome({1:1},var="x")
        E=poly_degre3_racines_entieres(rac_min,rac_max,X)
        exo,cor=factorisation_degre3(E,"E",exo,cor)
        F=poly_degre3_racines_fractionnaires(rac_min,rac_max,denom1,X)
        exo,cor=factorisation_degre3(F,"F",exo,cor)
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor 

def factorisation_degre2(P,nomP="P",detail=False,factorisation=True):
    cor=""
    x1=x2=0
    delta=int(P[1]**2-4*P[2]*P[0])
    cor+=u"Je calcule $\Delta=%s^2-4\\times %s\\times %s=%s$"%(pTeX(P[1]),pTeX(P[2]),pTeX(P[0]),TeX(delta))
    if delta<0:
        cor+=" donc $%s$ n'a pas de racines."%(nomP)
        P1=P
        P2=""
    elif delta==0:
        x0=Fractions(-1,2)*P[1]/P[2]
        cor+=" donc $%s$ a une seule racine $%s_0=%s$.\\par\n"%(nomP,P.var,TeX(x0))
        if factorisation:
            cor+=u"Ainsi $%s$ peut s'écrire $%s="%(nomP,nomP)
            if P[2]!=1:
                cor+=TeX(P[2])
        P1=u"{\\left(%s\\right)}^2"%(Polynome({1:1,0:-x0},var=P.var))
        P2=""
        cor+=P1+"$.\n"
    else:
        rac_delta,simplrac,strx1,x1,strx2,x2,parenthesex1,parenthesex2=listeracines(P[2],P[1],delta)
        if simplrac:
            cor+=" et $%s=%s$"%(radicalTeX(delta),rac_delta)
        cor+=".\par\n"
        cor+=" Les racines de $%s$ sont $%s_1=%s=%s$ et $%s_2=%s=%s$.\n"%(nomP,P.var,strx1,x1,P.var,strx2,x2)
        if factorisation:
            cor+=u"\\\\ Donc $%s$ peut s'écrire $%s(%s)=\n"%(nomP,nomP,P.var)
            if parenthesex1:
                x1="\\left(%s\\right)"%(x1)
            if parenthesex2:
                x2="\\left(%s\\right)"%(x2)
            cor+="%s\\times\\left(%s-%s\\right)\\times\\left(%s-%s\\right)$.\n"%(TeX(P[2]),P.var,x1,P.var,x2)
        P1="%s-%s"%(P.var,x1)
        P2="%s-%s"%(P.var,x2)
    if detail:
        return cor,delta,P1,P2,x1,x2
    else:
        return cor

def TeXracines(a,b,delta,simple=True):
    '''renvoie la formule des racines sous forme TeX'''
    strx1="\\dfrac{-%s-\\sqrt{%s}}{2\\times %s}"%(pTeX(b),TeX(delta),pTeX(a))
    strx2="\\dfrac{-%s+\\sqrt{%s}}{2\\times %s}"%(pTeX(b),TeX(delta),pTeX(a))
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
    a=int(a)
    b=int(b)
    parenthesex1=parenthesex2=True #par défaut
    simplrac=True
    strx1="\\dfrac{-%s-\\sqrt{%s}}{2\\times %s}"%(pTeX(b),TeX(delta),pTeX(a))
    strx2="\\dfrac{-%s+\\sqrt{%s}}{2\\times %s}"%(pTeX(b),TeX(delta),pTeX(a))
    ##on a strx1<strx2
    coeff,radicande=simplifie_racine(delta)
    if radicande==1:#delta est un carré
        rac_delta=TeX(coeff)
        x1=TeX((Fractions(1)*(-b-coeff)/(2*a)).simplifie())
        x2=TeX((Fractions(1)*(-b+coeff)/(2*a)).simplifie())
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

###############################################
#
#   Fonctions étudiant les polynômes
#
###############################################

def identites_remarquables(exo,cor,pol1,sgns,nomP="P",racines=True):
    '''Factorise un polynomes grâce aux identités remarquables'''
    
    X=Polynome({1:1},pol1.var)
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
    exo+=u"\\item  Factoriser le polynôme $$%s=%s$$\n"%(nomP,pol1)
    if a1!=1:
        cor+="\\item On remarque que $%s = %s = %s \\times\\big[ %s \\big]"%(nomP,pol1,TeX(a1),(pol1/a1).simplifie())
        cor+="= %s\\times \\big["%(TeX(a1))
    else:
        cor+="\\item $%s=%s ="%(nomP,pol1)
    if c!=1:
        cor+=u"(%s %s)^2"%(TeX(c),pol1.var)
    else:
        cor+=pol1.var+u"^2"
    if sgns:
        if sgns==-2: #-2 => (a-b)²
            cor+= "-2 \\times "
        else:        #+2 => (a+b)²
            cor+= "+2 \\times "
        if c<0:      #impossible ! 
            print "on peut avoir c<0 dans identites_remarquables"
            cor+="\\left(%s %s\\right)"%(TeX(c),pol1.var)
        elif c==1:
            cor+=pol1.var
        else:
            cor+=TeX(c)+pol1.var
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
    sgns=sgns/2
    if sgns:#(cx-b)² ou (cx+b)²
        liste_racines=[Fractions(-(sgns))*b/c]
        cor+="{(%s)}^2$"%(c*X+sgns*b)
    else:#(cx-b)(cx+b)
        liste_racines=[Fractions(-1)*b/c,Fractions(1)*b/c]
        cor+="(%s)(%s)$"%(c*X+b,c*X-b)
    if racines:
        return exo,cor,liste_racines
    return exo,cor


def tableau_de_signe(P,nomP,delta,P1,P2,x1,x2,detail=False):
    '''Étudie le signe d'un polynôme de degré2'''
    '''detail=True permet de récupérer la dernière ligne avec le signe de P'''

    if delta<0:
        if P[0]<0:
            signe=u"négatif"
        else:
            signe="positif"
        if detail:
            return "Donc $%s$ ne change pas de signe donc $%s$ est $%s$\\\\\n"%(nomP,nomP,signe),signe
        else:
            return "Donc $%s$ ne change pas de signe donc $%s$ est $%s$\\\\\n"%(nomP,nomP,signe)
    elif delta==0:
        tab_signe="$$\\tabvar{\n\
                \\tx{x}&\\tx{+\\infty}&& \\tx{%s}&& \\tx{-\\infty}\\cr\n\
                \\tx{%s(%s)}&&\\tx{+}&\\tx{%s}&\\tx{-}&\\cr}$$" % (x1,nomP,P.var,x1)
        str_signe="\\tx{%s(%s)}&&\\tx{+}&\\tx{%s}&\\tx{-}&\\cr" % (nomP,P.var,x1)
        if detail:
            return tab_signe,str_signe
        else:
            return tab_signe
    else:
        if P[2]>0:
            str_a="\\tx{%s}& & \\tx{+} && \\tx{+} && \\tx{+} & \\cr\n" %(P.var)
            str_signe="\\tx{%s(%s)}& &\\tx{+}&\\tx{0}&\\tx{-}&\\tx{0}&\\tx{+}&\\cr\n"% (nomP,P.var)
        else:
            str_a="\\tx{%s}& & \\tx{-} && \\tx{-} && \\tx{-} & \\cr\n" %(P.var)
            str_signe="\\tx{%s(%s)}& &\\tx{-}&\\tx{0}&\\tx{+}&\\tx{0}&\\tx{-}&\\cr\n" % (nomP,P.var)
        tab_signe="$$\\tabvar{\n\
                \\tx{%s}& \\tx{+\\infty}&& \\tx{%s}&&\\tx{%s}&& \\tx{-\\infty}\\cr\n\
                \\tx{%s}& & \\tx{-} &\\tx{0}& \\tx{+} && \\tx{+} & \\cr\n\
                \\tx{%s}& & \\tx{-} && \\tx{-} &\\tx{0}& \\tx{+} & \\cr\n\
                %s%s}$$" % (P.var,x1,x2,P1,P2,str_a,str_signe)
    if detail:
        return tab_signe,str_signe
    else:
        return tab_signe

def factorisation_degre3(E,nomE,exo="",cor="",racines=[0,1,-1,2,-2]):
    '''Factorise un polynôme de degré 3 avec une racine évidente'''
    X=Polynome({1:1},E.var)
    exo+="\\item Soit $%s =%s $\n"%(nomE,E)
    cor+="\\item Soit $%s=%s $\n"%(nomE,E)
    exo+="\\begin{enumerate}\n"
    cor+="\\begin{enumerate}\n"
    exo+=u"\\item Vérifier si $%s $ possède une racine évidente.\n"%(nomE)
    exo+="\\item Factoriser $%s $.\n"%(nomE)
    cor+="\\item "
    for x0 in racines:
        if E(x0)==0:
            break
    if x0==0:
        #degre_facteur=min(E.puiss)
        degre_facteur=1
        E2=(E/(X**degre_facteur))[0]
        if degre_facteur==1:
            cor+="On remarque que $%s$ peut se factoriser par $%s$ et $%s=%s\\left(%s\\right)$" %(nomE,E.var,nomE,E.var,E2)
        else:
            cor+=u"On remarque que $%s$ peut se factoriser par $%s^%s$ et $%s=%s^%s\\left(%s\\right)$"\
            %(nomE,E.var,str(degre_facteur),nomE,E.var,str(degre_facteur),E2)
    else:            
        cor+="Comme $%s(%s)=0$, on peut diviser $%s$ par $%s$\n"%(nomE,TeX(x0),nomE,X-x0)
        cor+=TeX_division(E,(X-x0))+"\n"
        E2,reste=E/(X-x0)
    cor+="\\item On doit maintenant factoriser le polynome $%s_2=%s$\\\\\n"%(nomE,E2)
    cor2,delta,P1,P2,x1,x2=factorisation_degre2(E2,nomP=nomE+"_2",detail=True)
    cor+=cor2+"\\\\\n"
    cor+="On en conclue donc que $%s="%(nomE)
    final=0
    if x0==0:
        P0=E.var
    else:
        P0="\\left(%s\\right)"%(X-x0)
    if E[3]==-1:
        cor+="-"
    elif E[3]!=1:
        cor+=TeX(E[3])            
    if delta<=0:
        E_factorise="%s\\times%s$\n"%(P0,P1)
    else:
        E_factorise="%s\\left(%s\\right)\\left(%s\\right)$\n"%(P0,P1,P2)
        x12=[x1,x2]
        for i in range(2):
            if isinstance(x12[i],str) and len(x12[i])>6 and x12[i][6]=="-":
                final=1
                x12[i]=x12[i][7:-7]
        x1,x2=x12[0],x12[1]
        E_final="%s\\left(%s+%s\\right)\\left(%s+%s\\right)\n"%(P0,E.var,x1,E.var,x2)

    cor+=E_factorise
    if final:
        cor+="\\\\\n Finalement, $%s=%s $\n"%(nomE,E_final)
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor

if __name__=="__main__":
    from TEST.imprimetest import *
    #exo,cor=Exo_factorisation()#denom1=12)
    #exo,cor=exo_tableau()
    exo,cor=exo_variation()
    for i in range(50):
        Exo_factorisation_degre3()
    exo,cor=exo_fonctions_rationnelles()
    imprime_TeX(exo+cor)
