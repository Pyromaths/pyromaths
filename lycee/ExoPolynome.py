# -*- coding: utf-8 -*-

import sys, os, codecs
sys.path.append("/home/nicolas/pyrogit/pyromaths")
from outils.Polylycee import *
#from outils.Affichage import TeX,tTeX,TeXz,pTeX
from random import randrange,randint
from math import *
from re import findall
##pyropath=os.path.normpath(os.path.join(os.getcwd(),'..'))
##sys.path.append(pyropath)
from outils.Arithmetique import carrerise,pgcd

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
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P,sgns=poly_id_remarquables(rac_min,rac_max,X)
        exo+="\\item $"+P.TeX()+"=0$\n"
        exot,cor,racines=identites_remarquables(exo,cor,P,sgns,racines=True)
        cor+=u"\\\\\n On en déduit que l'équation a "
        if len(racines)==1:
            cor+="une solution $"+X.var+"="+TeX(racines[0])+"$\n"
        else:
            cor+="deux solutions $"+X.var+"="+TeX(racines[0])+"$ ou $"+X.var+"="+TeX(racines[1])+"$\n"
    for i in range(2):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_entieres(rac_min,rac_max,X)
        #exo,cor=degre2racine(exo,cor,P,nomP="P")
        exo+="\\item $"+P.TeX()+"=0$\n"
        cor_fac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP="P",detail=True,factorisation=False)
        cor+="\\item "+cor_fac+"\n" 

    for i in range(3):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_fractionnaires(rac_min,rac_max,denom1,X,deltanul=False)
        #exo,cor=degre2racine(exo,cor,P,nomP="P")
        exo+="\\item $"+P.TeX()+"=0$\n"
        cor_fac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP="P",detail=True,factorisation=False)
        cor+="\\item "+cor_fac+"\n" 
    
    for i in range(2):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)
        #exo,cor=degre2racine(exo,cor,P,nomP="P")
        exo+="\\item $"+P.TeX()+"=0$\n"
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
#    exo="\\exercice\n"
#    cor="\\exercice*\n"
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
        exo,cor=degre2racine(exo,cor,P,nomP="P")
    
        #exo,cor=degre2racine_entiere(exo,cor,rac_min,rac_max,X)
    
    for i in range(3):
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_fractionnaires(rac_min,rac_max,denom1,X)
        exo,cor=degre2racine(exo,cor,P,nomP="P")
    
        #exo,cor=degre2racinefractionnaire(exo,cor,rac_min,rac_max,denom1,X)
    
    for i in range(2):
        #exo,cor=degre2racinequelconque(exo,cor,abs_a=1,abs_b=10,abs_c=10,X=X)
        X=Polynome({1:1},var=inconnues[randrange(4)])
        P=poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)
        exo,cor=degre2racine(exo,cor,P,nomP="P")
    
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
#    exo="\\exercice\n"
#    cor="\\exercice*\n"
    exo="\\begin{enumerate}\n"
    cor="\\begin{enumerate}\n"
    for i in range(2):
        X=Polynome({1:1},var="x")
        E=poly_degre3_racines_entieres(rac_min,rac_max,X)
        exo,cor=factorisation_degre3(E,"E",exo,cor)
        F=poly_degre3_racines_fractionnaires(rac_min,rac_max,denom1,X)
        exo,cor=factorisation_degre3(F,"F",exo,cor)
#    Q=poly_degre3_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)
#    exo+="\\item ou bien $Q="+Q.TeX()+"$\n"
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor 

def factorisation_degre3(E,nomE,exo="",cor=""):
    X=Polynome({1:1},E.var)
    exo+="\\item Soit $"+nomE+"="+E.TeX()+"$\n"
    cor+="\\item Soit $"+nomE+"="+E.TeX()+"$\n"
    exo+="\\begin{enumerate}\n"
    cor+="\\begin{enumerate}\n"
    exo+=u"\\item Vérifier si $"+nomE+u"$ possède une racine évidente.\n"
    exo+="\\item Factoriser $"+nomE+"$.\n"
    cor+="\\item "
    racines=[]
    for x0 in [0,1,-1,2,-2]:
        if E(x0)==0:
            break
    cor+="Comme $"+nomE+"("+TeX(x0)+")=0$, on peut diviser $"+nomE+"$ par $"+(X-x0).TeX()+"$\n"
    cor+=TeX_division(E,(X-x0))+"\n"
    E2,reste=E/(X-x0)
    cor+="\\item On doit maintenant factoriser le polynome $"+nomE+"_2="+ E2.TeX() +"$\\\\\n"
    cor2,delta,P1,P2,x1,x2=factorisation_degre2(E2,nomP="E_2",detail=True)
    cor+=cor2+"\\\\\n"
    cor+="On en conclue donc que $"+nomE+"="
    final=0
    if x0==0:
        P0=E.var
    else:
        P0="\\left("+(X-x0).TeX()+"\\right)"
    if E[3]==-1:
        cor+="-"
    elif E[3]!=1:
        cor+=TeX(E[3])            
    if delta<=0:
        E_factorise=P0+"\\times"+P1+"$\n"
    else:
        E_factorise=P0+"\\left("+P1+"\\right)\\left("+P2+"\\right)$\n"
        x12=[x1,x2]
        for i in range(2):
            if isinstance(x12[i],str) and len(x12[i])>6 and x12[i][6]=="-":
                final=1
                x12[i]=x12[i][7:-7]
        x1,x2=x12[0],x12[1]
        E_final=P0+"\\left("+E.var+"+"+x1+"\\right)\\left("+E.var+"+"+x2+"\\right)\n"

    cor+=E_factorise
    if final:
        cor+="\\\\\n Finalement, $"+nomE+"="+E_final+"$\n"
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor
    
def poly_degre3_racines_entieres(rac_min,rac_max,X):
    racine_evidente=[-2,-1,0,1,2][randrange(5)]
    return (X-racine_evidente)*poly_racines_entieres(rac_min,rac_max,X)
def poly_degre3_racines_fractionnaires(rac_min,rac_max,denom1,X):
    racine_evidente=[-2,-1,0,1,2][randrange(5)]
    return (X-racine_evidente)*poly_racines_fractionnaires(rac_min,rac_max,denom1,X)
def poly_degre3_racines_quelconques(abs_a,abs_b,abs_c,X):
    racine_evidente=[-2,-1,0,1,2][randrange(5)]
    return (X-racine_evidente)*poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)

def degre2racine(exo,cor,P,nomP="P"):
    var=P.var
    #X=Polynome({1:1},var=P.var)
    exo+=u"\\item Factoriser le polynôme $$"+nomP+"="+P.TeX()+"$$\n"
    cor+="\\item "+factorisation_degre2(P)
    return exo,cor

def factorisation_degre2(P,nomP="P",detail=False,factorisation=True):
    cor=""
    x1=x2=0
    delta=int(P[1]**2-4*P[2]*P[0])
    cor+="Je calcule $\Delta="+pTeX(P[1])+u"^2-4\\times"+pTeX(P[2])+"\\times"+pTeX(P[0])+"="\
    +TeX(delta)+"$"
    if delta<0:
        cor+=" donc $"+nomP+"$ n'a pas de racines."
        P1=P.TeX()
        P2=""
    elif delta==0:
        x0=Fraction(-1,2)*P[1]/P[2]
        cor+=" donc $"+nomP+"$ a une seule racine $"+P.var+"_0="+TeX(x0)+"$.\\par\n"
        if factorisation:
            cor+=u"Ainsi $"+nomP+u"$ peut s'écrire $"+nomP+"="
            if P[2]!=1:
                cor+=TeX(P[2])
        P1="{\\left("+(Polynome({1:1,0:-x0},var=P.var)).TeX()+u"\\right)}^2"
        P2=""
        cor+=P1+"$.\n"
    else:
        rac_delta,simplrac,strx1,x1,strx2,x2,parenthesex1,parenthesex2=listeracines(P[2],P[1],delta)
        if simplrac:
            cor+=" et $"+radicalTeX(delta)+"="+rac_delta+"$"
        cor+=".\par\n"
        cor+=" Les racines de $"+nomP+"$ sont $"+P.var+"_1="+ strx1 +"="+x1 +"$ et $"+P.var+"_2="+ strx2 + "="+x2 +"$.\n"
        if factorisation:
            cor+=u"\\\\ Donc $%s$ peut s'écrire $%s(%s)=\n"%(nomP,nomP,P.var)
            if parenthesex1:
                x1="\\left("+x1+"\\right)"
            if parenthesex2:
                x2="\\left("+x2+"\\right)"
            cor+=TeX(P[2])+"\\times\\left("+P.var+"-"+x1+"\\right)\\times\\left("+P.var+"-"+x2+"\\right)$.\n"
        P1=P.var+"-"+x1
        P2=P.var+"-"+x2
    if detail:
        return cor,delta,P1,P2,x1,x2
    else:
        return cor
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

def poly_racines_entieres(rac_min,rac_max,X,a1=1):
    p1facteur=[X-randrange(rac_min,rac_max) for i in range(2)]
    pol1=a1*p1facteur[0]*p1facteur[1]
    return pol1
def poly_id_remarquables(rac_min,rac_max,X):
    '''Renvoie un polynome obtenu par une identité remarquable'''
    
    a=randint(1,10)
    while 1:
        coeff=randrange(rac_min,rac_max)
        racine=randrange(rac_min,rac_max)
        if coeff!=0 and racine!=0:
            break
    sgns=[[-1,1][randrange(2)]for i in range(2)]
    p1facteur=[coeff*X+sgns[i]*racine for i in range(2)]
    return a*p1facteur[0]*p1facteur[1],sum(sgns)   
        #sum(sgns) permet de connaître l'identité
        # -2 => (a-b)²
        # +2 => (a+b)²
        # 0 => (a-b)(a+b)


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
    exo+=u"\\item  Factoriser le polynôme $$"+nomP+"="+pol1.TeX()+"$$\n"
    if a1!=1:
        cor+="\\item On remarque que $"+nomP+"="+pol1.TeX()+"="+TeX(a1)+"\\times\\big["+(pol1/a1).TeX()+"\\big]"
        cor+="="+TeX(a1)+"\\times \\big["
    else:
        cor+="\\item $"+nomP+"="+pol1.TeX()+"="
    if c!=1:
        cor+="("+TeX(c)+pol1.var+u")^2"
    else:
        cor+=pol1.var+u"^2"
    if sgns:
        if sgns==-2: #-2 => (a-b)²
            cor+= "-2 \\times "
        else:        #+2 => (a+b)²
            cor+= "+2 \\times "
        if c<0:      #impossible ! 
            print "on peut avoir c<0 dans identites_remarquables"
            cor+="\\left("+TeX(c)+pol1.var+"\\right)"
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
        liste_racines=[Fraction(-(sgns))*b/c]
        cor+="{("+ (c*X+sgns*b).TeX() +")}^2$"
    else:#(cx-b)(cx+b)
        liste_racines=[Fraction(-1)*b/c,Fraction(1)*b/c]
        cor+="("+ (c*X+b).TeX() +")("+(c*X-b).TeX()+")$"
    if racines:
        return exo,cor,liste_racines
    return exo,cor

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
def tableau_de_signe(P,nomP,delta,P1,P2,x1,x2,detail=False):
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
        tab_signe="$$\
                \\tabvar{\%\
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
        tab_signe="$$\
                \\tabvar{\
                \\tx{%s}& \\tx{+\\infty}&& \\tx{%s}&&\\tx{%s}&& \\tx{-\\infty}\\cr\n\
                \\tx{%s}& & \\tx{-} &\\tx{0}& \\tx{+} && \\tx{+} & \\cr\n\
                \\tx{%s}& & \\tx{-} && \\tx{-} &\\tx{0}& \\tx{+} & \\cr\n\
                %s%s}$$" % (P.var,x1,x2,P1,P2,str_a,str_signe)
    if detail:
        return tab_signe,str_signe
    else:
        return tab_signe

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
        exo+=u"\\item Étudier le signe du polynôme $%s=%s$\n" % (nomP,P.TeX())
        cor+="\\item $%s=%s$\\\\\n" % (nomP,P.TeX())
        corfac,delta,P1,P2,x1,x2=factorisation_degre2(P,nomP=nomP,detail=True,factorisation=True)
        cor+=corfac+"\\\\\n"
        cor+=tableau_de_signe(P,nomP,delta,P1,P2,x1,x2)
    
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor

def exo_variation():
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
    exo+=u"\\item Étudier le sens de variations de $%s$ définie par $%s(x)=%s$\n" % (nomP,nomP,P.TeX())
    cor+="\\item $%s(x)=%s$ donc $%s'(x)=%s$\\\\\n" % (nomP,P.TeX(),nomP,Pprime.TeX())
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
            var_de_P="\\tx{%s}& &\\fm&\\txh{%s}&\\fd&\\txb{%s}&\\fm&\\cr\n"\
                        %(nomP,TeX(P(int(re.findall("[\-0-9]+",x1)[0]))),TeX(P(int(re.findall("[\-0-9]+",x2)[0]))))
        else:
            var_de_P="\\tx{%s}& &\\fd&\txb{%s}&\\fm&\\txh{%s}&\\fd&\\cr\n"\
                      %(nomP,TeX(P(int(re.findall("[\-0-9]+",x1)[0]))),TeX(P(int(re.findall("[\-0-9]+",x2)[0]))))
        
        cor+="$$\
            \\tabvar{\
            \\tx{%s}& \\tx{+\\infty}&& \\tx{%s}&&\\tx{%s}&& \\tx{-\\infty}\\cr\n\
            %s\
            %s}$$"%(P.var,x1,x2,str_signe,var_de_P)
    exo+="\\end{enumerate}\n"
    cor+="\\end{enumerate}\n"
    return exo,cor


if __name__=="__main__":
    from TEST.imprimetest import *
    #exo,cor=Exo_factorisation()#denom1=12)
    #exo,cor=exo_tableau()
    exo,cor=exo_variation()
    imprime_TeX(exo+cor)
